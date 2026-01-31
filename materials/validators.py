import re
from rest_framework import serializers
from django.core.exceptions import ValidationError

def validate_youtube_link(value):
    youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'
    if not re.match(youtube_regex, value):
        raise ValidationError('Разрешены только ссылки на YouTube (youtube.com, youtu.be).')
    return value

class YouTubeLinkValidator:
    def __init__(self, field='video_url'):
        self.field = field

    def __call__(self, value):
        if not value:
            return
        youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'
        if not re.match(youtube_regex, value):
            raise serializers.ValidationError("Некорректная ссылка на YouTube")
