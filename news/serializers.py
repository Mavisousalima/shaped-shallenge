from rest_framework import serializers
from news.models import News, TemporaryLink

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class TemporaryLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryLink
        fields = '__all__'