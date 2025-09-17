import json
from langchain.llms import GoogleGemini
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
import base64
from io import BytesIO
from PIL import Image
import os
import logging

logger = logging.getLogger(__name__)

class WasteDetectionService:
    def __init__(self):
        self.llm = GoogleGemini(
            model="gemini-pro",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["input_content"],
            template="""
            Analyze this waste material and provide detailed information about:
            1. Waste type (e.g., plastic, organic, electronic, hazardous)
            2. Safe disposal methods
            3. Recycling options if applicable
            4. Safety precautions
            5. Environmental impact
            
            Provide the response in a proper JSON format with these keys:
            - waste_type
            - disposal_methods (array)
            - recycling_options (array, optional)
            - safety_precautions (array)
            - environmental_impact (string)
            
            Input: {input_content}
            """
        )
    
    async def analyze_waste(self, image_data: str | None = None):
        try:
             # Process image
            image = self._process_image(image_data)
            input_content = f"Image analysis of waste material: {image}"
            
            # Create prompt
            prompt = self.prompt_template.format(input_content=input_content)
            
            # Get response from Gemini
            response = self.llm([HumanMessage(content=prompt)])
            
            # Parse response (assuming it's in JSON format)
            # In a real implementation, you might need more sophisticated parsing
            return self._parse_gemini_response(response.content)
            
        except Exception as e:
            logger.error(f"Error in waste analysis: {str(e)}")
            raise
    
    def _process_image(self, image_data: str):
        """Process base64 image data for analysis"""
        try:
            # Remove data URL prefix if present
            if "," in image_data:
                image_data = image_data.split(",")[1]
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            
            # For Gemini, we might need to convert to text description
            # or use a multimodal approach. This is a simplified version.
            return "Image of waste material for analysis"
            
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise
    
    def _parse_gemini_response(self, response_text: str):
        """Parse the response from Gemini into structured data"""
        try:
            # The response from Gemini is expected to be a JSON string.
            # We need to remove the markdown syntax for JSON code blocks.
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            return json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Gemini response: {e}")
            # Handle cases where the response is not valid JSON
            # You might want to return a default error structure
            # or attempt a more lenient parsing.
            return {
                "error": "Failed to parse response from Gemini",
                "details": str(e)
            }
