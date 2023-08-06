import getopt
import sys
from flask import Flask
from flask_injector import FlaskInjector

from tracker.dependency import configure
from tracker.core.git_push_hook import account_api as git

app = Flask(__name__)
app.register_blueprint(git)

FlaskInjector(app=app, modules=[configure])

# Start the Flask server
if __name__ == "__main__":
    iport = 5000
    ihost = '127.0.0.1'

    myopts, args = getopt.getopt(sys.argv[1:], "p:h")

    ###############################
    # o == option
    # a == argument passed to the o
    ###############################
    for o, a in myopts:
        if o == '-p':
            iport = int(a)
        elif o == '-h':
            ihost = a
        else:
            print("Usage: %s -p port -h host" % sys.argv[0])

    app.run(host=ihost, port=iport)
