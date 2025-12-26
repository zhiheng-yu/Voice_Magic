import os
import json
import base64
import requests
from dotenv import load_dotenv
from utils.storage import VoiceStorage

load_dotenv()

class VoiceDesignService:
    def __init__(self):
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        self.storage = VoiceStorage("data/voices.json")
        self.voice_design_url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"
        
        self.target_model = "qwen3-tts-vd-realtime-2025-12-16"
    
    def create_custom_voice(self, voice_prompt, preview_text="你好，这是我的声音。", preferred_name=None, display_name=None):
        if not self.api_key:
            raise ValueError("未找到API Key，请先配置")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "qwen-voice-design",
            "input": {
                "action": "create",
                "target_model": self.target_model,
                "voice_prompt": voice_prompt,
                "language": "zh"
            },
            "parameters": {
                "sample_rate": 24000,
                "response_format": "wav"
            }
        }
        
        if preview_text:
            data["input"]["preview_text"] = preview_text
        
        if preferred_name:
            data["input"]["preferred_name"] = preferred_name
        
        try:
            response = requests.post(self.voice_design_url, headers=headers, json=data, timeout=60)
            
            print(f"API响应状态码: {response.status_code}")
            print(f"API响应内容: {response.text[:500]}")
            
            response.raise_for_status()
            result = response.json()
            
            if result.get("output"):
                voice_name = result["output"].get("voice")
                base64_audio = result["output"]["preview_audio"]["data"]
                audio_bytes = base64.b64decode(base64_audio)
                
                preview_filename = f"{voice_name}_preview.wav"
                preview_file = f"previews/{preview_filename}"
                os.makedirs("previews", exist_ok=True)
                with open(preview_file, "wb") as f:
                    f.write(audio_bytes)
                
                self.storage.add_voice(
                    voice_name=voice_name,
                    description=voice_prompt,
                    display_name=display_name or preferred_name or voice_name,
                    preview_file=preview_filename
                )
                
                return {
                    "voice_name": voice_name,
                    "description": voice_prompt,
                    "display_name": display_name or preferred_name or voice_name,
                    "preview_file": preview_filename,
                    "created_at": result.get("created_at", "")
                }
            else:
                raise Exception(f"创建失败: {result}")
                
        except requests.exceptions.RequestException as e:
            print(f"网络请求错误: {e}")
            print(f"响应内容: {response.text if 'response' in locals() else 'N/A'}")
            raise Exception(f"网络请求发生错误: {e}")
        except Exception as e:
            print(f"处理错误: {e}")
            import traceback
            traceback.print_exc()
            raise Exception(f"请求失败: {e}")
    
    def list_voices(self):
        voices = self.storage.list_voices()
        return voices
    
    def delete_voice(self, voice_name):
        return self.storage.delete_voice(voice_name)
