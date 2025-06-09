#This is for transcrbing and diarization of .wav files by exposing a FastAPI endpoint 
import os
import json
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pyannote.audio import Pipeline
from dotenv import load_dotenv
import whisper

# Load env variables
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
if not HUGGINGFACE_TOKEN:
    raise ValueError("Please set the HUGGINGFACE_TOKEN environment variable.")

# Load models
whisper_model = whisper.load_model("base")
diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=HUGGINGFACE_TOKEN)

app = FastAPI()

def transcribe_and_diarize(audio_path: str):
    whisper_result = whisper_model.transcribe(audio_path)
    diarization_result = diarization_pipeline(audio_path)

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

@app.post("/api/transcribe/")
async def transcribe_endpoint(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        result = transcribe_and_diarize(tmp_path)
        os.remove(tmp_path)
        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
