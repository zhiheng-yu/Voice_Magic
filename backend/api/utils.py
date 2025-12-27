from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import re
try:
    from pypinyin import pinyin, Style
    HAS_PYPINYIN = True
except Exception:
    HAS_PYPINYIN = False

router = APIRouter()

class PinyinRequest(BaseModel):
    text: str

@router.post("/pinyin")
async def to_pinyin(req: PinyinRequest):
    s = req.text or ""
    if not s:
        return {"slug": ""}
    if HAS_PYPINYIN:
        py = pinyin(s, style=Style.NORMAL, strict=False)
        flat = "".join("".join(x) for x in py)
    else:
        flat = s
    slug = re.sub(r"[^a-zA-Z0-9]+", "", flat).lower()[:16]
    if not slug:
        slug = f"voice-{len(s)}"
    return {"slug": slug}
