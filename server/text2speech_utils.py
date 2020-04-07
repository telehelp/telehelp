"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
import os

text_input = dict() # contains key as filename and string for tts

'''
Common sound bytes (both customer and volunteer)
'''
text_input['avreg_confirmed'] = 'Du är nu avregistrerad. Din data kommer att raderas.'
text_input['du_kopplas'] = 'Du kopplas nu till personen som du senast pratade med.'

'''
Sound bytes played to customer only
'''
text_input['info'] = 'Hej och välkommen till Telehelp. Här kan du bli tilldelad en volontär \
    som kan hjälpa dig med en vardagssyssla. Det kan exempelvis vara att handla mat eller hämta \
    ut medicin. Nästa gång du ringer kan du välja att bli tilldelad samma person. \
    Behöver du hjälp med en vardagssyssla? Tryck 1. Vill du höra informationen igen? Tryck 2'

text_input['post_nr'] = 'Knappa vänligen in ditt postnummer, 5 siffror, efter tonen. Din postkod kommer att lagras.'
text_input['du_befinner'] = 'Du befinner dig i närheten av '
text_input['stammer_det'] = 'Stämmer det? För att fortsätta, tryck 1. Vill du ändra ditt postnummer? Tryck 2.'

text_input['behover_hjalp'] = 'Välkommen till Telehelp! \
    Vi ser att du redan använt vår tjänst. Vill du att vi kontaktar'
text_input['pratade_sist'] = 'som du pratade med sist? Tryck 1. Vill du byta till en ny volontär? \
    Tryck 2. Vill du avregistrera dig från tjänsten? Tryck 3.'
text_input['info_igen'] = 'Vill du höra informationen igen?'

text_input['vi_letar'] = 'Vi letar efter någon som kan hjälpa dig i närområdet.'
text_input['finns_ingen'] = 'Ingen volontär är registrerad i ditt närområde. Vänligen försök igen senare.'
text_input['ringer_tillbaka'] = 'Samtalet kommer nu att avslutas, men du kommer snart att ringas upp av en volontär. Då är det upp till dig att berätta vad du behöver hjälp med. Hejdå!'

'''
Sound bytes played to volunteer only
'''
text_input['hjalte'] = 'Hej! En användare av Telehelp behöver en hjälte. Vill du ta detta samtal? Tryck 1. Om inte tryck 2.'
text_input['registrerad_volontar'] = 'Välkommen till Telehelp. Vi ser att du är registrerad som volontär. Vill du nå den person du hjälpte sist? Tryck 1. Vill du avregistrera dig från tjänsten? Tryck 2.'
text_input['hjalper_ingen'] = 'Du hjälper för närvarande ingen i riskgruppen. Förhoppningsvis ringer vi upp dig snart, när någon ber om hjälp! Tack för din insats.'

def generateSoundBytes():
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='sv-SE',
        name='sv-SE-Wavenet-A',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3, speaking_rate = 0.85)

    for key in text_input:
        # Set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text=text_input[key])

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        # The response's audio_content is binary.
        with open('media/'+key+'.mp3', 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "'+'media/'+key+'.mp3'+'"')

def generateCustomSoundByte(text_string, filename, saveDir='/media'):
        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='sv-SE',
            name='sv-SE-Wavenet-A',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

        # Select the type of audio file you want returned
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3, speaking_rate = 0.85)

        # Set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text=text_string)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        # The response's audio_content is binary.
        with open(os.path.join(saveDir, filename), 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file %s'%os.path.join(saveDir, filename))

if __name__ == '__main__':
    generateSoundBytes()
    #generateCustomSoundByte("Vi letar efter en ledig volontär i ditt område. Samtalet avslutas nu, men du kommer snart att ringas upp av en volontär", 'ringer_tillbaka.mp3', saveDir='../../media')
