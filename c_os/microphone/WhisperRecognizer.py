import whisper


class WhisperRecognizer:

    def __init__(self, model_size='base'):
        self.model = whisper.load_model(model_size)
        pass

    def audio_to_text(self, audio_path: str) -> str:
        result = self.model.transcribe(
            audio_path,
            fp16=False,
            condition_on_previous_text=True,
        )
        return result['text']

    pass
