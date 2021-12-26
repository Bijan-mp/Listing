
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.urls import reverse as django_reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, renderers, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from reservation import static_values
from reservation.models import Reservation, Room
from reservation.serializers import ReservationSerializer, RoomSerializer


class RoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def list(self, request, start_date, end_date):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Check if dates are past.
        if start_date < timezone.now().date() or end_date < timezone.now().date():
            return JsonResponse(
                static_values.ErroMessages.DATES_ARE_PAST,
                status=status.HTTP_400_BAD_REQUEST,
                safe=False,
            )

        if start_date > end_date:
            return JsonResponse(
                static_values.ErroMessages.START_IS_BIGGER_THAN_END,
                status=status.HTTP_400_BAD_REQUEST,
            )

        available_rooms = Room.get_available_room_list(start_date, end_date)
        serializer = RoomSerializer(available_rooms, many=True)
        return Response(serializer.data)


class ReservationViewset(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        start_date = datetime.strptime(request.data.get("start_date"), "%Y-%m-%d")
        end_date = datetime.strptime(request.data.get("end_date"), "%Y-%m-%d")
        # TODO: client must reserve from one day 12pm to another day 12pm

        if start_date > end_date:
            return JsonResponse(
                static_values.ErroMessages.START_IS_BIGGER_THAN_END,
                status=status.HTTP_400_BAD_REQUEST,
                safe=False,
            )

        if start_date.date() < timezone.now().date() or end_date.date() < timezone.now().date():
            return JsonResponse(
                static_values.ErroMessages.DATES_ARE_PAST,
                status=status.HTTP_400_BAD_REQUEST,
                safe=False,
            )

        try:
            room = Room.objects.get(pk=request.data.get("room"))
            if not room.is_available_at(start_date, end_date):
                return JsonResponse(
                    static_values.ErroMessages.ROOM_NOT_AVAILABLE,
                    status=status.HTTP_400_BAD_REQUEST,
                    safe=False,
                )

        except Room.DoesNotExist:
            return JsonResponse(
                static_values.ErroMessages.ROOM_NOT_EXISTING,
                status=status.HTTP_400_BAD_REQUEST,
                safe=False,
            )
        else:
            serializer = ReservationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def api_root(request, format=None):
    today = timezone.now()
    tow_days_later = today + timedelta(days=2)

    start_date = today.strftime("%Y-%m-%d")
    end_date = tow_days_later.strftime("%Y-%m-%d")
    return Response(
        {
            "reserve room [POST]": django_reverse("reservation:room_reservation"),
            "available rooms": reverse(
                "reservation:available_rooms",
                args=[start_date, end_date],
                request=request,
                format=format,
            ),
        }
    )
