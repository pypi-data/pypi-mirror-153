from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site
from django.shortcuts import render
import httplib2
from apiclient.discovery import build
from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_util.storage import DjangoORMStorage as Storage
from csgoogleanalytics.models import CredentialsModel, AnalyticsProfile
from oauth2client.client import OAuth2WebServerFlow

def get_flow(request):
    client_id = getattr(settings,'GOOGLE_OAUTH2_CLIENT_ID', '')
    client_secret = getattr(settings,'GOOGLE_OAUTH2_CLIENT_SECRET', '')
    scope = 'https://www.googleapis.com/auth/analytics.readonly'
    redirect_uri = '{0}'.format(request.build_absolute_uri(reverse('auth_return')))
    access_type = 'offline'
    flow = OAuth2WebServerFlow(client_id = client_id,
                           client_secret= client_secret,
                           scope = scope,
                           redirect_uri = redirect_uri,
                           access_type = access_type)
    return flow


@login_required
def set_google(request):
    FLOW = get_flow(request)
    FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,request.user.pk)
    authorize_url = FLOW.step1_get_authorize_url()
    return HttpResponseRedirect(authorize_url)
       

@login_required
def auth_return(request):
    FLOW = get_flow(request)
    if not xsrfutil.validate_token(settings.SECRET_KEY, str(request.GET['state']),request.user.pk):
        return  HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.GET)
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)   
    return HttpResponseRedirect(reverse('select_property'))

@login_required
def select_property(request):
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    http = httplib2.Http()
    http = credential.authorize(http)
    analytics = build('analytics', 'v3', http=http)
    profiles = analytics.management().profiles().list(accountId='~all', webPropertyId='~all').execute()
    items = profiles.get('items', [])
    return render(request, 'csgoogleanalytics/select_analytics_property.html',
                  context=locals())

@login_required
def set_property(request, track_id):
    site = Site.objects.get(id=settings.SITE_ID)
    credentialmodel = CredentialsModel.objects.get(id=request.user)
    if AnalyticsProfile.objects.filter(site=site).exists():
        profile = AnalyticsProfile.objects.get(site=site)
        profile.delete()
    AnalyticsProfile.objects.create(tracking_code=track_id,
                                    credentials=credentialmodel,
                                    site=site)
    return HttpResponseRedirect(reverse('admin:csgoogleanalytics_analytics_changelist'))
