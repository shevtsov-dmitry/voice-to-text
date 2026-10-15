from faster_whisper import WhisperModel

model = WhisperModel(
    "avazir/faster-distil-whisper-large-v3-ru", device="cuda", compute_type="float16"
)

segments, info = model.transcribe(
    "/home/shd/tmp/voice.wav", language="ru", condition_on_previous_text=False
)
for segment in segments:
    print("%s" % (segment.text))
