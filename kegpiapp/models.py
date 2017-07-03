from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

import kegpiapp.validators as validators


class FlowSensorModel(models.Model):
    OZ_PER_ML = 0.033814
    POUR_TIMEOUT = 10  # Minimum time between pours in seconds

    pin = models.PositiveIntegerField(validators=[validators.validate_pin])
    volume_per_pulse = models.FloatField(default=0, help_text="Volume in ml per pulse of the sensor",
                                         validators=[MinValueValidator(0)])

    def _pulse(self, channel):
        if hasattr(self, "kegmodel"):
            if not hasattr(self, "reset"):
                self.reset = True
            if not hasattr(self, "last_pour_time"):
                self.last_pour_time = datetime.now()
                return

            if (datetime.now() - self.last_pour_time).total_seconds() >= FlowSensorModel.POUR_TIMEOUT:
                self.reset = True
            else:
                vol = self.volume_per_pulse * FlowSensorModel.OZ_PER_ML

                if self.reset:
                    self.kegmodel.current_pour_volume = 0
                    self.reset = False
                    vol *= 2

                self.kegmodel.current_pour_volume += vol
                self.kegmodel.current_level -= vol

                if self.kegmodel.current_level < 0:
                    self.kegmodel.current_level = 0

                KegModel.objects.filter(pk=self.kegmodel.pk).update(current_level=self.kegmodel.current_level,
                                                                    current_pour_volume=self.kegmodel.current_pour_volume)

            self.last_pour_time = datetime.now()

    def __str__(self):
        return "Flow sensor (pin " + str(self.pin) + ")"


class WeightSensorModel(models.Model):
    pin = models.PositiveIntegerField(unique=True, validators=[validators.validate_pin])
    # pin2 = models.PositiveIntegerField(unique=True)
    pounds_per_volt = models.FloatField(default=0)
    zero_offset = models.FloatField(default=0)

    def _get_raw_reading(self):
        return 0  # TODO

    def get_current_weight(self):
        return (self._get_raw_reading() - self.zero_offset) * self.pounds_per_volt

    def get_current_level(self):
        if not hasattr(self, "kegmodel"):
            return 0

        full_weight = self.kegmodel.full_weight or 0
        empty_weight = self.kegmodel.empty_weight or 0
        beverage_weight = full_weight - empty_weight
        return (self.get_current_weight() - empty_weight) / beverage_weight * self.kegmodel.capacity

    def __str__(self):
        return "Weight sensor (pin " + str(self.pin) + ")"
        #return "Weight sensor (pins " + str(self.pin1) + ", " + str(self.pin2) + ")"


class TemperatureSensorModel(models.Model):
    pin = models.PositiveIntegerField(unique=True, validators=[validators.validate_pin])
    degrees_per_volt = models.FloatField(default=0, help_text="Degrees F per volt of the sensor")
    zero_offset = models.FloatField(default=0, help_text="Sensor reading at 0F")

    def _raw_reading(self):
        return 0  # TODO: get raw sensor reading

    def reading(self):
        return 0  # TODO: this

    def __str__(self):
        return "Temperature sensor (pin " + str(self.pin) + ")"


class BeverageModel(models.Model):
    beverage_type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, default=None, null=True, blank=True)
    brewery = models.CharField(max_length=100, default=None, null=True, blank=True)
    ABV = models.FloatField(help_text="ABV of the beverage in percent", default=0, blank=True,
                            validators=[MinValueValidator(0), MaxValueValidator(100)])
    tasting_notes = models.TextField(default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class TankModel(models.Model):
    TYPE_CHOICES = (
        ("N", "Nitrogen"),
        ("C", "CO2"),
        ("B", "Beer gas"),
    )

    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    sensor = models.ForeignKey(WeightSensorModel, default=None, on_delete=models.SET_DEFAULT, null=True, blank=True)
    capacity = models.FloatField(help_text="Capacity of the tank in l", validators=[MinValueValidator(0)])
    density = models.FloatField(help_text="Density of the gas in kg/l", default=0, blank=True,
                                validators=[MinValueValidator(0)])

    def __str__(self):
        types = dict(TankModel.TYPE_CHOICES)
        return types[self.type] + "(" + str(self.capacity) + "l)"


class KegModel(models.Model):
    CAPACITY_CHOICES = (
        (169, "Mini"),
        (640, "Cornelius"),
        (661, "Sixth barrel"),
        (992, "Quarter barrel"),
        (1984, "Half barrel"),
    )

    beverage = models.ForeignKey(BeverageModel, default=None, on_delete=models.SET_DEFAULT, null=True, blank=True)
    tap = models.PositiveIntegerField(default=None, null=True, blank=True,
                                      validators=[validators.validate_tap_unique])
    capacity = models.PositiveIntegerField(choices=CAPACITY_CHOICES)
    current_level = models.FloatField(default=0, validators=[MinValueValidator(0)])  # TODO: automatically enter full on form page
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,
                                validators=[MinValueValidator(0)])
    sensor = models.OneToOneField(FlowSensorModel, default=None, on_delete=models.SET_DEFAULT, null=True, blank=True)
    fill_date = models.DateField(default=None, null=True, blank=True)
    current_pour_volume = models.FloatField(default=0)

    @property
    def price_per_oz(self):
        if self.capacity == 0:
            return 0
        return float(self.price or 0) / self.capacity

    @property
    def current_pour_cost(self):
        return self.current_pour_volume * self.price_per_oz

    def __str__(self):
        capacities = dict(KegModel.CAPACITY_CHOICES)
        return (capacities[self.capacity] + " keg" if self.capacity in capacities else str(self.capacity) + " oz keg") + \
            " (" + str(self.beverage or "empty") + ", " + ("tap #" + str(self.tap) if self.tap else "untapped") + ")"


sensor_models = (FlowSensorModel, WeightSensorModel, TemperatureSensorModel)

