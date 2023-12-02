from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views import generic
from django.db.models import Q
from .views_helper import RoomSearch
from django.http import HttpResponse

from .models import RoomType, Room, ReservationCart, RoomReservations

# Create your views here.
class RoomDetailView(generic.DetailView):
    model = RoomType
    template_name = 'booking/room_detail.html'
    context_object_name = 'room'

    def get_object(self):
        # UpdateUser view is expecting a primary key (pk) or slug in the URL, but it's not receiving it.
        # I'm updating the get_object method so it uses the uuid instead of the pk.
        return RoomType.objects.get(uuid=self.kwargs['uuid'])


def find_available_rooms(room_type, r_check_in_date, r_check_out_date):
    # This functions returns all the rooms of a roomtype available from checkin to checkout.
    return Room.objects.filter(
                type = room_type,
                space_taken = False,
            ).exclude(
                room_id__in = RoomReservations.objects.filter(
                    Q(check_out_date__gt=r_check_in_date) & Q(check_in_date__lt=r_check_out_date))
                    .values('room_id')
            )

def reset_user_cart_if_exists(request):
    user_cart = ReservationCart.objects.filter(user=request.user)
    if user_cart.exists():
        if user_cart[0].room:
            user_cart[0].room.space_taken = False
            user_cart[0].room.save()

            user_cart[0].room = None
            user_cart[0].save()

def delete_user_cart_if_exists(request):
    user_cart = ReservationCart.objects.filter(user=request.user)
    if user_cart.exists():
        if user_cart[0].room:
            user_cart[0].room.space_taken = False
            user_cart[0].room.save()

            user_cart[0].room = None
            user_cart[0].save()
        user_cart[0].delete()
    
def search_room(request):
    # first check the user is logged in, with @loginrequired.
    r_adults = int(request.GET.get('adults'))
    r_children = int(request.GET.get('children'))
    r_check_in_date = request.GET.get('check_in_date')
    r_check_out_date = request.GET.get('check_out_date')

    # check if he has a cart.
    if ReservationCart.objects.filter(user=request.user).exists():
        # if he has one delete it, make sure to reset all info.
        user_cart = ReservationCart.objects.filter(user=request.user)
        if user_cart[0].room:
            user_cart[0].room.space_taken = False
        user_cart.delete()
        print("This user already has a cart!, lets delete it!")

    # Then create a new cart for this user.
    ReservationCart.objects.create(
            user=request.user,
            check_in_date = r_check_in_date,
            check_out_date = r_check_out_date,
    )
    print("Just created a new cart for this user!")

    # Now find what type of rooms can have this many guests, and if they are available.
    available_room_types = {'room_types': []} 

    for room_type in RoomType.objects.all():

        if room_type.max_adults >= r_adults and room_type.max_children >= r_children:
            room_type_fits = True # this means that this type of room can fit this many people.
            room_type_available = False # This is to check if there are rooms available for this type.

            # We now need to check, if there rooms available for this type of room.
            available_rooms = find_available_rooms(room_type, r_check_in_date, r_check_out_date)
            # If there is room available for this type.
            if len(available_rooms) > 0:
                room_type_available = True
            
            # If the type applies for the amount of people, and it's available show in the listview as normal.
            # If the room type apllies for the amount of people, but there are not rooms available, show 'habitación no disponible'
            available_room_types['room_types'].append(
                RoomSearch(room_type_object=room_type, room_fits=room_type_fits, room_is_available=room_type_available)
            )
        else:
            # If the amount of people exceds the capicity, then show 'No se puede seleccionar esta habitación porque excede la capacidad permitida'.
            available_room_types['room_types'].append(
                RoomSearch(room_type_object=room_type, room_fits=False, room_is_available=False)
            )
    print(available_room_types['room_types'])
    # This return will send to the template a dictionary which have the [RoomTypeObject, it_fits?, RoomAvailable]
    return render(request, 'booking/search_results.html', available_room_types)

def reservate_now(request):
    # This is a post request, to add a room to the user's cart.
    # User needs to be logged in, and have a cart.
    user_cart_query = ReservationCart.objects.filter(user=request.user)
    user_cart = user_cart_query[0] # because filter returns a queryset and not an object.

    if not user_cart_query.exists():
        # redirect to home.
        print("User doesn't have a cart")
        pass
    else:
        # Lets see if there is a room in there already, if he does reset the cart.
        # This way if he goes back to the page, his choice still remains.
        # If he choses another room then the previous one will be erased, and the other one will be added.
        reset_user_cart_if_exists(request)
    

    # 2. Find an available room of the type requested, and set space_taken = True, and add the room to the cart.
    room_type_name = request.POST.get('room_type_to_reservate')

    room_type = RoomType.objects.filter(type=room_type_name)[0] # We do this to get the object of the class.
    r_check_in_date = user_cart.check_in_date
    r_check_out_date = user_cart.check_out_date
    # Find available room, and set space_taken = true to the first one found.
    available_rooms = find_available_rooms(room_type, r_check_in_date, r_check_out_date)
    # Check if there is room available.
    room_available = len(available_rooms) > 0 # This a boolean value.

    print(available_rooms)

    # Now we need to assign a room to his/her cart.
    reserved_room = available_rooms[0]
    reserved_room.space_taken = True

    reserved_room.save()

    user_cart.room = reserved_room
    user_cart.save()

    return HttpResponse("Room added to cart succesfully.")

    if room_available:
        
        reserved_room = available_rooms[0]
        if not user_cart.room:
            reserved_room.space_taken = True
            user_cart.room = reserved_room # Now this room is added to the user's cart.
            reserved_room.save()
            user_cart.save()
            print(user_cart.room.number)
            print(str(user_cart.room.space_taken))
            return HttpResponse("Room added to cart succesfully.")
        else:
            # If he has a room already reset the space taken attribute, and change its value.
            user_cart.room.space_taken = False

            reserved_room.space_taken = False
            user_cart.room = reserved_room

            reserved_room.save()
            user_cart.save()
            return HttpResponse("cart reset succesfully.")
        
        print(room_type, r_check_in_date, r_check_out_date)
