# import required classes
import httplib2
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage
from oauth2client.tools import run

import time
from datetime import date, timedelta
import csv
import pprint
from models import CredentialsModel,Analytics,AllowedPattern

from django.conf import settings
from models import Analytics, ANALYTICS_DELTA_OPTIONS


SITE_ID = getattr(settings,'SITE_ID',1)


# Declare constants and set configuration values

# The file with the OAuth 2.0 Client details for authentication and authorization.
#CLIENT_SECRETS = 'client_secrets.json'

CLIENT_SECRETS=getattr(settings,"CLIENT_SECRETS",'client_secrets.json')
# The file with the OAuth 2.0 Client details for authentication and authorization.
# A file to store the access token TOKEN_FILE_NAME = 'analytics.dat'
#TOKEN_FILE_NAME = getattr(settings,"TOKEN_FILE_NAME",'analytics.dat')

# A helpful message to display if the CLIENT_SECRETS is missing in settings.
MISSING_CLIENT_SECRETS_MESSAGE = 'CLIENT_SECRETS is missing in settings'

# The Flow object to be used if we need to authenticate.
FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
                               scope='https://www.googleapis.com/auth/analytics.readonly',
                               message=MISSING_CLIENT_SECRETS_MESSAGE)

def clean_title(title):
     generic_title=getattr(settings,'GENERIC_TITLE','')
     return title.replace(generic_title,'')

def prepare_credentials():
  # Retrieve existing credendials
  id = CredentialsModel.objects.all()[0].id
  storage = Storage(CredentialsModel, 'id', id, 'credential')
  credentials = storage.get()

  # If existing credentials are invalid and Run Auth flow
  # the run method will store any new credentials
  if credentials is None or credentials.invalid:
    credentials = run(FLOW, storage) #run Auth Flow and store credentials

  return credentials
  
  
def initialize_service():
  # 1. Create an http object
  http = httplib2.Http()

  # 2. Authorize the http object
  # In this tutorial we first try to retrieve stored credentials. If
  # none are found then run the Auth Flow. This is handled by the
  # prepare_credentials() function defined earlier in the tutorial
  credentials = prepare_credentials()
  http = credentials.authorize(http)  # authorize the http object

  # 3. Build the Analytics Service Object with the authorized http object
  return build('analytics', 'v3', http=http)

def get_first_profile_id(service):
  # Get a list of all Google Analytics accounts for this user
  accounts = service.management().accounts().list().execute()

  if accounts.get('items'):
    # Get the first Google Analytics account
    firstAccountId = accounts.get('items')[0].get('id')

    # Get a list of all the Web Properties for the first account
    webproperties = service.management().webproperties().list(accountId=firstAccountId).execute()

    if webproperties.get('items'):
      # Get the first Web Property ID
      firstWebpropertyId = webproperties.get('items')[0].get('id')

      # Get a list of all Views (Profiles) for the first Web Property of the first Account
      profiles = service.management().profiles().list(
          accountId=firstAccountId,
          webPropertyId=firstWebpropertyId).execute()

      if profiles.get('items'):
        # return the first View (Profile) ID
        return profiles.get('items')[0].get('id')

  return None


def get_results_realtime(service,profile_id):
  """ """
  return service.data().realtime().get(
      ids='ga:' + profile_id,
      metrics='rt:activeUsers').execute()


def get_results(service, profile_id):
  # Use the Analytics Service Object to query the Core Reporting API
  """
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='2014-01-01',
      end_date='2014-12-31',
      metrics='ga:users,ga:sessions,ga:pageviews',
      dimensions='ga:socialNetwork,ga:deviceCategory').execute()
  """
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='2015-01-07',
      end_date='2015-01-07',
      metrics='ga:pageviews',
      dimensions='ga:pagePath,ga:pageTitle ',
      sort='-ga:pageviews',
      max_results=20).execute()
  
def get_all_profile_ids(service):
    ids = []
    accounts = service.management().accounts().list().execute()
    time.sleep(1)
    if accounts.get('items'):
        for account in accounts.get('items'):
            account_id = account.get('id')
            webproperties = service.management().webproperties().list(accountId=account_id).execute()
            time.sleep(1)
            if webproperties.get('items'):
                for webproperty in webproperties.get('items'):
                    webproperty_id = webproperty.get('id')
                    profiles = service.management().profiles().list(
                                accountId=account_id,
                                webPropertyId=webproperty_id).execute()
                    time.sleep(1)
                    if profiles.get('items'):
                        for profile in profiles.get('items'):
                            profile_id = profile.get('id')
                            ids.append(profile_id)
    return ids                            
                    

def get_results_by_dates(service, profile_id,start_date,end_date):
  # Use the Analytics Service Object to query the Core Reporting API
  """
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='2014-01-01',
      end_date='2014-12-31',
      metrics='ga:users,ga:sessions,ga:pageviews',
      dimensions='ga:socialNetwork,ga:deviceCategory').execute()
  """
  max_results=getattr(settings,'ANALYTICS_MAX_RESULTS',500)
  return service.data().ga().get(
                                ids='ga:' + profile_id,
                                start_date = start_date,
                                end_date = end_date,
                                metrics ='ga:pageviews',
                                dimensions ='ga:pagePath,ga:pageTitle ',
                                sort ='-ga:pageviews',
                                max_results =max_results).execute()


def parser(start_date,end_date):
    analy = initialize_service()

    #id = get_first_profile_id(analy)
    id = getattr(settings,'ANALYTICS_ID','')
    data = get_results_by_dates(analy,id,start_date,end_date)
    return data


def parse_analytics():
  for delta in ANALYTICS_DELTA_OPTIONS:
     start_date = date.today() - timedelta(days=delta[0])
     end_date=date.today()
     analytics_data =  parser(start_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d'))
     if analytics_data.get('rows',None):
        Analytics.objects.filter(delta=delta[0],site=SITE_ID).delete()       
        pass

     for a_data in analytics_data['rows']:
       try:
          is_valid = AllowedPattern.objects.get(pattern=resolve(a_data[0]).url_name,site=SITE_ID).is_valid and True or False
       except:
          is_valid=False
       try:   
         analytics=  Analytics(title=clean_title(a_data[1]),
                               pageviews=a_data[2],
                               path=a_data[0],
                               start_date=start_date,
                               end_date = end_date,
                               delta=delta[0],
                               is_valid=is_valid,
                               site_id=SITE_ID
                              ) 
         bat = analytics.save()
       except:
         pass #ezin da gorde  


from django.conf import urls
from django.core.urlresolvers import resolve
from elhuyar.urls import urlpatterns


def import_patterns(urlpatterns1):
  AllowedPattern.objects.all().delete()
  for patt in urlpatterns1:
     for patt1 in patt.urlpatterns:
        example = patt1.regex.pattern
        name = patt1.name

        AllowedPattern(name=name,
                       example=example, 
                       )
        AllowedPattern.save()