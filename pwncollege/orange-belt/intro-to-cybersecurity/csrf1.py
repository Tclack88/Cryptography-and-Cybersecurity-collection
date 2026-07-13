from flask import Flask, redirect
# Strategy: We want the user to hit /publish (equivalent to visiting the URL).
# A redirect keeps the original headers, so it appears that it originated from the source

app = Flask(__name__)

@app.route("/")
def respond():
    url = "http://challenge.localhost:80/publish"
    return redirect(url)

app.run(debug=True, port=1337)
