from fastapi import FastAPI, HTTPException, Body
from deep_translator import GoogleTranslator
import uvicorn
from typing import Dict, Optional

app = FastAPI(title="Translation API", description="A simple API for text translation")

# Simple dictionaries instead of Pydantic models

@app.post("/translate")
async def translate(
    text: str = None, 
    source: str = "auto", 
    dest: str = "en",
    payload: Optional[Dict] = Body(None)
):
    """
    Translate text from source language to destination language
    
    - **text**: Text to translate
    - **source**: Source language code (default: auto-detect)
    - **dest**: Destination language code (default: en)
    """
    try:
        # If JSON payload is provided, use it instead of query parameters
        if payload:
            text = payload.get("text", text)
            source = payload.get("source", source)
            dest = payload.get("dest", dest)
        
        if not text:
            raise HTTPException(status_code=400, detail="Text to translate is required")
            
        # Use deep_translator's GoogleTranslator
        translator = GoogleTranslator(source=source if source != "auto" else "auto", target=dest)
        translated_text = translator.translate(text)
        
        return {
            "translated_text": translated_text,
            "source_language": source,
            "destination_language": dest,
            "original_text": text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Translation API",
        "usage": "POST /translate with text, source language, and destination language"
    }

@app.get("/languages")
def get_languages():
    """Get a list of supported languages"""
    # deep_translator's GoogleTranslator supported languages
    languages = GoogleTranslator.get_supported_languages(as_dict=True)
    return languages

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
