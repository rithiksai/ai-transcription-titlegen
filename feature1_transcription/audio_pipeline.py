#This is for transcrbing and diarization of .wav files through the commad prompt
import os
import json
import whisper
from pyannote.audio import Pipeline
from dotenv import load_dotenv

load_dotenv()

# Load Whisper model
whisper_model = whisper.load_model("base")

# Load pyannote diarization pipeline
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
if not HUGGINGFACE_TOKEN:
    raise ValueError("Please set your Hugging Face token in the HUGGINGFACE_TOKEN env variable.")

diarization_pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token=HUGGINGFACE_TOKEN
)

def transcribe_and_diarize(audio_path):
    # Transcribe with Whisper
    whisper_result = whisper_model.transcribe(audio_path, verbose=False)

    # Run diarization
    diarization_result = diarization_pipeline(audio_path)

    # Match speaker segments with transcribed text
    output = []
    for segment, _, speaker in diarization_result.itertracks(yield_label=True):
        segment_text = ""
        for ws in whisper_result.get("segments", []):
            if ws["end"] >= segment.start and ws["start"] <= segment.end:
                segment_text += ws["text"].strip() + " "

        if segment_text.strip():
            output.append({
                "speaker": speaker,
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": segment_text.strip()
            })

    return output

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python audio_pipeline.py <audio_file_path>")
        sys.exit(1)

    audio_path = sys.argv[1]
    result = transcribe_and_diarize(audio_path)
    print(json.dumps(result, indent=2))
