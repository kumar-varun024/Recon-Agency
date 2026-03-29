from fastapi import APIRouter
from core.scanner import run_nmap_scan

router = APIRouter()

@router.get("/nmap/{target:path}")
async def scan_target(target: str):
    results = await run_nmap_scan(target)
    return results