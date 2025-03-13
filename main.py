import os
import gc
import torch
import aiofiles
import whisperx
import nest_asyncio
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from deep_translator import GoogleTranslator
from langchain_community.llms import Ollama

# ✅ Force CPU since MPS is NOT supported
device = "cpu"
batch_size = 16  # Adjust based on system memory
compute_type = "float32"  # Use float32 for better compatibility

print(f"Using device: {device}")

# ✅ Load WhisperX model (Forced CPU)
whisper_model = whisperx.load_model("large-v3", device=device, compute_type=compute_type)

# ✅ FastAPI App
app = FastAPI()

# ✅ Initialize Ollama LLM
ollama = Ollama(base_url="http://localhost:11434", model="mistral")

# ✅ Directory for saving uploaded audio files
AUDIO_FILES_DIRECTORY = "static/audio_files"
os.makedirs(AUDIO_FILES_DIRECTORY, exist_ok=True)

# 🔹 **Audio Transcription & Analysis Endpoint**
@app.post("/analyze-audio")
async def analyze_audio(file: UploadFile = File(...), analysis_type: str = "Summary of Call"):
    try:
        # ✅ Save uploaded file
        file_path = os.path.join(AUDIO_FILES_DIRECTORY, file.filename)
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(await file.read())

        # ✅ Load & Transcribe Audio
        audio = whisperx.load_audio(file_path)
        result = whisper_model.transcribe(audio, batch_size=batch_size, language="hi")

        # ✅ Load Alignment Model
        align_model, metadata = whisperx.load_align_model(language_code="hi", device=device)
        aligned_result = whisperx.align(result["segments"], align_model, metadata, audio, device)

        # ✅ Extract & Translate Text
        full_transcription = " ".join([seg["text"] for seg in aligned_result['segments']])
        translated_text = GoogleTranslator(source="hi", target='en').translate(full_transcription)

        # ✅ Analyze using Ollama
        analysis_prompt = f"Analyze this conversation: {translated_text} for {analysis_type}"
        analysis = ollama.invoke(analysis_prompt)  # Corrected function call

        # ✅ Clean Up
        gc.collect()
        del align_model, metadata

        return JSONResponse(content={"transcription": full_transcription, "translated": translated_text, "analysis": analysis})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# ✅ Run with: uvicorn main:app --reload
