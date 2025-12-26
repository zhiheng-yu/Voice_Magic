from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.tts_service import TTSService
import json

router = APIRouter()
tts_service = TTSService()

@router.websocket("/tts/streaming")
async def websocket_tts(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            action = message.get("action")
            
            if action == "connect":
                await tts_service.connect(websocket, message)
            elif action == "synthesize":
                await tts_service.synthesize(websocket, message)
            elif action == "close":
                await tts_service.close(websocket)
                break
                
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()
