from faster_whisper import WhisperModel

model = WhisperModel(
    "avazir/faster-distil-whisper-large-v3-ru", device="cuda", compute_type="float16"
)

segments, info = model.transcribe(
    "audio.mp3", language="ru", condition_on_previous_text=False
)
for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
