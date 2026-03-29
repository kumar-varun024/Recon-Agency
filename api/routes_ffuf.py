from fastapi import APIRouter
from core.scanner import run_ffuf_scan

router = APIRouter()

@router.get("/ffuf/{target:path}")
async def scan_directories(target: str):
    results = await run_ffuf_scan(target)
    return results
from fastapi import APIRouter, Query
from core.scanner import run_ffuf_scan

router = APIRouter()

# We add the 'wordlist' variable, but give it a default value so it's optional!
@router.get("/ffuf/{target:path}")
async def scan_directories(
    target: str, 
    wordlist: str = Query("/usr/share/wordlists/dirb/common.txt", description="Path to your wordlist")
):
    results = await run_ffuf_scan(target, wordlist)
    return results