Instalation
-----------


Setup
-----

- Create google secrets

  Acces to th "API Access pane":https://code.google.com/apis/console#:access and create a project
  Create credentials inside the project (OAuth Client Id)
  Select Web Application
- Activate analytics api for the project
- Add csgoogleanalytics and django_object_actions to your installed apps
- Add csgoogleanalytics to your urls
  url(r'^analytics/', include(csgoogleanalytics.urls))
- run migrate
- Add allowed return path to the credentials created previously
    example
    http://localhost:8000/analytics/auth_return
- Set your url validator import path in settings CSGOOGLEANALYTICS_URL_VALIDATOR
   This function gets a path from analytics and must return a tuple with theese elements:
   (is_valid(bool), title(str), photo_src(str), content_type(int), content_id(int))
requirements
------------

Django > 1.5