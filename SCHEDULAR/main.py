from fastapi import FastAPI
import threading
from schedular import start_scheduler

app = FastAPI()

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=start_scheduler, daemon=True)
    thread.start()
