from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from kegpiapp import models


def validate_pin(value):
    VALID_PINS = range(2, 27 + 1)
    if value not in VALID_PINS:
        raise ValidationError(_("%(value)s is not in valid pin range (2-27)"), params={"value": value})

    used_pins = []
    for model in models.sensor_models:
        used_pins.extend(model.objects.values_list("pin", flat=True))

    if value in used_pins:
        raise ValidationError(_("Pin #%(value)s has already been used"), params={"value": value})


def validate_tap_unique(value):
    if not (value == 0 or value is None):
        used_taps = models.KegModel.objects.values_list("tap", flat=True)
        if value in used_taps:
            raise ValidationError("Tap #%(value)s has already been used", params={"value": value})
