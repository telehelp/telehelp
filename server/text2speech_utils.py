"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import os
import time
import urllib.parse

from dotenv import load_dotenv
from google.cloud import texttospeech
from google.oauth2 import service_account
from zipcode_utils import getListOfCities
from zipcode_utils import readZipCodeData

load_dotenv()

LANGUAGE_CODE = os.getenv("TELEHELP_LANG")
if LANGUAGE_CODE == "SE":
    ZIPDATA = "SE.txt"
else:
    ZIPDATA = "DE.txt"


text_input = dict()  # contains key as filename and string for tts

"""
Common sound bytes (both customer and volunteer)
"""
text_input["avreg_confirmed"] = "You are now unregistered. Your personal data has been removed."
text_input["du_kopplas"] = "You will now be connected to the last person you talked to."

"""
Sound bytes played to customer only
"""
text_input[
    "info"
] = "Hi and welcome to Telehelp. Here you can be assigned a volunteer that can help\
 you handle self-isolation during the COVID-19 crisis. Examples of tasks are to go \
 grocery shopping or visiting a pharmacy. The next time you call this number, you can choose to \
 reach the same volunteer again. If you require assistance from a volunteer, press 1. \
 If you want to hear this information again, press 2."

text_input["post_nr"] = "Enter your postal code, 5 digits, after the beep. Your postal code will be stored."
text_input["du_befinner"] = "We think you are in the vicinity of"
text_input["stammer_det"] = "If this is correct, press 1. To change your postal code, press 2."

text_input[
    "behover_hjalp"
] = "Welcome to Telehelp! We can see that you've already used our service. Do you want to get in touch with"
text_input[
    "ensam_gamling"
] = "Välkommen till Telehelp. \
    Vi ser att du redan använt vår tjänst. Behöver du hjälp med en vardagssyssla? Tryck 1\
    Vill du avregistrera dig från tjänsten? Tryck 2."


text_input[
    "pratade_sist"
] = "who you talked to last? Press 1. If you want to switch to another volunteer, press 2. If you want to unregister from the service, press 3."

text_input["info_igen"] = "Do you want to hear the information again?"

text_input["vi_letar"] = "We are finding someone from your area who can assist you."

text_input["finns_ingen"] = "No volunteers are registered in your area. Please try again later."

text_input[
    "ringer_tillbaka"
] = "The call will now end, but you will soon get called up by a volunteer. It is up to you to share what you need help with. Bye!"

"""
Sound bytes played to volunteer only
"""
text_input[
    "hjalte"
] = "Hi! Somebody has called in to Telehelp and is in need of a hero! Can you take this call? Press 1. Otherwise, press 2."

text_input[
    "registrerad_volontar"
] = "Welcome to Telehelp! We see that you are registered as a volunteer. Do you want to reach the person you last helped? Press 1. If you want to unregister from the service, press 2."

text_input[
    "hjalper_ingen"
] = "Welcome to Telehelp! We see that you are registered as a volunteer. \
        You are currently not helping anyone from an at-risk group. Hopefully, we will call you up soon, \
        when someone is in need of assistance. Thank you for your solidarity. If you want to unregister from the service, press 1. Otherwise, please hang up."

text_input[
    "ingen_hittad"
] = "Unfortunately, we did not find any available volunteers in your area. Please try calling back later."


"""
Input parameters for text-to-speech model
"""
voice = texttospeech.types.VoiceSelectionParams(
    language_code="en-GB", name="en-GB-Wavenet-D", ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE
)


# Select the type of audio file you want returned
audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.MP3, speaking_rate=0.85
)

# Instantiates a client
dirname = os.path.dirname(__file__)
filepath_json = os.path.join(dirname, "..", "..", "GoogleTextToSpeech.json")
cred = service_account.Credentials.from_service_account_file(filepath_json)
client = texttospeech.TextToSpeechClient(credentials=cred)


def generateSoundBytes():
    print("Generating IVR sound bytes (skips existing)")
    for key in text_input:
        # The response's audio_content is binary.
        outputPath = os.path.join("media", "ivr", key + ".mp3")
        if not os.path.isfile(outputPath):
            synthesis_input = texttospeech.types.SynthesisInput(text=text_input[key])
            response = client.synthesize_speech(synthesis_input, voice, audio_config)

            with open(outputPath, "wb") as out:
                # Write the response to the output file.
                out.write(response.audio_content)
                print('  Audio content written to file "' + outputPath + '" (relative to current dir).')

            # Insert pause to not reach quota of calls per minute
            time.sleep(0.2)


# Generate sound bytes for all cities in SE.txt, without overwriting existing ones
def generateCitySoundBytes():
    print("Generating city sound bytes (skips existing)")
    cities = getListOfCities(ZIPDATA)
    for city in cities:
        outputPath = os.path.join("media", "city", city + ".mp3")
        if not os.path.isfile(outputPath):
            synthesis_input = texttospeech.types.SynthesisInput(text=city)
            response = client.synthesize_speech(synthesis_input, voice, audio_config)

            with open(outputPath, "wb") as out:
                out.write(response.audio_content)
                print('  Audio content written to file "' + outputPath + '"')

            # Insert pause to not reach quota of calls per minute
            time.sleep(0.15)


def generateNameSoundByte(name):
    print("Generating name sound bytes (skips existing)")
    outputPath = os.path.join("media", "name", name + ".mp3")
    if not os.path.isfile(outputPath):
        synthesis_input = texttospeech.types.SynthesisInput(text=name)
        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        with open(outputPath, "wb") as out:
            out.write(response.audio_content)
            print('  Audio content written to file "' + outputPath + '"')


def generateCustomSoundByte(text_string, filename, saveDir="/media"):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text_string)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open(os.path.join(saveDir, filename), "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print("  Audio content written to file %s" % os.path.join(saveDir, filename))


if __name__ == "__main__":
    generateSoundBytes()
    generateCitySoundBytes()
