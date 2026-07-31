from faster_whisper import WhisperModel


RU_MODEL = "avazir/faster-distil-whisper-large-v3-ru"
EN_MODEL = "distil-large-v3"


class Transcriber:
    def __init__(self):
        print("Loading Russian model...")

        self.ru_model = WhisperModel(
            RU_MODEL,
            device="cuda",
            compute_type="float16",
        )

        print("Loading English model...")

        self.en_model = WhisperModel(
            EN_MODEL,
            device="cuda",
            compute_type="float16",
        )

        print("Models loaded.")

    def transcribe(self, audio_path: str, language: str) -> str:
        if language == "ru":
            model = self.ru_model
        elif language == "en":
            model = self.en_model
        else:
            raise ValueError(f"Unsupported language: {language}")

        segments, info = model.transcribe(
            audio_path,
            language=language,
            beam_size=5,
            condition_on_previous_text=False,
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        return text
