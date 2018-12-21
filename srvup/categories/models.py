from django.db import models
from django.db.models import Count
from django.db.models.signals import pre_save
# Create your models here.
from django.urls import reverse

from courses.fields import PositionField
from courses.utils import create_slug
from videos.models import Video


class CategoryQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all(
        ).active().annotate(
            courses_length=Count("secondary_category", distinct=True)
        ).prefetch_related('primary_category', 'secondary_category')


    # prefetch_related('primary_category') below does the same job as this,only thing is this is efficient
    # qs = Category.objects.all()
    # obj = qs.first()
    # courses = obj.course_set.all()


class Category(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True)  # unique = False
    order = PositionField( blank=True)
    video = models.ForeignKey(Video, null=True, blank=True,on_delete=models.CASCADE)
    description = models.TextField()
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CategoryManager()

    def get_absolute_url(self):
        return reverse("category-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


def pre_save_category_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_category_receiver, sender=Category)
