from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from development.meeting_summarizer.MeetingSummarizer import MeetingSummarizer
import uvicorn

app = FastAPI(title="Meeting Summarizer API", version="1.0")

# Initialize your summarizer once (to reuse the same OpenAI client)
summarizer = MeetingSummarizer()


def read_file(file: UploadFile) -> str:
    """Helper function to read uploaded file and return plain text"""
    try:
        content = file.file.read().decode("utf-8").strip()
        return content
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or unreadable file format")


@app.post("/summarize")
async def get_summary(file: UploadFile = File(...)):
    """
    Upload a meeting transcript text file and get its summary.
    """
    transcript = read_file(file)
    summary, _ = summarizer.summarize(transcript)
    return JSONResponse(content={"summary": summary})


@app.post("/action-items")
async def get_action_items(file: UploadFile = File(...)):
    """
    Upload a meeting transcript text file and get extracted action items.
    """
    transcript = read_file(file)
    _, actions = summarizer.summarize(transcript)
    return JSONResponse(content={"action_items": actions})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2222)