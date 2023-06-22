from datetime import datetime
from flask import Flask, render_template,jsonify,request
from azure.storage.blob import BlobServiceClient
from . import app

CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=arnabsa;AccountKey=GlWpxAlG70eELtWZaz0FrbYyZqLGApX9tSxNLCSDDSjbdYsgbRMYCL/IlSFRQFf5mVcBKPno7XoZ+AStsx90rA==;EndpointSuffix=core.windows.net'
CONTAINER_NAME = 'azureml'
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

@app.route("/")
def home():
    return render_template("layout.html")

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file.filename)
        blob_client.upload_blob(file)
        return 'File uploaded successfully'
    return 'No file selected'

@app.route('/execute-script', methods=['POST'])
def execute_script():
    # Add your Python script logic here
    # For example, print a message
    print('Python script executed successfully')
    return jsonify({'success': True})
