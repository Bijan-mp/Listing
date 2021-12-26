from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reservation.api_views import ReservationViewset, RoomViewset, api_root
from reservation.views import (
    HouseView,
    IndexView,
    OwnerHomeView,
    ReservedRoomView,
    create_house,
)

app_name = "reservation"


urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path(
        "<int:id>/",
        include(
            [
                path("", OwnerHomeView.as_view(), name="owner_home"),
                path("house/", HouseView.as_view(), name="owner_create_house"),
                path(
                    "house/<int:house_id>/",
                    HouseView.as_view(),
                    name="owner_house_detail_update",
                ),
                path(
                    "reserved-rooms/<str:status>",
                    ReservedRoomView.as_view(),
                    name="owner_reserved_rooms",
                ),
            ]
        ),
    ),
]

# API endpoints
room_reservation_view = ReservationViewset.as_view({"post": "create"})
available_rooms_view = RoomViewset.as_view({"get": "list"})
urlpatterns += [
    path(
        "api-v1/",
        include(
            [
                path("", api_root, name="api_root"),
                path(
                    "rooms/reservation/",
                    room_reservation_view,
                    name="room_reservation",
                ),
                path(
                    "rooms/available/<str:start_date>/<str:end_date>/",
                    available_rooms_view,
                    name="available_rooms",
                ),
            ]
        ),
    )
]
