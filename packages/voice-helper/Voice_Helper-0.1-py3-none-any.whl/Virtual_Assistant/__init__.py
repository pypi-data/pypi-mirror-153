"""
A package designed to help coders create there own voice assistant
"""

# import what we need

import pyttsx3, speech_recognition as sr

# create the voices list

voices = ["male", "female"]

# create the voice assistant class


class voice_assistant:
    """
    A easy to use voice assistant

    Some functions include:
    speak: Gets the assistant to say a string
    listen: Gets the assistant to listen for your voice, returning a string
    """

    # define the init function

    def __init__(self, name, voice):

        # test if the voice is in voices

        if voice in voices:

            # set the parameters

            self.name = name

            self.voice = voice

            # create the voice engine and the voices to use list

            global voice_engine

            voice_engine = pyttsx3.init()

            voices_to_use = voice_engine.getProperty("voices")

            # test if the voice is male

            if self.voice == "male":

                # set the voice

                voice_engine.setProperty("voice", voices_to_use[0].id)

            # test if the above condition is false

            else:

                # set the voice

                voice_engine.setProperty("voice", voices_to_use[1].id)

        # test if the above condition is false

        else:

            # raise an error

            raise TypeError("Invalid Voice")

    # define the speak function

    def speak(self, text):
        """
        Makes the assistant say the passed string
        """

        # say the text

        voice_engine.say(text)
        voice_engine.runAndWait()

    # define the listen function

    def listen(self):
        """
        Listens to your voice and returns a string if successful
        """

        # create the listener

        listener = sr.Recognizer()

        # continue with the microphone as source

        with sr.Microphone() as source:

            # create the audio

            audio = listener.listen(source)

            # set said

            said = ""

            # try to get what the user said

            try:

                # get what the user said

                said = listener.recognize_google(audio)

            # if that fails, print and say an error message and then retry

            except:

                # print and say an error message and then retry

                print("System Error. Please speak again")

                self.speak("Sorry, I had trouble hearing you. Please try again")

                said = self.listen()

        # return said

        said = said.replace(".", "")
        said = said.replace("'", "")
        said = said.replace("mail", "male")
        said = said.replace("femail", "female")
        return said.lower()
