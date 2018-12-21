from django.db import models

# Create your models here.
from django.db.models import Q
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify
from courses.utils import create_slug


class VideoQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def unused(self):
        return self.filter(Q(lecture__isnull=True) & Q(category__isnull=True))


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()


class Video(models.Model):
    title = models.CharField(max_length=120, default='YouTube Video')
    slug = models.SlugField(blank=True, max_length=100)
    embed_code = models.TextField()
    free = models.BooleanField(default=True)
    member_required = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)  # last saved
    timestamp = models.DateTimeField(auto_now_add=True)  # time added

    objects = VideoManager()

    def __str__(self):  # __unicode__
        return self.title

    def get_absolute_url(self):
        return reverse("video-detail", kwargs={"slug": self.slug})


def pre_save_video_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        # instance.slug = slugify(instance.title)
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_video_receiver, sender=Video)
