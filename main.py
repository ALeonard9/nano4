#!/usr/bin/env python

"""
main.py -- Udacity conference server-side Python App Engine
    HTTP controller handlers for memcache & task queue access

$Id$

created by wesc on 2014 may 24

"""

__author__ = 'wesc+api@google.com (Wesley Chun)'

import webapp2
from google.appengine.api import app_identity
from google.appengine.api import mail
from google.appengine.api import memcache
from conference import ConferenceApi

class SetAnnouncementHandler(webapp2.RequestHandler):
    def get(self):
        """Set Announcement in Memcache."""
        ConferenceApi._cacheAnnouncement()
        self.response.set_status(204)


class SendConfirmationEmailHandler(webapp2.RequestHandler):
    def post(self):
        """Send email confirming Conference creation."""
        mail.send_mail(
            'noreply@%s.appspotmail.com' % (
                app_identity.get_application_id()),     # from
            self.request.get('email'),                  # to
            'You created a new Conference!',            # subj
            'Hi, you have created a following '         # body
            'conference:\r\n\r\n%s' % self.request.get(
                'conferenceInfo')
        )

# Set the fetaured speaker
class SetFeaturedSpeaker(webapp2.RedirectHandler):
    def post(self):
        print self.request.get('speaker')
        memcache.set("featuredSpeaker",
                         self.request.get('speaker') + ": " +
                         self.request.get('name'))
        self.response.set_status(204)

# class SetFeaturedSpeakerHandler(webapp2.RequestHandler): # New Code
#     def post(self):
#         """Set Featured Speaker."""
#         data = {'websafeConferenceKey': self.request.get('websafeConferenceKey'),
#                 'speaker': self.request.get('speaker')}
#         ConferenceApi._cacheFeaturedSpeaker(data)
#         self.response.set_status(204)


app = webapp2.WSGIApplication([
    ('/crons/set_announcement', SetAnnouncementHandler),
    ('/tasks/send_confirmation_email', SendConfirmationEmailHandler),
    ('/tasks/set_featured_speaker', SetFeaturedSpeaker),
], debug=True)