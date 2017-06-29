from django.db import models


class FlowSensorModel(models.Model):
    def _pulse(self):
        if hasattr(self, "kegmodel"):
            self.kegmodel.current_level -= self.volume_per_pulse

            if self.kegmodel.current_level < 0:
                self.kegmodel.current_level = 0

    pin = models.PositiveIntegerField(unique=True)
    volume_per_pulse = models.FloatField(default=0, help_text="Volume in ml per pulse of the sensor", blank=True)

    def __str__(self):
        return "Flow sensor (pin " + str(self.pin) + ")"


class TemperatureSensorModel(models.Model):
    pin = models.PositiveIntegerField(unique=True)
    degrees_per_volt = models.FloatField(default=0, help_text="Degrees F per volt of the sensor")
    zero_offset = models.FloatField(default=0, help_text="Sensor reading at 0F")

    def _raw_reading(self):
        return 0  # TODO: get raw sensor reading

    def reading(self):
        return 0  # TODO: this


class BeverageModel(models.Model):
    beverage_type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, default=None, null=True, blank=True)
    brewery = models.CharField(max_length=100, default=None, null=True, blank=True)
    ABV = models.FloatField(help_text="ABV of the beverage in percent", default=0, blank=True)
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
    sensor = models.ForeignKey(FlowSensorModel, default=None, on_delete=models.SET_DEFAULT, null=True, blank=True)
    capacity = models.FloatField(help_text="Capacity of the tank in l")
    density = models.FloatField(help_text="Density of the gas in kg/l", default=0, blank=True)


class KegModel(models.Model):
    CAPACITY_CHOICES = (
        (169, "Mini"),
        (640, "Cornelius"),
        (661, "Sixth barrel"),
        (992, "Quarter barrel"),
        (1984, "Half barrel"),
    )

    beverage = models.ForeignKey(BeverageModel, default=None, on_delete=models.SET_DEFAULT, null=True, blank=True)
    fill_date = models.DateField(default=None, null=True, blank=True)
    capacity = models.PositiveIntegerField(choices=CAPACITY_CHOICES)
    current_level = models.FloatField(default=0)
    sensor = models.OneToOneField(FlowSensorModel, default=None, on_delete=models.SET_DEFAULT, null=True, blank=True)
    density = models.FloatField(help_text="Density of the beverage in kg/l", default=0, blank=True)
    tap = models.PositiveIntegerField(unique=True, default=None, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # maybe should be per beverage?

    @property
    def price_per_oz(self):
        return float(self.price) / self.capacity

    @property
    def last_pour(self):
        return 0  # TODO: implement

    def __str__(self):
        capacities = dict(KegModel.CAPACITY_CHOICES)
        return capacities[self.capacity] + " keg" if self.capacity in capacities else str(self.capacity) + " oz keg"


class SettingsModel(models.Model):
    number_of_taps = models.PositiveIntegerField(default=1)
    temperature = models.ForeignKey(FlowSensorModel, default=None, on_delete=models.SET_DEFAULT, null=True,
                                    blank=True)


class HistoryModel(models.Model):
    pass
