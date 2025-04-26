import os
from django import template

register = template.Library()

@register.filter
def is_video(file_url):
    """
    Check if the file URL is a video file based on the extension
    """
    video_extensions = ['.mp4', '.mov', '.avi', '.wmv', '.mkv', '.webm']
    ext = os.path.splitext(file_url)[1].lower() if file_url else ''
    return ext in video_extensions

@register.filter
def file_extension(file_url):
    """
    Get the file extension from a URL
    """
    return os.path.splitext(file_url)[1].lower()[1:] if file_url else '' 