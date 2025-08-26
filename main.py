from fastapi import FastAPI
import aiohttp
import asyncio
from contextlib import asynccontextmanager

app = FastAPI()

TARGET_URL = "https://luco-share-io.onrender.com/"


async def ping_task():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(TARGET_URL) as response:
                    status = response.status
                    print(f"Pinged {TARGET_URL}, status: {status}")
            except Exception as e:
                print(f"Error pinging {TARGET_URL}: {e}")
            await asyncio.sleep(12 * 60)  # Wait 12 minutes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the ping task on startup
    task = asyncio.create_task(ping_task())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)

# Health check endpoint
@app.get("/health")
async def health_check():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("https://lucoshare-pinger.onrender.com/heath") as response:
                status = response.status
                return {"status": "healthy", "self_ping_status": status}
        except Exception as e:
            return {"status": "healthy", "self_ping_error": str(e)}


@app.get("/")
async def root():
    return {"message": "FastAPI app is running"}
