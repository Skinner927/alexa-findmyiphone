"""
This is a WSGI script that will take responses from Amazon's Echo/Alexa.
"""
import os, sys

# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))
activate_this = os.path.dirname(os.path.abspath(__file__)) + \
                '/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
path = os.path.dirname(__file__)
if path not in sys.path:
    sys.path.append(path)

import bottle
from bottle import request, post
from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudFailedLoginException
import difflib
from users import USERS


@post('/')
def findIphone():
    try:
        intent = request.json['request']['intent']
        if intent['name'] == 'FindIphone':
            user = intent['slots']['User']['value']
            return findUserIphone(user)
    except PyiCloudFailedLoginException:
        return response("Invalid icloud email or password for " + user);
    except Exception as e:
        return response("Whoops, something broke: " + str(e))

    return response(
        "No idea what you asked for. Try saying, Find My iPhone, John.")


# run bottle
# do not remove the application assignment (wsgi won't work)
application = bottle.default_app()


def findUserIphone(user):
    user = user.lower()

    found_user = difflib.get_close_matches(user, USERS.keys(), n=1)

    if len(found_user) == 0:
        return response("I don't know who " + user + " is.")
    
    user = found_user[0]
    email, passwd = USERS[user]
    api = PyiCloudService(email, passwd)   

    if api.requires_2fa:
        return response(("This account requires two factor authentication, which "
                         "puts you in an odd place, because you need your phone to "
                         "authorize for two factor authentication. I cannot help "
                         "you find your iphone."))

    phones = [d for d in api.devices if d.content['deviceClass'] == 'iPhone']

    if len(phones) < 1:
        return response("Sorry, couldn't find any iPhones for " + user)

    for p in phones:
        p.play_sound()

    return response("Calling " + user + "'s iPhone.")


def response(msg):
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": msg,
            },
            "shouldEndSession": True
        }
    }

