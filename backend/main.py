from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import observer # Import the file your friend just edited

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "DECEPTOR AI Backend is running! Go to /docs to test."}
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/event")
def receive_event(event: dict):
    # This calls the function in your friend's file!
    assessment = observer.assess(event, []) 
    return {"status": "success", "assessment": assessment}