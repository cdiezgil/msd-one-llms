from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("server.main:app", host="0.0.0.0", port=5000, reload=True)
