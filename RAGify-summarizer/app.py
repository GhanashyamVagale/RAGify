from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import httpx
from summarize import summarize_text 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # ✅ allow all origins
    allow_credentials=False,      # ✅ required when using "*"
    allow_methods=["*"],          # ✅ allow POST, GET, etc.
    allow_headers=["*"],          # ✅ allow Content-Type: application/json
)


@app.get('/') 
def home_route():
    return {"msg":"This route works!"}

@app.post('/summarize_paper/')
async def summarize_paper(request: Request):
    try:
        body = await request.json()
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:4000/extract_pdf_text/", json=body)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to extract text from PDF")
        
        text = response.json().get("text", "")
        if not text:
            raise HTTPException(status_code=500, detail="No text extracted from PDF")
        
        summary = summarize_text(text)

        return {"summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=3001)