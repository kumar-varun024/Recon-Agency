from fastapi import APIRouter
from core.scanner import run_recon_pipeline

router = APIRouter()

@router.get("/full-recon/{target:path}")
async def full_recon_pipeline(target: str):
    # This hits our new double-tool function
    results = await run_recon_pipeline(target)
    return results