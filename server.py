
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/mapbox_js')
def mapbox_js():
	return render_template('mapbox_js.html', 
		ACCESS_KEY=app.config['MAPBOX_ACCESS_KEY']
	)

# app.run(threaded=True)
