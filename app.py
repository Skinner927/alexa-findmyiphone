import bottle
from bottle import request, post
from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudFailedLoginException
import difflib
import requests
from users import USERS

# It doesn't allow us to take extra time to process so who cares
send_progressive = False


def get_safe(dic, *keys):
    """
    Safely traverse through dictionary chains
    :param dict dic:
    :param str keys:
    :return:
    """
    no_d = dict()
    for key in keys:
        dic = dic.get(key, no_d)
    if dic is no_d:
        return None
    return dic


def response(msg):
    return dict(
        version='1.0',
        response=dict(
            outputSpeech=dict(
                type='PlainText',
                playBehavior='REPLACE_ENQUEUED',
                text=msg,
            ),
            shouldEndSession=True
        )
    )


def notify_user_phones(user, request):
    if not user:
        return response('I don\'t know who you are.')
    user = user.lower()

    found_user = difflib.get_close_matches(user, USERS.keys(), n=1)

    if len(found_user) == 0:
        return response('I don\'t know who {} is.'.format(user))

    if send_progressive:
        # Send a progressive notice that we're going to look up their
        # account. This part is slow so Alexa might time out otherwise.
        requests.post(
            'https://api.amazonalexa.com/v1/directives',
            json=dict(
                header=dict(
                    requestId=get_safe(request, 'request', 'requestId')
                ),
                directive=dict(
                    type='VoicePlayer.Speak',
                    speech='Looking for {}\'s devices to call.'.format(user)
                )
            ),
            headers=dict(
                Authorization='Bearer {}'.format(
                    get_safe(request, 'context', 'System', 'apiAccessToken'))
            ))

    user = found_user[0]
    email, passwd = USERS[user]
    api = PyiCloudService(email, passwd)

    phones = [d for d in api.devices if d.content['deviceClass'] == 'iPhone']

    if len(phones) < 1:
        return response('Sorry, I couldn\'t find any iPhones for '
                        '{}.'.format(user))

    for p in phones:
        try:
            p.play_sound()
        except Exception:
            pass

    return response('Calling {}\'s iPhone'.format(user))


@post('/')
def find_iphone():
    request_type = get_safe(request.json, 'request', 'type')
    if request_type == 'SessionEndedRequest':
        # Just eat these
        return

    intent = get_safe(request.json, 'request', 'intent')
    if request_type != 'IntentRequest' or not intent:
        return response('I could not understand your request.')
    if intent.get('name') == 'FindIphone':
        user = get_safe(intent, 'slots', 'User', 'value')
        try:
            return notify_user_phones(user, request.json)
        except PyiCloudFailedLoginException:
            return response('Invalid icloud email or password for '
                            '{}'.format(user))
        except Exception as e:
            return response('Whoops, something broke: {}'.format(e))

    return response('No idea what you asked for. '
                    'Try saying, Find My iPhone, John.')


# run bottle
# do not remove the application assignment (wsgi won't work)
application = bottle.default_app()
