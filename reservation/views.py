from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from reservation import static_values

from .models import House, ListingOwner


class IndexView(TemplateView):
    template_name = "reservation/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["owners"] = ListingOwner.objects.all()
        return context


class OwnerHomeView(TemplateView):
    template_name = "reservation/owner-home.html"

    def get_context_data(self, id, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = ListingOwner.objects.get(pk=id)
        context["owner"] = owner
        context["houses"] = owner.get_houses()
        context["statuses"] = {
            "ALL": static_values.status.GET_RESERVED_ROOM_LIST_ALL,
            "FROME_HERE": static_values.status.GET_RESERVED_ROOM_LIST_FROM_NOW,
        }
        return context


class HouseView(TemplateView):
    template_name = "reservation/house.html"

    def get_context_data(self, id, house_id=None, **kwargs):

        context = super().get_context_data(**kwargs)
        context["errors"] = []
        try:
            owner = ListingOwner.objects.get(pk=id)
            house = House.objects.get(pk=house_id)
        except ListingOwner.DoesNotExist:
            context["errors"] = context["errors"].append(
                static_values.ErroMessages.LISTING_OWNER_DOSE_NOT_EXIST
            )
        except House.DoesNotExist:
            context["errors"] = context["errors"].append(
                static_values.ErroMessages.HOSE_DOSE_NOT_EXIST
            )
            context["owner"] = owner
        else:
            context["owner"] = owner
            context["house"] = house
            context["rooms"] = house.get_rooms()

        return context

    def post(self, request, id, house_id=None, *args, **kwargs):
        errors = []
        messages = []
        print("hoooooooooooy")
        try:
            owner = ListingOwner.objects.get(pk=id)
        except ListingOwner.DoesNotExist:
            print("errrors")
            errors.append(
                static_values.ErroMessages.LISTING_OWNER_DOSE_NOT_EXIST
            )
        else:
            print("else")

            try:
                # If there is house, update it.
                house = House.objects.get(pk=house_id)
                house.name = self.request.POST.get("name", house.name)
                house.address = self.request.POST.get("address", house.address)
                house.save()
                house_id=house.id
                print(house)
                messages.append(static_values.SuccessMessage.SUCCESS_OPERATION)
            except House.DoesNotExist:
                # If there is not any house, create it.
                house = House.objects.create(
                    name=self.request.POST.get("name"),
                    address=self.request.POST.get("address"),
                    owner = owner
                )
                house_id=house.id
                messages.append(static_values.SuccessMessage.SUCCESS_OPERATION)
                return redirect("reservation:owner_house_detail_update",id = owner.id,house_id=house_id)
            else:
                context = self.get_context_data(id, house_id, *args, **kwargs)
                context["errors"] = errors
                context["msgs"] = messages
            
        return self.render_to_response(context)


class ReservedRoomView(TemplateView):
    template_name = "reservation/reserved-room.html"

    def get_context_data(self, id, status, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = ListingOwner.objects.get(pk=id)
        context["owner"] = owner
        context["statuses"] = {
            "ALL": static_values.status.GET_RESERVED_ROOM_LIST_ALL,
            "FROME_HERE": static_values.status.GET_RESERVED_ROOM_LIST_FROM_NOW,
        }

        if status == static_values.status.GET_RESERVED_ROOM_LIST_ALL:
            context["reservations"] = owner.get_all_room_reservation()

        elif status == static_values.status.GET_RESERVED_ROOM_LIST_FROM_NOW:
            context["reservations"] = owner.get_room_reservation_from_now()

        return context


@require_http_methods(["POST"])
def create_house(request):
    print("yoohooooo")
    pass


@require_http_methods(["PUT"])
def update_house(request, house_id):
    pass
