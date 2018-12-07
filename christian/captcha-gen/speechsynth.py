'''
Speech synthesizer module, need to have google cloud texttospeech api activated
from google cloud example
'''


from google.cloud import texttospeech
import os


# deletes existing file if the same name
# returns filename from wordstring
def make_audio(wordstring, outputfname, outputfolder='./'):
    client = texttospeech.TextToSpeechClient()
    
    # set text input
    synthesis_input = texttospeech.types.SynthesisInput(text=wordstring)
    
    # voice options...
    voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    # idek
    audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)

    # response
    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    
    output = outputfolder + outputfname+'.wav'
    # write to file --- WILL DELETE FILE IF EXISTS
    if os.path.exists(output): os.remove(output)

    with open(output, 'w+') as out:
        out.write(str(response.audio_content))

    return output
