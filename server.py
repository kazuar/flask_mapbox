
from flask import Flask

app = Flask(__name__)
app.debug = True

app.run(threaded=True)
