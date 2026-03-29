from fastapi import FastAPI
from api.routes_nmap import router as nmap_router
from api.routes_ffuf import router as ffuf_router
from api.routes_subfinder import router as subfinder_router
from api.routes_pipeline import router as pipeline_router # <-- ADD THIS

app = FastAPI(
    title="Automated Recon API",
    description="API for orchestrating security reconnaissance tools",
    version="1.0.0"
)

app.include_router(nmap_router, prefix="/scan", tags=["Nmap"])
app.include_router(ffuf_router, prefix="/scan", tags=["FFUF"])
app.include_router(subfinder_router, prefix="/scan", tags=["Subfinder"])
app.include_router(pipeline_router, prefix="/pipeline", tags=["Automated Pipelines"]) # <-- ADD THIS

@app.get("/health")
async def health_check():
    return {"status": "active", "message": "The Front Desk is open for business."}