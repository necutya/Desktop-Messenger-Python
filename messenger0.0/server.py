import time

from flask import Flask, request
from datetime import datetime

app = Flask(__name__)
messages = [
    {"username": "Artem", "text": "Hello!", "time": time.time()},
    {"username": "Danil_lox", "text": "Hi!", "time": time.time()},
]

users = {
    "Artem": "12345",
    "Danil_lox" : "54321"
}

@app.route("/")
def hello_view():
    return "<h1>Welcome to Python messenger!</h1>"


@app.route("/status")
def status_view():
    return {
        "status": True,
        "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "messeges_count": len(messages),
        "users_count": len(users)
    }


@app.route("/send", methods=['POST'])
def send_view():
    """
    Send messages
    input: {
        "username": str,
        "text": str,
        "password": str
    }
    :return: {"ok": bool}
    """
    # Use BD
    data = request.json
    username = data["username"]
    text = data["text"]
    password = data["password"]

    if username not in users or users[username] != password:
        return {"ok": False}

    messages.append({"username": username, "text": text, "time": time.time()})

    return {'ok': True}


@app.route("/auth", methods=['POST'])
def auth_view():
    """
    Authorize user or send error
    input: {
        "username": str,
        "password": str
    }
    :return: {"ok": bool}
    """
    data = request.json
    username = data["username"]
    password = data["password"]

    if username not in users:
        users[username] = password
        return {"ok": True}
    elif users[username] == password:
        return {"ok": True}
    else:
        return {"ok": False}


@app.route("/messages")
def messages_view():
    """
    Return messages after stamp "after"
    :input: after - time stamp
    :return: {
        "messages": [
            {"username": str, "text": str, "time": float},
            ...
            ]
        }
    """
    after = float(request.args['after'])

    return {'messages': [message for message in messages if after < message["time"]]}


app.run()
