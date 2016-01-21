# Submission for nanodegree project 4 - Conference Organization App

## Description
This product uses the Google App Engine to create a robust, exhaustive API for the Conference application provided by Udacity. In
order to use this application, you will need to sign up for an account, then create a project. The remainin instructions are below.

## Design choices
In implementing the sessions, I chose to replicate much of what was used for the conferences API. Like most Kinds in App engine, we needed the ability to create and retrieve sessions. Unique to this Kind would be the association with Conference. In SQL terms it is a parent table. Datatable calls it an ancestor. The important thing is it is a 1 to many relationship. Speaker was more or less just another field for a Session. Returning sessions for a speaker is a simple query.

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
