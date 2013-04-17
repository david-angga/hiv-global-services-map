import os
import cgi
import urllib2

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import images

TEMPLATE_VALS = {
    'service_options': [{ 'value': 'hiv_ct',
                          'display_name': 'HIV counselling and testing' },
                        { 'value': 'opp',
                          'display_name': 'Opportunistic infections: prevention and treatment' },
                        { 'value': 'tb',
                          'display_name': 'Tuberculosis detection, prevention and treatment' },
                        { 'value': 'sti',
                          'display_name': 'STI (sexually transmitted infections): diagnosis and treatment' },
                        { 'value': 'palliative',
                          'display_name': 'Palliative care: treatment of pain and other symptoms, psychosocial and spiritual support and end-of-life care' },
                        { 'value': 'hiv_ct',
                          'display_name': 'HIV counselling and testing' },
                        { 'value': 'art_plain',
                                  'display_name': 'ART (antiretroviral therapy)' },
                        { 'value': 'art_adhere',
                          'display_name': 'ART (antiretroviral therapy) adherence: counselling and support' },
                        { 'value': 'prevention_risk',
                          'display_name': 'Prevention services for those most at risk including people who use drugs, sex workers, MSM (men who have sex with men), prisoners, migrants and youth' },
                        { 'value': 'prevention_discord',
                          'display_name': 'HIV prevention and reproductive health services for PLHIV and discordant couples' },
                        { 'value': 'pmtct',
                          'display_name': 'PMTCT (preventing mother to child transmission) and health services for HIV-positive mothers and infants' },
                                { 'value': 'plhiv',
                                  'display_name': 'PLHIV (people living with HIV) support groups' },
                        { 'value': 'daily',
                          'display_name': 'Nutritional and daily living support' },
                        { 'value': 'pschyosocial',
                          'display_name': 'Psychosocial support: support groups and counselling' },
                        { 'value': 'orphans',
                          'display_name': 'Orphans and vulnerable children: care, support and protection' },
                        { 'value': 'comprehensive_hs',
                          'display_name': 'Comprehensive HIV Services'}
                        ],
    'description_options': [{ 'value': 'public_clinic',
                              'display_name': 'Public clinic' },
                            { 'value': 'private_clinic',
                              'display_name': 'Private clinic' },
                            { 'value': 'gov_hospital',
                                      'display_name': 'Government hospital' },
                            { 'value': 'private_hospital',
                              'display_name': 'Private hospital' },
                            { 'value': 'ngo',
                              'display_name': 'Non-government organisation' },
                            { 'value': 'commercial',
                              'display_name': 'Commercial enterprise/venue' },
                            { 'value': 'support_group',
                              'display_name': 'Support group' },
                            { 'value': 'comm_centre',
                              'display_name': 'Community centre' },
                            { 'value': 'office',
                              'display_name': 'Office' },
                            ],
    'group_options': [{ 'value': 'gen_pop',
                        'display_name': 'General Population' },
                      { 'value': 'live_hiv',
                        'display_name': 'People living with HIV' },
                      { 'value': 'women',
                        'display_name': 'Women' },
                      { 'value': 'lgbt_comm',
                        'display_name': ('Lesbian, gay, bisexual and transgender community') },
                      { 'value': 'msm',
                        'display_name': 'Men who have sex with men' },
                      { 'value': 'sex_workers',
                        'display_name': 'Sex workers' },
                      { 'value': 'drugs',
                        'display_name': 'People who use drugs' },
                      { 'value': 'migrants',
                        'display_name': 'Migrants' },
                      { 'value': 'children',
                        'display_name': 'Children (below 18 years)' },
                      { 'value': 'young',
                        'display_name': 'Young people' },
                      { 'value': 'prisoners',
                        'display_name': 'Prisoners or people in detention' },
                      { 'value': 'all_people',
                        'display_name': 'All people most-at-risk of HIV'}
                      ],
    }


class LocationEntry(db.Model):
    facility_desc = db.StringProperty()
    facility_name = db.StringProperty()
    primary_group = db.StringProperty()
    primary_service = db.StringProperty()

    add1 = db.StringProperty()
    add2 = db.StringProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    country = db.StringProperty()
    postal = db.StringProperty()
    telephone = db.StringProperty()
    website = db.StringProperty()

    manager_employee = db.StringProperty()
    contact_name = db.StringProperty()
    contact_email = db.StringProperty()
    contact_phone = db.StringProperty()
    feedback = db.StringProperty(multiline=True)

    photo = db.BlobProperty()

    latitude = db.StringProperty()
    longitude = db.StringProperty()

    user_name = db.StringProperty()
    entry_date = db.DateTimeProperty(auto_now_add=True)


