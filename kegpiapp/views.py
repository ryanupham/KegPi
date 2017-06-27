from django.contrib import messages
from django.forms.models import modelform_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse

from kegpiapp.forms import KegForm
from kegpiapp.models import CapacitySensorModel, BeverageModel, KegModel


def view_main(request):
    context = {
        "kegs": sorted([k for k in KegModel.objects.all() if k.tap], key=lambda k: k.tap),
    }

    return render(request, "dashboard.html", context)


def _edit(request, redirect, form_factory, cls, model=None):
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

    return render(request, "editForm.html", {"form": form, "id": model.id if model else None})


def _remove(request, redirect, pk, cls):
    if pk:
        cls.objects.get(pk=pk).delete()
        messages.add_message(request, messages.SUCCESS, "Successfully removed")

    return HttpResponseRedirect(reverse(redirect))


def _view_items(request, objects, title, new_url, edit_url, remove_url):
    context = {
        "objs": objects,
        "title": title,
        "new_url": new_url,
        "edit_url": edit_url,
        "remove_url": remove_url,
    }

    return render(request, "viewItems.html", context)


def edit_beverage(request, pk=None):
    form_factory = modelform_factory(BeverageModel, exclude=())
    model = BeverageModel.objects.get(pk=pk) if pk else None

    return _edit(request, "view beverages", form_factory, BeverageModel, model)


def edit_keg(request, pk=None):
    model = KegModel.objects.get(pk=pk) if pk else None

    return _edit(request, "view kegs", KegForm, KegModel, model)


def edit_sensor(request, pk=None):
    form_factory = modelform_factory(CapacitySensorModel, exclude=("kg_per_volt", "zero_offset"))
    model = CapacitySensorModel.objects.get(pk=pk) if pk else None  # TODO: check if valid pk

    return _edit(request, "view sensors", form_factory, CapacitySensorModel, model)


def remove_beverage(request, pk):
    return _remove(request, "view beverages", pk, BeverageModel)


def remove_keg(request, pk):
    return _remove(request, "view kegs", pk, KegModel)


def remove_sensor(request, pk):
    return _remove(request, "view sensors", pk, CapacitySensorModel)


def view_beverages(request):
    return _view_items(request, BeverageModel.objects.all(), "Beverages", "new beverage", "edit beverage",
                       "remove beverage")


def view_kegs(request):
    return _view_items(request, KegModel.objects.all(), "Kegs", "new keg", "edit keg", "remove keg")


def view_sensors(request):
    return _view_items(request, CapacitySensorModel.objects.all(), "Sensors", "new sensor", "edit sensor",
                       "remove sensor")