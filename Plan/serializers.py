from rest_framework import serializers


class WorkVolumeRequestSerializer(serializers.Serializer):
    factory = serializers.IntegerField()
    start = serializers.DateField()
    finish = serializers.DateField()
    weight = serializers.IntegerField(min_value=0, max_value=2147483647)
    author = serializers.IntegerField()




class ErrorSerializer(serializers.Serializer):
    errorCode = serializers.IntegerField()