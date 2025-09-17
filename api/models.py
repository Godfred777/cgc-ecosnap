from pydantic import BaseModel

class WasteManagemetRequest(BaseModel):
    image: str |None = None #Base64 encoded image
    


class WasteDetectionResponse(BaseModel):
    waste_type: str
    disposal_methods: list[str]
    recycling_options: list[str] | None = None
    safety_precautions: list[str]
    environmental_impact: str | None = None