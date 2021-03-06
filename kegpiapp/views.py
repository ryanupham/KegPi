from django.contrib import messages
from django.forms.models import modelform_factory
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse

from kegpiapp.models import FlowSensorModel, BeverageModel, KegModel, TankModel


def view_main(request):
    return render(request, "dashboard.html")


def _edit(request, redirect, form_factory, cls, model=None, custom_js=None):
    form = form_factory(instance=model) if model else form_factory()

    if request.method == "POST":
        form = form_factory(request.POST)

        old = None
        if "old-id" in request.POST:
            old = cls.objects.get(pk=request.POST["old-id"])
            old.delete(keep_parents=True)  # TODO: fix this bug

        if form.is_valid():
            form.save()

            messages.add_message(request, messages.SUCCESS,
                                 "Successfully added" if old is None else "Successfully edited")
            return HttpResponseRedirect(reverse(redirect))
        elif old:
            old.id = request.POST["old-id"]
            old.save()

    return render(request, "editForm.html", {"form": form, "id": model.id if model else None, "custom_js": custom_js})


def _remove(request, redirect, pk, cls):
    if pk:
        cls.objects.get(pk=pk).delete()
        messages.add_message(request, messages.SUCCESS, "Successfully removed")

    return HttpResponseRedirect(reverse(redirect))


def _view_items(request, objects, title, new_url, edit_url, remove_url, custom_js=None):
    context = {
        "objs": objects,
        "title": title,
        "new_url": new_url,
        "edit_url": edit_url,
        "remove_url": remove_url,
        "custom_js": custom_js,
    }

    return render(request, "viewItems.html", context)


def edit_beverage(request, pk=None):
    form_factory = modelform_factory(BeverageModel, exclude=())
    model = get_object_or_404(BeverageModel, pk=pk) if pk else None

    return _edit(request, "view beverages", form_factory, BeverageModel, model)


def edit_keg(request, pk=None):
    form_factory = modelform_factory(KegModel, exclude=("last_pour_volume", "last_pour_time", "current_pour_volume"))
    model = get_object_or_404(KegModel, pk=pk) if pk else None

    return _edit(request, "view kegs", form_factory, KegModel, model, "js/kegmodel_edit.js")


def edit_gas(request, pk=None):
    form_factory = modelform_factory(TankModel, exclude=())
    model = get_object_or_404(TankModel, pk=pk) if pk else None

    return _edit(request, "view gas tanks", form_factory, TankModel, model)


def edit_sensor(request, pk=None):
    form_factory = modelform_factory(FlowSensorModel, exclude=())
    model = get_object_or_404(FlowSensorModel, pk=pk) if pk else None

    return _edit(request, "view sensors", form_factory, FlowSensorModel, model)


def remove_beverage(request, pk):
    return _remove(request, "view beverages", pk, BeverageModel)


def remove_keg(request, pk):
    return _remove(request, "view kegs", pk, KegModel)


def remove_gas(request, pk):
    return _remove(request, "view gas tanks", pk, TankModel)


def remove_sensor(request, pk):
    return _remove(request, "view sensors", pk, FlowSensorModel)


def view_beverages(request):
    return _view_items(request, BeverageModel.objects.all(), "Beverages", "new beverage", "edit beverage",
                       "remove beverage")


def view_kegs(request):
    kegs = list(KegModel.objects.filter(tap__gt=0).order_by("tap")) + list(KegModel.objects.exclude(tap__gt=0))
    return _view_items(request, kegs, "Kegs", "new keg", "edit keg", "remove keg")


def view_gas(request):
    return _view_items(request, TankModel.objects.all(), "Gas Tanks", "new gas tank", "edit gas tank",
                       "remove gas tank")


def view_sensors(request):
    return _view_items(request, FlowSensorModel.objects.all(), "Sensors", "new sensor", "edit sensor",
                       "remove sensor")


def get_state_info(request):
    response = {
        "kegs": {
            keg.pk: {
                "level": keg.current_level if keg.sensor else 0,
                "currentPour": "${0:.2f}".format(keg.current_pour_cost),
            } for keg in KegModel.objects.all()
        },
        "gas": {
            gas.pk: {
                "level": gas.current_level if gas.sensor else 0,
            } for gas in TankModel.objects.all()
        },
        "ver": get_state_info.ver
    }

    return JsonResponse(response)
get_state_info.ver = 0


def get_keg_block(request):
    context = {
        "kegs": sorted([k for k in KegModel.objects.all() if k.tap], key=lambda k: k.tap),
        "gas_tanks": TankModel.objects.all(),
    }

    return render(request, "dashboard-data.html", context)
