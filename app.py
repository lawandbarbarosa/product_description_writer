from fastapi import FastAPI, HTTPException
import os
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

from main import agent


load_dotenv()

app = FastAPI(title = 'SimkoAI Product Description Generator')


class Product_request(BaseModel):
    product_name: str
    product_category: str
    key_features: List[str]
    target_audience: str
    tone: str

class Product_response(BaseModel):
    research_notes: str
    draft_description: str
    final_description: str


@app.get("/")
def read_root():
    return {"Status": "Simko API is online", "version": "SIMKO 1.0"}

@app.post("/generate", response_model=Product_response)
async def generate_description(request: Product_request):
    """
    Triggers the LangGraph agent to research, draft, and refine 
    a product description based on user input.
    """
    try:
        initial_state = {
            "product_name": request.product_name,
            "product_category": request.product_category,
            "key_features": request.key_features,
            "target_audience": request.target_audience,
            "tone": request.tone,
            "research_notes": None,
            "draft_description": None,
            "final_description": None
        }

        result = agent.invoke(initial_state)


        return Product_response(
            research_notes=result['research_notes'],
            draft_description=result['draft_description'],
            final_description=result['final_description']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port = 8001)