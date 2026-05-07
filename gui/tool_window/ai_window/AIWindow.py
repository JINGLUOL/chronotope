from libs.c_pyqt5.window import TransparentWindow


class AIWindow(TransparentWindow):

    def __init__(self):
        super(AIWindow, self).__init__(0, 0, 833, 1333, False)


        pass

    def hear(self):
        # audio_path = resources.output_data("user_audio.wav")
        # vosk = VoskRecognizer(resources.VoskSmallCNModel, audio_path)
        # vosk.recognize()
        # print(WhisperRecognizer('large-v3').audio_to_text(audio_path))
        pass

    pass
