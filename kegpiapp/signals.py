from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from kegpiapp.models import FlowSensorModel
from kegpiapp.views import get_state_info

try:
    import RPi.GPIO as GPIO
    has_gpio = True
except:
    has_gpio = False


@receiver(post_save, sender=FlowSensorModel)
def flow_sensor_after_save(sender, instance, **kwargs):
    if has_gpio:
        GPIO.cleanup(instance.pin)
        GPIO.setup(instance.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(instance.pin, GPIO.RISING, callback=instance._pulse)


@receiver(post_save)
def model_after_save(**kwargs):
    get_state_info.ver += 1

if has_gpio:
    GPIO.setmode(GPIO.BCM)
    for s in FlowSensorModel.objects.all():  # TODO: init weight sensors
        flow_sensor_after_save(None, s)
