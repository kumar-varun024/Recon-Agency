from fastapi import APIRouter
from core.scanner import run_ffuf_scan

router = APIRouter()

@router.get("/scan/ffuf/{target:path}")
async def scan_target(target: str):
    results = await run_ffuf_scan(target)
    return results