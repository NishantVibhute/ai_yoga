from gtts import gTTS
import pygame
import tempfile
import threading
import os

from core.translations import TRANSLATIONS

pygame.mixer.init()


class VoiceCoach:

    def __init__(self):
        self.enabled = True

        self.languages = [
            "en",
            "hi",
            "mr",
            "gu",
            "ta"
        ]

        self.language = "en"

    def toggle(self):
        self.enabled = not self.enabled

    def toggle_language(self):

        current_index = self.languages.index(
            self.language
        )

        next_index = (
            current_index + 1
        ) % len(self.languages)

        self.language = self.languages[
            next_index
        ]

    def speak(self, text):

        if not self.enabled:
            return

        threading.Thread(
            target=self._play_audio,
            args=(text,),
            daemon=True
        ).start()

    def translate(self, text):

        if self.language == "en":
            return text

        return TRANSLATIONS.get(
            text,
            {}
        ).get(
            self.language,
            text
        )

    def _play_audio(self, text):

        try:

            tts = gTTS(
                text=text,
                lang=self.language
            )

            filename = tempfile.mktemp(".mp3")

            tts.save(filename)

            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

        except Exception as e:
            print("Voice Error:", e)