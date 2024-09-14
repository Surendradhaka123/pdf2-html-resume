from fastapi import FastAPI, File, Form, UploadFile,HTTPException,Depends
from fastapi.responses import HTMLResponse, StreamingResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
import io
from openai import OpenAI
import uuid
import uvicorn
from io import BytesIO
from PyPDF2 import PdfReader


def read_pdf(file: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(file))
        full_text = []
        for page in reader.pages:
            full_text.append(page.extract_text())
        return '\n'.join(full_text)
    except Exception as e:
        raise ValueError(f"Failed to read PDF: {str(e)}")



app = FastAPI()
templates = Jinja2Templates(directory="templates")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"], 
    allow_headers=["Content-Type", "Authorization"],
)
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

async def get_session(request: Request):
    return request.session

html_storage = {}

@app.get("/", response_class=HTMLResponse)
async def index():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.post("/upload")
async def upload_file(
    pdfFile: UploadFile = File(...),
    apiKey: str = Form(...),
    session: dict = Depends(get_session)
):
    
    if not pdfFile.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    session["api_key"] = apiKey
    stored_api_key = session.get("api_key")

    if not stored_api_key:
        raise HTTPException(status_code=400, detail="API key is missing")

    client = OpenAI(api_key=stored_api_key)

    content = await pdfFile.read()
    try:
       
        full_text = read_pdf(content)
        try:
            completion = client.chat.completions.create(seed=455,
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Generate a formatted and explained HTML resume from given resume pdf text."},
                {"role": "user", "content":full_text}])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

        response=completion.choices[0].message.content
        resume_html = response

        unique_id = str(uuid.uuid4())
        html_storage[unique_id] = resume_html

        return JSONResponse({"view_url": f"/view/{unique_id}", "download_url": f"/download/{unique_id}"})
    
    
    except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
    
    
@app.get("/view/{unique_id}", response_class=HTMLResponse)
async def view_resume(unique_id: str):
    resume_html = html_storage.get(unique_id)
    if resume_html:
        return HTMLResponse(content=resume_html, media_type="text/html")
    else:
        raise HTTPException(status_code=404, detail="Resume not found")

@app.get("/download/{unique_id}")
async def download_resume(unique_id: str):
    resume_html = html_storage.get(unique_id)
    if resume_html:
        return StreamingResponse(
            io.BytesIO(resume_html.encode("utf-8")),
            media_type="text/html",
            headers={"Content-Disposition": "attachment; filename=resume.html"}
        )
    else:
        raise HTTPException(status_code=404, detail="Resume not found")
    


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
