# Submission for nanodegree project 4 - Conference Organization App

## Description
This product uses the Google App Engine to create a robust, exhaustive API for the Conference application provided by Udacity. In
order to use this application, you will need to sign up for an account, then create a project. The remainin instructions are below.

## Design choices
In implementing the sessions, I chose to replicate much of what was used for the conferences API. Like most Kinds in App engine, we needed the ability to create and retrieve sessions. Unique to this Kind would be the association with Conference. In SQL terms it is a parent table. Datatable calls it an ancestor. The important thing is it is a 1 to many relationship. Speaker was more or less just another field for a Session. Returning sessions for a speaker is a simple query.

In terms of data modeling, these design choices were made with normalization in mind. This minimalizes redundant data. Here is a view of the variable types selected for this Session model.

```
name                    = ndb.StringProperty(required=True)
highlights              = ndb.StringProperty()
speaker                 = ndb.StringProperty()
duration                = ndb.IntegerProperty() # in minutes format
typeOfSession           = ndb.StringProperty(repeated=True)
date                    = ndb.DateProperty()
startTime               = ndb.TimeProperty() # 24hr format
organizerUserId         = ndb.StringProperty()
```
Name is a required string, since it will how users identify a session.
typeOfSession is the only repeated variable since a session may have many types. The remaining variables are 1 to 1. Each subsequent variable has its appropriate type. Note that startTime uses a 24 hour format for easy addition or subtraction.

## Additional Queries
1. Get all Cloud Sessions. This method returns sessions containing ultra hot topic of Cloud. The Conference app can use this in a "Cloud Week" promotion. Geared towards cloud developers.
```
    @endpoints.method(message_types.VoidMessage, SessionForms,
            http_method='GET', name='getCloudSessions')
    def getCloudSessions(self, request):
        """Returns sessions featuring a cloud highlight"""

        sessions = Session.query(ndb.OR(
            Session.highlights == 'cloud'
            ))
        return SessionForms(
            items=[self._copySessionToForm(session) for session in sessions]
        )

```
2. Get all sessions that are shorter than an hour. This would be useful for people with short attention spans. Perhaps best used for conferences that invite children under the age of 10.
```
    @endpoints.method(message_types.VoidMessage, SessionForms,
            http_method='GET', name='getShortSessions')
    def getShortSessions(self, request):
        """Returns sessions that are 1 hour or less"""

        sessions = Session.query(ndb.OR(
            Session.duration < 60
            ))
        return SessionForms(
            items=[self._copySessionToForm(session) for session in sessions]
        )
```
## Query problem
The problem with this query is that it cannot be handled with a single query.  NBD cannot natively handle two inequality filters at once.

## Query solution
The query for sessions before 7pm is solved by taking the SessionForms as an input, querying ndb for a start time for less than or equal to the 24-hour formatted 7pm (19). To solve the problem above I've implement a single query that filters on sessions whose start times begin before or at 7pm. Secondarily, using a loop to iterate over the responses, I append sessions that are not workshops to the returned value.
```
    # Filters for sessions that occur before 7PM and are not a workshop type
    @endpoints.method(message_types.VoidMessage, SessionForms,
            http_method='GET', name='getBefore7PMWorkshopSessions')
    def getBefore7PMWorkshopSessions(self, request):
        """Returns sessions that occur before 7PM and are not a workshop"""

        # First filter sessions based on time using NBD
        sessions = Session.query(ndb.AND(
                Session.startTime != None,
                Session.startTime <= timed(hour=19)
                ))
        # Second, filter session type using native Python since NBD cannot
        # handle two inequality filters in one query
        time_filter_sessions = []
        for session in sessions:
            if 'workshop' in session.typeOfSession:
                continue
            else:
                time_filter_sessions.append(session)

        return SessionForms(
            items=[self._copySessionToForm(session) for session in time_filter_sessions]
        )
```


## Products
- [App Engine][1]

## Language
- [Python][2]

## APIs
- [Google Cloud Endpoints][3]

## Setup Instructions
1. Update the value of `application` in `app.yaml` to the app ID you
   have registered in the App Engine admin console and would like to use to host
   your instance of this sample.
1. Update the values at the top of `settings.py` to
   reflect the respective client IDs you have registered in the
   [Developer Console][4].
1. Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
1. (Optional) Mark the configuration files as unchanged as follows:
   `$ git update-index --assume-unchanged app.yaml settings.py static/js/app.js`
1. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting your local server's address (by default [localhost:8080][5].)
1. (Optional) Generate your client library(ies) with [the endpoints tool][6].
1. Deploy your application.


[1]: https://developers.google.com/appengine
[2]: http://python.org
[3]: https://developers.google.com/appengine/docs/python/endpoints/
[4]: https://console.developers.google.com/
[5]: https://localhost:8080/
[6]: https://developers.google.com/appengine/docs/python/endpoints/endpoints_tool
