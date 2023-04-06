from rest_framework import serializers
from .models import Acticle


class ActicleSerial(serializers.ModelSerializer):
    class Meta:
        model = Acticle
        # fields = ['id', 'title', 'author']
        fields = '__all__'

