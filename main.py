from dotenv import load_dotenv
load_dotenv() 

from fastapi import FastAPI
from routes import skin, weather, routine
import os
from fastapi.middleware.cors import CORSMiddleware


PERFECTCORP_API_KEY = os.getenv("PERFECTCORP_API_KEY")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(skin.router, prefix="/api/skin")
app.include_router(weather.router, prefix="/api/weather")
app.include_router(routine.router, prefix="/api/routine")

@app.get("/")
def root():
    return {"message": "Skin & Weather API running"}