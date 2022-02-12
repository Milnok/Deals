from rest_framework import serializers

from .models import Customer, Gems


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class GemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gems
        fields = ('gem',)


class CustomerSerializer(serializers.ModelSerializer):
    gems = serializers.StringRelatedField(source="get_gems", many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ('username', 'spent_money', 'gems')
