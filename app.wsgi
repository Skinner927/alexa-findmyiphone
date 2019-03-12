"""
This is a WSGI script that will take responses from Amazon's Echo/Alexa.
"""
import os
import sys

# Change working directory so relative paths (and template lookup) work again
here_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(here_dir)
activate_this = os.path.join(here_dir, 'venv/bin/activate_this.py')
with open(activate_this) as f:
    code = compile(f.read(), activate_this, 'exec')
    exec(code, dict(__file__=activate_this, __name__='__name__'))
if here_dir not in sys.path:
    sys.path.append(here_dir)

# Expose the application for wsgi to grab
import app

application = app.application
