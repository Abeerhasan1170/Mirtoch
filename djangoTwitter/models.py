from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
import os
from tinymce.models import HTMLField
import requests
from requests_oauthlib import OAuth1
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.template.loader import render_to_string

auth = OAuth1(os.environ.get('API_KEY'), os.environ.get('SECRET_KEY'),
              os.environ.get('ACCESS_TOKEN'), os.environ.get('ACCESS_TOKEN_SECRET'))


class Country(models.Model):
    country_code = models.CharField(default='', max_length=4, primary_key=True)
    name = models.CharField(max_length=250, default='')
    list_id = models.CharField(max_length=250, default='')
    total_cases = models.CharField(max_length=250, default='0')
    new_cases = models.CharField(max_length=250, default='0')
    total_deaths = models.CharField(max_length=250, default='0')
    total_recovered = models.CharField(max_length=250, default='0')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_country = models.ForeignKey(Country,
                                        related_name='default_Country',
                                        to_field='country_code',
                                        on_delete=models.CASCADE,
                                        blank=True, null=True)
    is_verified = models.BooleanField('verified', default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Profile(models.Model):
    profile_category = [
        ('G', 'Government'),
        ('M', 'Media'),
        ('P', 'Business'),
        ('A', 'Active'),
        ('O', 'PoliticalParty'),
    ]
    associated_country = models.ForeignKey(Country,
                                           related_name='user_country',
                                           on_delete=models.CASCADE,
                                           blank=True, null=True)
    user_name = models.CharField(max_length=50)
    category = models.CharField(
        max_length=2, choices=profile_category, default='P')
    position = models.CharField(max_length=500, null=True, blank=True)
    facebook = models.CharField(
        max_length=500, blank=True, default='https://www.facebook.com/')
    twitter = models.CharField(
        max_length=500, blank=True, default="https://www.twitter.com/")
    website = models.CharField(
        max_length=500, blank=True, default='N/A')

    def __str__(self):
        return self.user_name


class Usernames(models.Model):
    username = models.CharField(max_length=50)


@receiver(post_save, sender=Profile)
def addToList(sender, instance, *args, **kwargs):
    if kwargs['created']:
        print(instance.associated_country.list_id)
        url = f"https://api.twitter.com/1.1/lists/members/create.json?list_id={instance.associated_country.list_id}&screen_name={instance.user_name}"
        requests.post(url, auth=auth)


@receiver(post_delete, sender=Profile)
def deleteFromList(sender, instance, *args, **kwargs):
    screen_name = instance.user_name
    url = f"https://api.twitter.com/1.1/lists/members/destroy.json?screen_name={screen_name}&list_id={instance.associated_country.list_id}"
    requests.post(url, auth=auth)


class About(models.Model):
    content = HTMLField()

    def __str__(self):
        return self.content


class Publication(models.Model):
    title = models.CharField(max_length=250, default='')
    content = HTMLField()
    slug = models.SlugField(max_length=1000, default='',
                            editable=False, null=True,
                            blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.slug

    def generate_slug(self):
        """generating a slug for the title of the publication
            eg: this-is-an-project"""
        slug = slugify(self.title)
        new_slug = slug
        s = 1
        while Publication.objects.filter(slug=new_slug).exists():
            """increase value of slug by one"""
            new_slug = f'{slug}-{s}'
            s += 1
        return new_slug

    def save(self, *args, **kwargs):
        """create a publication and save to the database"""
        if not self.slug:
            self.slug = self.generate_slug()
        super(Publication, self).save(*args, **kwargs)


def update_slug(sender, instance, signal, **kwargs):
    '''Signal to update an project's slug once title is updated'''
    if kwargs.get('updated', True):
        publication = Publication.objects.filter(slug=instance.pk)
        new_slug = slugify(instance.title)
        publication.update(
            slug=new_slug
        )


@receiver(post_save, sender=Publication)
def send_notifications_to_all_users(sender,
                                    instance,
                                    created, *args, **kwargs):
    """
        sender {[type]} -- [Instance of ]
        created {[type]} -- [If the article is posted.]
    """
    if instance and created:
        users = User.objects.filter(is_active=True)
        for user in users:
            sender = os.getenv('EMAIL_HOST_USER')
            email = user.email
            email_subject = "Mirtoch - A new Publication has been made"
            message = render_to_string('djangoTwitter/create_publication.html', {
                'title': email_subject,
                'username': user.username,
                'title': instance.title,
                'content': instance.content
            })

            send_mail(email_subject, '', sender, [
                email, ], html_message=message)
            notify.send(instance, recipient=user,
                        verb=instance.title,
                        action_object=instance)


class Volunteer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    comment = models.TextField()

    def __str__(self):
        return self.first_name


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comment_user',
                             on_delete=models.CASCADE,
                             blank=True, null=True)
    content = HTMLField()
    publication = models.ForeignKey(Publication, related_name='publication',
                                    on_delete=models.CASCADE,
                                    blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
