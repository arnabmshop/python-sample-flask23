from datetime import datetime
from flask import Flask, render_template
from . import app

CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=arnabsa;AccountKey=GlWpxAlG70eELtWZaz0FrbYyZqLGApX9tSxNLCSDDSjbdYsgbRMYCL/IlSFRQFf5mVcBKPno7XoZ+AStsx90rA==;EndpointSuffix=core.windows.net'
CONTAINER_NAME = 'azureml'

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file.filename)
        blob_client.upload_blob(file)
        return 'File uploaded successfully'
    return 'No file selected'

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
