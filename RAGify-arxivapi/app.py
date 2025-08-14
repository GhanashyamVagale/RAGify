from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import httpx
import json
import xml.etree.ElementTree as ET
import fitz 
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # ✅ allow all origins
    allow_credentials=False,      # ✅ required when using "*"
    allow_methods=["*"],          # ✅ allow POST, GET, etc.
    allow_headers=["*"],          # ✅ allow Content-Type: application/json
)

ARXIV_API_URL = "https://export.arxiv.org/api/query"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

@app.get('/') 
def home_route():
    return {"msg":"This route works!"}

@app.post("/search_papers/")
async def search_papers(request: Request):
    try:
        body = await request.json()
        title = body.get("title")

        if not title:
            raise HTTPException(status_code=400, detail="Missing 'title' in request body")

        query = f'all:"{title}"'
        url = f"{ARXIV_API_URL}?search_query={query}&start=0&max_results=10"

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, headers=HEADERS, timeout=30.0)

        content_type = response.headers.get("Content-Type", "")
        print("arXiv Response Status:", response.status_code)
        print("Content-Type:", content_type)
        print("URL:", url)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch data from arXiv")

        if "xml" not in content_type:
            raise HTTPException(status_code=500, detail=f"Expected XML response, got {content_type}")

        try:
            root = ET.fromstring(response.text)
        except ET.ParseError as parse_err:
            raise HTTPException(status_code=500, detail=f"Failed to parse XML from arXiv: {str(parse_err)}")

        ns = {'ns': 'http://www.w3.org/2005/Atom'}
        entries = root.findall("ns:entry", ns)

        if not entries:
            return {"papers": [], "message": "No results found from arXiv"}

        papers = []
        for entry in entries[:5]:
            paper_title = entry.find("ns:title", ns).text.strip()
            link = entry.find("ns:id", ns).text.strip()
            paper_id = link.split("/")[-1]
            pdf_link = f"https://export.arxiv.org/pdf/{paper_id}.pdf"
            papers.append({"title": paper_title, "link": pdf_link})

        return {"papers": papers}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@app.post("/extract_pdf_text/")
async def extract_pdf_text(request: Request):
    try:
        body = await request.json()
        paper_url = body.get("url")

        if not paper_url:
            raise HTTPException(status_code=400, detail="Missing 'url' in request body")

        if not paper_url.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Provided URL is not a PDF")

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(paper_url, timeout=30.0)

        content_type = response.headers.get("Content-Type", "")
        print("Response Status:", response.status_code)
        print("Content-Type:", content_type)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch the PDF file")

        if "application/pdf" not in content_type:
            raise HTTPException(
                status_code=400,
                detail=f"Expected PDF but got {content_type} instead. The URL may be blocked or incorrect.",
            )

        pdf_text = extract_text_from_pdf(response.content)
        return {"text": pdf_text}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


def extract_text_from_pdf(pdf_bytes):
    """Extract text from a PDF file using PyMuPDF."""
    text = ""
    with fitz.open("pdf", pdf_bytes) as pdf:
        for page in pdf:
            text += page.get_text("text") + "\n\n"
    return text.strip()

if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=4000)