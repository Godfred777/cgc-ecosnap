import os
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import *
from services import *
import logging

app = FastAPI(title='Clean Greeen Connect EcoSnap API', version='1.0.0', debug=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

waste_detection_service = WasteDetectionService()

@app.post("/waste-management", response=WasteDetectionResponse)
async def waste_management(request: WasteManagemetRequest):
    if not request.image:
        raise HTTPException(status_code=400, detail="Image is required")
    
    try:
        response = await waste_detection_service.analyze_waste(image_data=request.image)
        return response
    except Exception as e:
        logger.error(f"Error in waste management: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")