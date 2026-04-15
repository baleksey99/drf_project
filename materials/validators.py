import re
from rest_framework import serializers


def validate_youtube_link(value):
    """
    Валидирует, что ссылка ведёт на YouTube.
    Поддерживает форматы:
    - youtube.com/watch?v=...
    - youtu.be/...
    - youtube.com/embed/...
    """
    youtube_regex = (
        r'(https?://)?'  # протокол (опционально)
        r'(www\.)?'       # www (опционально)
        r'(youtube\.com/watch\?v=|'  # youtube.com/watch?v=
        r'youtu\.be/|'     # youtu.be/
        r'youtube\.com/embed/)'  # youtube.com/embed/
        r'[\w-]{11}'      # ID видео (11 символов)
    )

    if not re.match(youtube_regex, value):
        raise serializers.ValidationError(
            'Разрешены только ссылки на YouTube (youtube.com, youtu.be).'
        )
    return value
