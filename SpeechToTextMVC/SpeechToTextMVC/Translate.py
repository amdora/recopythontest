class Translate(object):
   def transcribe_gcs():
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()
    path="gs://speechtotext6577/audio.flac"
    audio = types.RecognitionAudio(uri=path)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        #sample_rate_hertz=16000,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=290)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    a=[]
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        a.insert( 1, "Transcript:".format(result.alternatives[0].transcript))
        #a.insert = { 1, "Transcript": format(result.alternatives[0].transcript), 2, "Confidence": format(result.alternatives[0].confidence)}
       # a.append(u'Transcript: {}'.format(result.alternatives[0].transcript))
       # print(u'Transcript: {}'.format(result.alternatives[0].transcript))
       # print('Confidence: {}'.format(result.alternatives[0].confidence))
    return a

#else: transcribe_file(args.path) 


