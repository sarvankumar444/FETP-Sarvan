import json

import requests
from authlib.integrations.flask_client import OAuth
from flask import Flask, abort, redirect, render_template, session, url_for,request,jsonify

app = Flask(__name__)

appConf = {
    "OAUTH2_CLIENT_ID": "1021115725397-1cgg3qg2mnqmgc6e94ljgs1u7modcajl.apps.googleusercontent.com",
    "OAUTH2_CLIENT_SECRET": "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",
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": "e9248057-1fda-4130-9d47-bff8c430cca6",
    "FLASK_PORT": 5000
}

app.secret_key = appConf.get("FLASK_SECRET")

oauth = OAuth(app)
# list of google scopes - https://developers.google.com/identity/protocols/oauth2/scopes
oauth.register(
    "myApp",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read",
        # 'code_challenge_method': 'S256'  # enable PKCE
    },
    server_metadata_url=f'{appConf.get("OAUTH2_META_URL")}',
)


@app.route("/")
def home():
    return render_template("home.html", session=session.get("user"),
                           pretty=json.dumps(session.get("user"), indent=4))


@app.route("/signin-google")
def googleCallback():
    # fetch access token and id token using authorization code
    token = oauth.myApp.authorize_access_token()

    # fetch user data with access token
    personDataUrl = "https://people.googleapis.com/v1/people/me?personFields=genders,birthdays"
    personData = requests.get(personDataUrl, headers={
        "Authorization": f"Bearer {token['access_token']}"
    }).json()
    token["personData"] = personData
    # set complete user information in the session
    session["user"] = token
    return redirect(url_for("home"))


@app.route("/google-login")
def googleLogin():
    if "user" in session:
        abort(404)
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

# Second code phase 2
# -------------
def process_word(size):
    word = "FORMULAQSOLUTIONSFORMULAQSOLUTIONS"
    l = [letter for letter in word]
    result = []

    num = size // 2

    for i in range(num + 1):
        spaces = " " * (size - i - 1)
        character = "".join(l[i:(i * 3) + 1])
        result.append(spaces + character)

    ch = list(character)

    try:
        for i in range(num, -1, -1):
            if ch != []:
                spaces = " " * (size - i - 1)

                if ch != []:
                    ch.pop(0)
                    ch.pop(-1)

                character = "".join(ch)
                result.append(spaces + character)
    except IndexError:
        pass

    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        size = int(data['size'])
        result = process_word(size)
        return jsonify({'result': result})
    else:
        return render_template('home.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=appConf.get(
        "FLASK_PORT"), debug=True)