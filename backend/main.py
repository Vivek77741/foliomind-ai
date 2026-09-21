from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, portfolio, copilot
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

app = FastAPI(
    title="FolioMind AI - SnapTrade Copilot Backend",
    description="Backend API services for SnapTrade AI Portfolio Copilot",
    version="1.0.0"
)

# Configure CORS - allow configured frontend, localhost, and all Vercel deployments
origins = [
    settings.FRONTEND_URL,
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(portfolio.router)
app.include_router(copilot.router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "FolioMind AI Backend",
        "environment": settings.ENVIRONMENT,
        "is_demo_mode": settings.SNAPTRADE_CLIENT_ID in ["DEMO_CLIENT_ID", ""]
    }

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "FolioMind AI"}


@app.post("/api/webhook/snaptrade")
async def snaptrade_webhook(request: Request):
    """
    SnapTrade Webhook Handler for reliable, event-driven updates.
    Invalidates cached portfolio data when brokerage accounts sync or disconnect.
    """
    payload = await request.json()
    event_type = payload.get("eventType", "UNKNOWN")
    logger.info(f"Received SnapTrade Webhook: {event_type} | Payload: {payload}")

    # Handle connection events (e.g. CONNECTION_BROKEN, HOLDINGS_UPDATED)
    if event_type == "CONNECTION_BROKEN":
        logger.warning(f"Connection broken for user {payload.get('userId')}. Requiring re-auth.")
    elif event_type == "HOLDINGS_UPDATED":
        logger.info(f"Holdings updated for user {payload.get('userId')}.")

    return {"status": "received", "event_type": event_type}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
