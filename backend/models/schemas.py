from pydantic import BaseModel
from typing import Optional

class VoiceCreate(BaseModel):
    voice_name: str
    description: str
    preview_file: Optional[str] = None
    audio_file: Optional[str] = None
    created_at: str

class VoiceResponse(BaseModel):
    voice_name: str
    description: str
    preview_file: Optional[str] = None
    audio_file: Optional[str] = None
    created_at: str

class TTSRequest(BaseModel):
    text: str
    voice_name: Optional[str] = None
    voice_type: str = "design"
