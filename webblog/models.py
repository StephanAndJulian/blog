from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, related_name="%(class)s_author")
    content = models.CharField(max_length=10000)
    publication_date = models.DateTimeField()
    likes = models.ManyToManyField(User, related_name="%(class)s_likes")


    class Meta:
        abstract = True
        ordering = ['-publication_date']



class Blogpost(Post):
    title = models.CharField(max_length=1000)
    tags = models.CharField(max_length=500)


class Comment(Post):
    blogpost = models.ForeignKey(Blogpost)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birthday = models.DateField()
    gender = models.SmallIntegerField(max_length=1);
