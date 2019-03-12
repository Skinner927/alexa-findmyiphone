import bottle
import app
app.send_progressive = False

bottle.run(app=app.application, host='127.0.0.1', port=8080)
