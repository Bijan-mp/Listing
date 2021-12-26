
from rest_framework import serializers

from .models import House, Reservation, Room


class HouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = House
        exclude = ["owner"]


class RoomSerializer(serializers.ModelSerializer):
    
    house = HouseSerializer(many=False, read_only=True)
    class Meta:
        model = Room
        fields = "__all__"
        read_only_fields = ('number',)


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['room', 'start_date', 'end_date', 'client_name']
