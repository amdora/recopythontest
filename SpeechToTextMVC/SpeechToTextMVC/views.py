"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from SpeechToTextMVC import app
from flask import request
from flask import Flask, render_template, request
from werkzeug import secure_filename
from pydub import AudioSegment
import subprocess
from google.cloud import storage
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="Speech To Text Auth.json"

@app.route('/')
@app.route('/home')
def home():
          if request.method == 'POST':
            f = request.files['file']
            if f.filename == '':
                message='Please Select a wav file'
                return render_template("index.html", message=message,title="Google speech to text")
            f.save(secure_filename(f.filename))
            src = f.filename
            dst = "Audio.flac"
            AudioSegment.converter = "ffmpeg/bin/ffmpeg"
            sound = AudioSegment.from_wav(src)
            sound.export(dst, format="flac")

            storage_client = storage.Client()
            bucket = storage_client.get_bucket("speechtotext6577")
            blob = bucket.blob(dst)

            blob.upload_from_filename(dst)
            os.remove(dst)
            os.remove(f.filename)
            myList=transcribe_gcs(dst)
            delete_blob("speechtotext6577","Audio.flac")
            return render_template("index.html", myList=myList,title="Google speech to text")
          return render_template("index.html",title="Google speech to text")

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/Translate')
def Translate():
    """Renders the about page."""
    return render_template('Translate.html',title='Translate',year=datetime.now().year,message='Your application description page.'
    )

@app.route('/Result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      #result = request.form
     # rresult=transcribe_gcs()
     # myList= transcribe_gcs()
      if 'file' not in request.files:
          flash('No file part')
          return redirect(request.url)
      file = request.files['file']
      if file.filename == '':
          flash('No file selected for uploading')
          return redirect(request.url)
      if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          flash('File(s) successfully uploaded')
          return render_template("Translate.html", myList=myList)
     # result = transcribe_gcs()
      #return render_template("Translate.html", myList=myList)


def delete_blob(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

def transcribe_gcs(fileName):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()
    path="gs://speechtotext6577/"+fileName
    audio = types.RecognitionAudio(uri=path)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        #sample_rate_hertz=16000,
        language_code='ja')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=290)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    a=[]
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        a.insert( 0, "Transcript: "+format(result.alternatives[0].transcript))
        a.insert( 1, "Confidence: "+format(result.alternatives[0].confidence))
        #a.insert = { 1, "Transcript": format(result.alternatives[0].transcript), 2, "Confidence": format(result.alternatives[0].confidence)}
       # a.append(u'Transcript: {}'.format(result.alternatives[0].transcript))
       # print(u'Transcript: {}'.format(result.alternatives[0].transcript))
       # print('Confidence: {}'.format(result.alternatives[0].confidence))
    return a




@app.route("/Upload", methods=['GET', 'POST'])
def Upload():
          if request.method == 'POST':
            f = request.files['file']
            if f.filename == '':
                message='Please Select a wav file'
                return render_template("Upload.html", message=message)
            f.save(secure_filename(f.filename))
            src = f.filename
            dst = "Audio.flac"
            AudioSegment.converter = "ffmpeg/bin/ffmpeg"
            sound = AudioSegment.from_wav(src)
            sound.export(dst, format="flac")

            storage_client = storage.Client()
            bucket = storage_client.get_bucket("speechtotext6577")
            blob = bucket.blob(dst)

            blob.upload_from_filename(dst)
            os.remove(dst)
            os.remove(f.filename)
            myList=transcribe_gcs(dst)
            delete_blob("speechtotext6577","Audio.flac")
            return render_template("Upload.html", myList=myList)
          return render_template("Upload.html")