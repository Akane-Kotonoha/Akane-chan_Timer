import pyaudio
import wave


class AkanePlayer:
    CHUNK = 4096

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=44100,
                                      output=True)

    def __del__(self):
        self.stream.close()
        self.audio.terminate()

    def play(self, filename):
        w_file = wave.open(filename, 'rb')
        data = w_file.readframes(self.CHUNK)
        while data:
            self.stream.write(data)
            data = w_file.readframes(self.CHUNK)
