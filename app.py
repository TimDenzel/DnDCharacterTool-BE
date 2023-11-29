import threading
import webbrowser

from flask import Flask, request, render_template
from characterService import *
from flask_cors import CORS
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
    except Exception as e:
        if hasattr(e, 'message'):
            return print(e.message), 500
        else:
            return '', 500


@app.route('/character', methods=['POST'])
def addNewCharacter():  # put application's code here
    try:
        addCharacter(request.data)
        return '', 201
    except ValueError as v:
        if hasattr(v, 'message'):
            return print(v.message), 400
        else:
            return '', 400
    except ReferenceError:
        return '', 409
    except Exception as e:
        if hasattr(e, 'message'):
            return print(e.message), 500
        else:
            return '', 500


@app.route('/character', methods=['PUT'])
def updateOldCharacter():  # put application's code here
    try:
        updateCharacter(request.args.get("id"), request.data)
        return '', 202
    except FileNotFoundError:
        return '', 404
    except ValueError as v:
        if hasattr(v, 'message'):
            return print(v.message), 400
        else:
            return '', 400
    except ReferenceError:
        return '', 409
    except Exception as e:
        if hasattr(e, 'message'):
            return print(e.message), 500
        else:
            return '', 500


@app.route('/character', methods=['DELETE'])
def deleteOldCharacter():  # put application's code here
    if deleteCharacter(request.args.get("id")):
        return '', 204
    else:
        return '', 404



if __name__ == '__main__':
    port = 5000
    url = 'http://127.0.0.1:{0}'.format(port)
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    app.run(port=port, debug=False)

