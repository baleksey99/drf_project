import re
from rest_framework import serializers
from django.core.exceptions import ValidationError

def validate_youtube_link(value):
    """
    Проверяет, что URL ведёт на YouTube (youtube.com или youtu.be).
    Поддерживает:
    - https://www.youtube.com/watch?v=...
    - https://youtu.be/...
    - embed-ссылки
    - плейлисты
    """
    youtube_regex = (
        r'^(https?://)?(www\.)?'
        r'(youtube\.com|youtu\.be|youtube-nocookie\.com)/'
        r'(watch\?v=|embed/|v/|shorts/|playlist\?list=|)[^\s]+$'
    )
    if not re.match(youtube_regex, value):
        raise ValidationError('Разрешены только ссылки на YouTube (youtube.com, youtu.be).')
    return value

class YouTubeLinkValidator:
    def __init__(self, field='video_url'):
        self.field = field

    def __call__(self, value):
        if not value:
            return
        try:
            validate_youtube_link(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.message)
