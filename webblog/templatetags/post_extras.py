from webblog.models import *
from django import template

register = template.Library()

def likes(blogpost):
    return len(blogpost.likes.all())

register.filter('likes', likes)

