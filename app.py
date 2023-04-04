import threading
import webbrowser

from flask import Flask, request, render_template
from characterService import *
from flask_cors import CORS
from win32api import GenerateConsoleCtrlEvent
app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def root():  # put application's code here
    return render_template('index.html')


@app.route('/characters', methods=['GET'])
def searchCharacters():  # put application's code here
    return searchByName(request.args.get("name"))


@app.route('/character', methods=['GET'])
def getCharacter():  # put application's code here
    try:
        return searchById(request.args.get("id"))
    except FileNotFoundError:
        return '', 404
    except:
        return '', 500


@app.route('/character', methods=['POST'])
def addNewCharacter():  # put application's code here
    try:
        addCharacter(request.data)
        return '', 201
    except ValueError:
        return '', 400
    except ReferenceError:
        return '', 409
    except:
        return '', 500


@app.route('/character', methods=['PUT'])
def updateOldCharacter():  # put application's code here
    try:
        updateCharacter(request.args.get("id"), request.data)
        return '', 202
    except FileNotFoundError:
        return '', 404
    except ValueError:
        return '', 400
    except ReferenceError:
        return '', 409
    except:
        return '', 500


@app.route('/character', methods=['DELETE'])
def deleteOldCharacter():  # put application's code here
    if deleteCharacter(request.args.get("id")):
        return '', 204
    else:
        return '', 404


@app.route('/shutdown', methods=['GET'])
def shutdown():
    CTRL_C_EVENT = 0
    GenerateConsoleCtrlEvent(CTRL_C_EVENT, 0)
    return "Server shutting down..."


if __name__ == '__main__':
    port = 5000
    url = 'http://127.0.0.1:{0}'.format(port)
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    app.run(port=port, debug=False)

