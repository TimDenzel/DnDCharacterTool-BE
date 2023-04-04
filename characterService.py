import json
import jsonschema
from jsonschema import validate

chars = json.load(open('files/characters.json', 'r'))

characterSchema = {
    "type": "object",
    "properties": {
        "ac": {
            type: "integer",
            "minimum": 0
        },
        "charisma": {
            type: "integer",
            "minimum": 0,
            "maximum": 30
        },
        "constitution": {
            type: "integer",
            "minimum": 0,
            "maximum": 30
        },
        "dexterity": {
            type: "integer",
            "minimum": 0,
            "maximum": 30
        },
        "id": {
            type: "number",
            "minimum": 0
        },
        "immunities": {
            type: "string"
        },
        "information": {
            type: "string"
        },
        "intelligence": {
            type: "integer",
            "minimum": 0,
            "maximum": 30
        },
        "languages": {
            type: "string"
        },
        "level": {
            type: "integer",
            "minimum": 1,
            "maximum": 20
        },
        "maxHP": {
            type: "integer",
            "minimum": 0
        },
        "name": {
            type: "string"
        },
        "passivePerception": {
            type: "integer",
            "minimum": 0
        },
        "resistances": {
            type: "string"
        },
        "strength": {
            type: "integer",
            "minimum": 0,
            "maximum": 30
        },
        "wisdom": {
            type: "integer",
            "minimum": 0,
            "maximum": 30
        },

    },
    "required": [
        "ac",
        "charisma",
        "constitution",
        "dexterity",
        "id",
        "intelligence",
        "level",
        "maxHP",
        "name",
        "passivePerception",
        "strength",
        "wisdom"
    ]
}


def searchByName(name):  # name search function

    filteredChars = []
    if len(name) > 0:
        for char in chars:
            if name.lower() in char['name'].lower():
                filteredChars.append(char)
        return filteredChars
    else:
        return chars


def searchById(id):  # search function with id
    for char in chars:
        if int(id) == char['id']:
            return char
    raise FileNotFoundError


def addCharacter(characterAsJson):
    character = json.loads(characterAsJson)
    if not validateJson(character):
        raise ValueError
    if existsId(character):
        raise ReferenceError
    chars.append(character)
    writeInFile()
    return True


def updateCharacter(id, characterAsJson):
    # castedId = int(id)
    # characterId = json.loads(characterAsJson)["id"]
    # if characterId != castedId:

    if json.loads(characterAsJson)["id"] != int(id):
        raise ReferenceError
    if not deleteCharacter(id):
        raise FileNotFoundError
    addCharacter(characterAsJson)
    writeInFile()
    return True


def deleteCharacter(id):
    try:
        existingCharacter = searchById(id)
        chars.remove(existingCharacter)
        writeInFile()
        return True
    except:
        return False


def writeInFile():
    with open('files/characters.json', 'w') as outfile:
        json.dump(chars, outfile)


def existsId(character):
    for char in chars:
        if character["id"] == char["id"]:
            return True

    return False


def validateJson(jsonData):
    try:
        validate(instance=jsonData, schema=characterSchema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True
