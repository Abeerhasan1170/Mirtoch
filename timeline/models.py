from django.db import models
from tinymce.models import HTMLField
from django.urls import reverse
from datetime import datetime
from django.template.defaultfilters import slugify


# Create your models here.
class Title(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('posts_in_category', kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        if self.title:
            self.title = self.title.capitalize()
            self.slug = slugify(self.title)

        super(Title, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Content(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    TimelineTitle = models.CharField(max_length=50)
    content = HTMLField()
    created = models.DateField(default=datetime.now)

    def __str__(self):
        return self.TimelineTitle
