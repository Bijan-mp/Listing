from django.utils import timezone

import datetime
from django.test import TestCase

from reservation.models import House, ListingOwner, Room


def create_owner(name):
    return ListingOwner.objects.create(name=name)


def create_house(owner=None, name="h", address="address"):
    if owner is None:
        owner = create_owner(name=name)
    return House.objects.create(owner=owner, name=name, address=address)


def create_room(house=None):
    if house is None:
        house = create_house()
    return Room.objects.create(house=house)


def reserve_room(
    room=None, start_date=timezone.now(), end_date=timezone.now(), client_name="c name"
):
    if room is None:
        room = create_room()
    return room.reserve(
        client_name=client_name, start_date=start_date, end_date=end_date
    )


class RoomModelTestCase(TestCase):
    '''
    The Important test for this model is reservation test.
    If the business logic of reservation hase problem, it may couse conflict in reservation.
    Because this is a sample project , just test get_available_room_list() to prevent this problem
    '''
    
    def setUp(self):
        # Every test needs access to the request factory.
        self.available_range_start = timezone.now()
        self.available_range_end = self.available_range_start + datetime.timedelta(
            days=5
        )
    
    def test_avalablity_of_room_that_has_not_been_reserved_yet(self):
        """
        get_available_room_list()
        The method must return rooms that have note been reserved yet.

        """
        room = create_room()

        available_rooms = Room.get_available_room_list(
            start_date=self.available_range_start, end_date=self.available_range_end
        )
        self.assertIn(room, available_rooms)

    def test_avalablity_of_room_booked_and_delivered_befor_date_range(self):
        """
        get_available_room_list()
        The method must return rooms have booked and delivered befor available date range

        """
        room = create_room()
        reserve_room(
            room=room,
            start_date=(self.available_range_start - datetime.timedelta(days=20)),
            end_date=(self.available_range_start - datetime.timedelta(days=10)),
        )

        available_rooms = Room.get_available_room_list(
            start_date=self.available_range_start, end_date=self.available_range_end
        )

        self.assertIn(room, available_rooms)

    def test_avalablity_of_room_are_reserved_after_date_range(self):
        """
        get_available_room_list()
        The method must return rooms are reserved after available date range.

        """
        room = create_room()
        reserve_room(
            room=room,
            start_date=(self.available_range_end + datetime.timedelta(days=10)),
            end_date=(self.available_range_end + datetime.timedelta(days=12)),
        )
        available_rooms = Room.get_available_room_list(
            start_date=self.available_range_start, end_date=self.available_range_end
        )
        self.assertIn(room, available_rooms)

    def test_avalablity_of_room_with_reserve_start_in_date_range(self):
        """
        get_available_room_list()
        The method must not return rooms that reserved start date in available date range.

        """
        room = create_room()
        reserve_room(
            room=room,
            start_date=(self.available_range_start + datetime.timedelta(days=1)),
            end_date=(self.available_range_end + datetime.timedelta(days=1)),
        )
        available_rooms = Room.get_available_room_list(
            start_date=self.available_range_start, end_date=self.available_range_end
        )
        self.assertNotIn(room, available_rooms)

    def test_avalablity_of_room_with_reserve_end_in_date_range(self):
        """
        get_available_room_list()
        The method must not return rooms that reserved end date in available date range.

        """
        room = create_room()
        reserve_room(
            room=room,
            start_date=(self.available_range_start - datetime.timedelta(days=1)),
            end_date=(self.available_range_end - datetime.timedelta(days=1)),
        )
        available_rooms = Room.get_available_room_list(
            start_date=self.available_range_start, end_date=self.available_range_end
        )
        self.assertNotIn(room, available_rooms)

    def test_avalablity_of_room_reserved_in_date_range(self):
        """
        get_available_room_list()
        The method must not return rooms are reserved in available date range.

        """
        room = create_room()
        reserve_room(
            room=room,
            start_date=(self.available_range_start + datetime.timedelta(days=1)),
            end_date=(self.available_range_end - datetime.timedelta(days=1)),
        )

        available_rooms = Room.get_available_room_list(
            start_date=self.available_range_start, end_date=self.available_range_end
        )
        self.assertNotIn(room, available_rooms)

    def test_avalablity_of_room_reserved_befor_available_date_range_and_will_delivered_after_range(
        self,
    ):
        """
        get_available_room_list()
        The method must not return rooms are reserved befor available date range
        and will be delivered after available date range.
        """
        room = create_room()
        reserve_room(
            room=room,
            start_date=(self.available_range_start - datetime.timedelta(days=2)),
            end_date=(self.available_range_end + datetime.timedelta(days=2)),
        )
        available_rooms = Room.get_available_room_list(
            start_date=self.available_range_start, end_date=self.available_range_end
        )
        self.assertNotIn(room, available_rooms)
