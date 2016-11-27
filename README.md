#Alexa Find My iPhone

This is an Amazon Echo app that will use the "find my iPhone" feature of iCloud to find your iPhone.

Most of the magic is done by [pyicloud](https://github.com/picklepete/pyicloud).

## About
The handler was written in Python with Bottle web framework. The app is a wsgi application that is meant to be run with Apache's `mod_wsgi` module. However, you could easily port this to anything else. 

## Virtual Envornment
Create your virtual environment in a directory named `venv`. The wsgi script depends on this. Install requirements in `requirements.txt`

## Config on Amazon's end
**Name:** FindMyIPhone

**Invocation Name:** find my iphone

**Intent Schema:**

```
{
  "intents": [
    {
      "intent": "FindIphone",
      "slots": [
        {
          "name": "User",
          "type": "AMAZON.US_FIRST_NAME"
        }
      ]
    }
  ]
}
```

**Utterances:**

```
FindIphone {User}
FindIphone to call {User}
```

## User Config

Copy `users.example.py` to `users.py` to configure users' iCloud accounts. There is a `USERS` dictionary where each key is the name of the user, and each value is a tuple of iCloud username and password.

## How to use

If you configured your app with the given Amazon config, you should be able to say to Alexa: `Alexa, tell Find My iPhone, John` where `John` is the user whose iPhone you are trying to find.

## License
Code licensed under the unlicense. View `LICENSE.txt` for more information.

TL;DR; Code is public domain.