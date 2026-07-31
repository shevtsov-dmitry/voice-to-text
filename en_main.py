from faster_whisper import WhisperModel

model = WhisperModel(
    "distil-large-v3",
    device="cuda",
    compute_type="float16",
)

segments, info = model.transcribe(
    "audio_en.mp3",
    beam_size=5,
    language="en",
    condition_on_previous_text=False,
)

with open("transcription.txt", "w", encoding="utf-8") as f:
    for segment in segments:
        f.write(segment.text.strip() + "\n")

print("Saved to transcription.txt")
