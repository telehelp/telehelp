"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
import os

text_input = dict() # contains key as filename and string for tts

# NOTE: Manually edited with additional pauses: text_input['info'] = 'Hej och välkommen till Telehelp. Här kan du bli tilldelad en volontär som kan hjälpa dig med en vardagssyssla. Det kan exempelvis vara att handla mat eller hämta ut medicin. Nästa gång du ringer kan du välja att bli tilldelad samma person. Dina uppgifter kommer att samlas.'
text_input['post_nr'] = 'Knappa vänligen in ditt postnummer, 5 siffror, efter tonen.'
text_input['du_befinner'] = 'Du befinner dig i närheten av '
text_input['stammer_det'] = 'Stämmer det?'
text_input['om_inte'] = 'Stämmer det?'
text_input['behover_hjalp'] = 'Behöver du hjälp med en vardagssyssla?'
text_input['info_igen'] = 'Vill du höra informationen igen?'
text_input['andra_postnr'] = 'Vill du ändra ditt postnummer?'
text_input['avreg'] = 'Vill du avregistrera dig från tjänsten?'
text_input['kontakta'] = 'Vill du att vi kontaktar '
text_input['igen'] = 'igen?'
text_input['nagon_annan'] = 'Vill du prova någon annan?'
text_input['vi_letar'] = 'Vi letar efter någon som kan hjälpa i närområdet '
text_input['du_kopplas'] = 'Du kopplas nu upp med'
text_input['upp_till_er'] = 'Det är upp till er att bestämma hur du bäst får hjälp.'
#text_input['tryck'] = 'Tryck '
text_input['1'] = 'Tryck 1'
text_input['2'] = 'Tryck 2'
text_input['3'] = 'Tryck 3'
text_input['4'] = 'Tryck 4'
text_input['5'] = 'Tryck 5'
text_input['6'] = 'Tryck 6'
text_input['6'] = 'Tryck 6'
text_input['7'] = 'Tryck 7'
text_input['8'] = 'Tryck 8'
text_input['9'] = 'Tryck 9'
text_input['0'] = 'Tryck 0'
text_input['hjalte'] = 'Någon från Telehelp behöver en hjälte, dröj kvar medan vi kopplar dig vidare.'
#text_input['nod'] = 'Någon i nöd'
text_input['en_volontar'] = 'en volontär'
text_input['avreg_confirmed'] = 'Du är nu avregistrerad. Din data kommer att raderas.'
text_input['finns_ingen'] = 'Ingen volontär är registrerad i ditt område. Vänligen försök senare.'
text_input['registrerad_volontar'] = 'Välkommen till Telehelp. Vi ser att du är registrerad som volontär.'
text_input['ring_upp_riskgrupp'] = 'Vill du nå den person du hjälpte sist?'
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
    #generateSoundBytes()
    generateCustomSoundByte("Vi letar efter en ledig volontär i ditt område. Samtalet avslutas nu, men du kommer snart att ringas upp av en volontär", 'ringer_tillbaka.mp3', saveDir='../../media')
