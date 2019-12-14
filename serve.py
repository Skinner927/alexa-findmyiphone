import bottle
import app
app.send_progressive = False

bottle.run(app=app.application, host='0.0.0.0', port=8080)
