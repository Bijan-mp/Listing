from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone

from reservation import static_values


class ListingOwner(models.Model):
    name = models.CharField(max_length=100)

    def get_houses(self):
        return self.house_set.all()

    def get_house_room_list(self, house):
        if house.owner == self:
            return house.get_rooms()
        return False

    def get_all_available_room_list(self, start_date, end_date):
        return Room.get_available_room_list(
            start_date=start_date, end_date=end_date, owner=self
        )

    def get_all_room_reservation(self):
        return Reservation.get_all_reservations(owner=self)

    def get_room_reservation_from_now(self):
        return Reservation.get_list_from_now(owner=self)


class House(models.Model):
    name = models.CharField(max_length=100, default=None)
    address = models.CharField(max_length=1024)
    owner = models.ForeignKey(ListingOwner, on_delete=models.CASCADE)

    def get_rooms(self):
        return self.room_set.all()

    def __str__(self):
        return self.name


class Room(models.Model):
    number = models.IntegerField(default=0)
    area = models.IntegerField(default=12)
    single_bed_number = models.IntegerField(default=0)
    double_bed_number = models.IntegerField(default=1)
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    def is_available_at(self, start_date, end_date):
        reservation_list = Reservation.objects.filter(room=self).filter(
            Q(start_date__range=[start_date, end_date])
            | Q(end_date__range=[start_date, end_date])
        )
        if reservation_list.exists():
            return False
        return True

    def reserve(self, client_name, start_date, end_date):
        try:
            reservation = self.reservation_set.create(
                client_name=client_name, start_date=start_date, end_date=end_date
            )
        except ValidationError:
            return False
        else:
            return reservation

    @classmethod
    def get_available_room_list(cls, start_date, end_date, owner=None):
        queryset = Room.objects.exclude(
            Q(reservation__start_date__range=[start_date, end_date])
            | Q(reservation__end_date__range=[start_date, end_date])
            | (
                Q(reservation__start_date__lte=start_date)
                & Q(reservation__end_date__gte=end_date)
            )
        )

        if owner is None:
            return queryset

        try:
            owner = ListingOwner.objects.get(pk=owner.id)
        except ListingOwner.DoesNotExist:
            return False
        else:
            return owner.filter(house__owner=owner)

    def save(self, *args, **kwargs):
        """
        Customize save to make number fields autoincrement per house.
        """
        self.number = self.house.room_set.count() + 1
        super(Room, self).save(*args, **kwargs)

    def __str__(self):
        return "{} house :{}  Room :{}".format(self.id, self.house, self.number)


class Reservation(models.Model):
    client_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    @classmethod
    def get_list_from_now(cls, owner=None):
        queryset = Reservation.objects.filter(
            Q(start_date__gte=timezone.now()) | Q(end_date__gte=timezone.now())
        )
        if owner is None:
            return queryset
        try:
            owner = ListingOwner.objects.get(pk=owner.id)
        except ListingOwner.DoesNotExist:
            return False
        else:
            return queryset.filter(room__house__owner=owner)

    @classmethod
    def get_all_reservations(cls, owner=None):
        if owner is None:
            return Reservation.objects.all()
        try:
            owner = ListingOwner.objects.get(pk=owner.id)
        except ListingOwner.DoesNotExist:
            return False
        else:
            return Reservation.objects.filter(room__house__owner=owner)

    def save(self, *args, **kwargs):
        """
        Customize save to make sure that user can not reserv rooms that are reserved befor.
        """
        if not self.room.is_available_at(self.start_date, self.end_date):
            raise ValidationError(static_values.ErroMessages.ROOM_NOT_AVAILABLE)
        super(Reservation, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - room: {}  name: {}  from: {}  to: {}".format(
            self.id, self.room.id, self.client_name, self.start_date, self.end_date
        )
