import pyttsx3
import time
import threading


class VoiceCoach:

    def __init__(self):

        self.enabled = True

        self.last_message = ""
        self.last_time = 0

        self.cooldown = 3

    def toggle(self):

        self.enabled = not self.enabled

        return self.enabled

    def speak(self, message):

        if not self.enabled:
            return

        current_time = time.time()

        if (
            message == self.last_message
            and current_time - self.last_time < self.cooldown
        ):
            return

        self.last_message = message
        self.last_time = current_time

        threading.Thread(
            target=self._speak_thread,
            args=(message,),
            daemon=True
        ).start()

    def _speak_thread(self, message):

        try:

            engine = pyttsx3.init()

            engine.setProperty(
                "rate",
                170
            )

            engine.say(message)

            engine.runAndWait()

        except:
            pass