from fastapi import FastAPI, Request
from pydantic import BaseModel
import time
import asyncio

app = FastAPI()

class ResponseModel(BaseModel):
    message: str
    timestamp: float
    tokens: int

@app.get("/benchmark")
async def benchmark(request: Request, tokens: int = 10):
    # Simulate processing time
    start_time = time.time()
    await asyncio.sleep(0.01)  # Simulating I/O operation
    end_time = time.time()
    return {"message": "Success", "timestamp": end_time, "tokens": tokens} # Retun in Json format

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)