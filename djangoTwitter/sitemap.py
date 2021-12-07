from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Publication, User, Profile
class StaticSitemap(Sitemap):

    def items(self):
        priority = 0.8
        changefreq = 'monthly'
        protocol = 'https'
        return [
            'mirtoch:terms',
            'mirtoch:about',
            'mirtoch:home',
            'mirtoch:publications',
        ]

    def location(self, item):
        return reverse(item)

class PublicationSitemap(Sitemap):
    def items(self):
        return Publication.objects.all()
    def location(self, item):
        return '/publications/%s'%item.slug


# class ProfileSitemap(Sitemap):
#     def items(self):
#         return Profile.objects.all()

#     def location(self, item):
#         return reverse('mirtoch:profiles', args=[item.user_name])


