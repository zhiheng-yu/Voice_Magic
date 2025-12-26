from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.storage import SettingsStorage

router = APIRouter()
settings_storage = SettingsStorage()

class SettingsRequest(BaseModel):
    api_key: str
    region: str = "beijing"

@router.post("/api-key")
async def save_settings(request: SettingsRequest):
    try:
        settings_storage.save_api_key(request.api_key)
        settings_storage.save_region(request.region)
        return {"message": "设置保存成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api-key")
async def get_settings():
    try:
        api_key = settings_storage.get_api_key()
        region = settings_storage.get_region()
        
        masked_key = "***" + api_key[-4:] if api_key and len(api_key) > 4 else ""
        
        return {
            "api_key": masked_key,
            "region": region,
            "has_key": bool(api_key)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
