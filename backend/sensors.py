from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from kegpiapp.models import FlowSensorModel

try:
    import RPi.GPIO as GPIO
    has_gpio = True
except:
    has_gpio = False

if has_gpio:
    GPIO.setmode(GPIO.BCM)


@receiver(post_save, sender=FlowSensorModel)
def flow_sensor_after_save(sender, instance, **kwargs):  # TODO: Init existing sensors on app start
    if has_gpio:
        GPIO.cleanup(instance.pin)
        GPIO.setup(instance.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(instance.pin, GPIO.RISING, callback=instance._pulse)