class LocationEntryHandler(webapp.RequestHandler):
    def post(self):
        location = LocationEntry()
        if users.get_current_user():
            location.user_name = users.get_current_user().email()

        location.facility_desc = self.request.get('facility_desc')
        location.facility_name = self.request.get('facility_name')
        location.primary_group = self.request.get('primary_group')
        location.primary_service = self.request.get('primary_service')

        location.add1 = self.request.get('add1')
        location.add2 = self.request.get('add2')
        location.city = self.request.get('city')
        location.state = self.request.get('state')
        location.country = self.request.get('country')
        location.postal = self.request.get('postal')
        location.telephone = self.request.get('telephone')
        location.website = self.request.get('website')

        location.manager_employee = self.request.get('manager_employee')
        location.contact_name = self.request.get('contact_name')
        location.contact_email = self.request.get('contact_email')
        location.contact_phone = self.request.get('contact_phone')
        location.feedback = self.request.get('feedback')

        location.latitude = self.request.get('latitude')
        location.longitude = self.request.get('longitude')

        if self.request.get('photo'):
            location.photo = db.Blob(images.resize(self.request.get('photo'), 500, 500))

        if self.request.get('image_url'):
            img = urllib2.urlopen(self.request.get('image_url')).read()
            location.photo = db.Blob(images.resize(img), 500, 500)

        location.put()
        self.redirect('/4')

class MainPage(webapp.RequestHandler):
    def get(self):
        locations = LocationEntry.all()
        TEMPLATE_VALS.update ({
          'locations': locations,
        })
        path = os.path.join(os.path.dirname(__file__), 'landing_page.html')
        self.response.out.write(template.render(path, TEMPLATE_VALS))

# Initial screening page for facility locations.
class PageOne(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'hiv.html')
        self.response.out.write(template.render(path, TEMPLATE_VALS))

# Page to enter facility type information and services offered.
class PageTwo(webapp.RequestHandler):
    def get(self):
        self.redirect('/1')
    def post(self):
        path = os.path.join(os.path.dirname(__file__), 'hiv2.html')
        # Create a map here of everything in POST and have an array of KV pairs.
        self.response.out.write(template.render(path, TEMPLATE_VALS))

# Address and contact information.
class PageThree(webapp.RequestHandler):
    def get(self):
        self.redirect('/1')
    def post(self):
        path = os.path.join(os.path.dirname(__file__), 'hiv3.html')
        TEMPLATE_VALS.update({
                'hidden_options': [ { 'name': 'primary_group',
                                      'value': cgi.escape(self.request.get('primary_group')) },
                                    { 'name': 'facility_desc',
                                      'value': cgi.escape(self.request.get('facility_desc')) },
                                    { 'name': 'facility_name',
                                      'value': cgi.escape(self.request.get('facility_name')) },
                                    { 'name': 'primary_service',
                                      'value': cgi.escape(self.request.get('primary_service')) },
                                    ] })
        self.response.out.write(template.render(path, TEMPLATE_VALS))

# Confirmation page for data submission.
class PageFour(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'hiv4.html')
        self.response.out.write(template.render(path, TEMPLATE_VALS))

# Kiosk-style display page for all facility locations.
class KioskPage(webapp.RequestHandler):
    def get(self):
        locations = LocationEntry.all()
        TEMPLATE_VALS.update ({
          'locations': locations,
        })
        path = os.path.join(os.path.dirname(__file__), 'kiosk.html')
        self.response.out.write(template.render(path, TEMPLATE_VALS))        

class CallbackPicup(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'callback_picup.html')
        self.response.out.write(template.render(path, TEMPLATE_VALS))
        
class Image(webapp.RequestHandler):
    def get(self):
        location = db.get(self.request.get("img_id"))
        if location.photo:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(location.photo)
        else:
            self.response.out.write("No Image")

application = webapp.WSGIApplication([
  ('/index_ori', MainPage),
  ('/1', PageOne),
  ('/2', PageTwo),
  ('/3', PageThree),
  ('/4', PageFour),
  ('/kiosk', KioskPage),
  ('/handler', LocationEntryHandler),
  ('/callback_picup', CallbackPicup),
  ('/img', Image)
])


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
