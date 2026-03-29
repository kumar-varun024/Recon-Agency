from fastapi import APIRouter
from core.scanner import run_subfinder_scan

router = APIRouter()

@router.get("/subfinder/{target:path}")
async def scan_subdomains(target: str):
    results = await run_subfinder_scan(target)
    return results