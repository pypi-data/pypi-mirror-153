# -*- coding: utf-8 -*-
from oauth2client.contrib.django_util.models import CredentialsField

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from datetime import timedelta
from django.contrib.sites.managers import CurrentSiteManager


class Analytics(models.Model):
    title = models.CharField(max_length=255)
    pageviews = models.IntegerField(default=0)
    path = models.CharField(max_length=255, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=False)
    photo_src = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.IntegerField(blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)
    site = models.ForeignKey(Site)

    objects = models.Manager()
    siteobjects = CurrentSiteManager()

    def get_object(self):
        ct = ContentType.objects.get_for_id(self.content_type)
        try:
            return ct.get_object_for_this_type(pk=self.object_id)
        except:
            return None

    def __unicode__(self):
        return self.title


class AnalyticsProfile(models.Model):
    tracking_code = models.CharField(max_length=32, unique=True)
    credentials = models.ForeignKey("CredentialsModel")
    site = models.ForeignKey(Site)

    objects = models.Manager()
    siteobjects = CurrentSiteManager()


class CredentialsModel(models.Model):
    id = models.ForeignKey(settings.AUTH_USER_MODEL, primary_key=True)
    credential = CredentialsField()
    site = models.ForeignKey(Site)

    objects = models.Manager()
    siteobjects = CurrentSiteManager()

    def is_valid(self):
        try:
            if self.credential.invalid:
                return False
            else:
                return True
        except:
            return False

    is_valid.boolean = True

    def has_refresh_token(self):
        if self.credential.refresh_token:
            return True
        else:
            return False

    has_refresh_token.boolean = True

    def save(self, *args, **kwargs):
        if not hasattr(self, 'site') or self.site is None:
            self.site = Site.objects.get(id=settings.SITE_ID)
        super(CredentialsModel, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.id.id)


class AllowedPattern(models.Model):
    name = models.CharField(max_length=255)
    pattern = models.CharField(max_length=255)
    is_valid = models.BooleanField(default=False)


PERIOD_CHOICES_FULL = {
    0: ("1d", timedelta(days=0)),
    1: ("2d", timedelta(days=1)),
    2: ("1w", timedelta(days=7)),
    3: ("2w", timedelta(days=14)),
    4: ("1m", timedelta(days=30)),
    5: ("2m", timedelta(days=60)),
    6: ("1y", timedelta(days=365)),
    7: ("2y", timedelta(days=730)),
    8: ("5y", timedelta(days=1825)),
    9: ("10y", timedelta(days=3650)),
    10: ("20y", timedelta(days=7300)),
}

PERIOD_CHOICES = [(key, value[0]) for key, value in PERIOD_CHOICES_FULL.items()]


class Page(models.Model):
    """ """

    pagepath = models.CharField(max_length=255)
    content_type = models.IntegerField()
    object_id = models.IntegerField()

    added_at = models.DateField()
    added_day = models.IntegerField(default=0)
    added_week = models.IntegerField(default=0)
    added_month = models.IntegerField(default=0)
    added_year = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.added_at:
            self.added_at = self.created_at.date()

        self.added_day = int(self.added_at.strftime("%Y%m%d"))
        self.added_week = int(self.added_at.strftime("%Y%02W"))
        self.added_month = int(self.added_at.strftime("%Y%m"))
        self.added_year = self.added_at.year
        super(Page, self).save(*args, **kwargs)

    def get_object(self):
        ct = ContentType.objects.get_for_id(self.content_type)
        try:
            return ct.get_object_for_this_type(pk=self.object_id)
        except:
            return None

    def __unicode__(self):
        return self.pagepath


class PageStats(models.Model):
    """ """

    page = models.ForeignKey(Page)
    period = models.SmallIntegerField(choices=PERIOD_CHOICES)
    pageviews = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.page.pagepath
