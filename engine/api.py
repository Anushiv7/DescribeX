"""
FastAPI application — thin wrapper around the Caption Engine.

This acts only as an interface. No business logic belongs here.
The engine remains independent and can be used directly via Python.
"""

from __future__ import annotations

import os
import shutil
import tempfile
from typing import Annotated

from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from engine.core.caption_engine import CaptionEngine
from engine.export import burn_captions, export_txt
from engine.utils.download import download_video
from engine.utils.exceptions import DescribeXError

app = FastAPI(
    title="DescribeX API",
    description="API wrapper for the DescribeX caption engine.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = CaptionEngine()


def _cleanup_temp_file(path: str) -> None:
    """Background task to clean up temporary files."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/caption")
async def generate_captions(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(None),
    video_url: Annotated[str, Form()] = None,
) -> JSONResponse:
    """Generate captions for an uploaded video or remote URL."""
    if not video and not video_url:
        raise HTTPException(status_code=400, detail="Must provide either a video file or video_url.")

    tmp_path = None
    if video and video.filename:
        ext = os.path.splitext(video.filename)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            shutil.copyfileobj(video.file, tmp)
            tmp_path = tmp.name
    elif video_url:
        temp_dir = tempfile.mkdtemp()
        background_tasks.add_task(lambda p: shutil.rmtree(p, ignore_errors=True), temp_dir)
        try:
            tmp_path = download_video(video_url, temp_dir)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Failed to download video: {exc}")

    if tmp_path:
        background_tasks.add_task(_cleanup_temp_file, tmp_path)

    try:
        captions = engine.generate_captions(tmp_path)
        return JSONResponse(content=captions)
    except DescribeXError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/export/txt")
async def export_to_txt(
    background_tasks: BackgroundTasks,
    captions: dict[str, str],
) -> FileResponse:
    """Export captions to a TXT file."""
    try:
        fd, path = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        
        output_path = export_txt(captions, path)
        background_tasks.add_task(_cleanup_temp_file, output_path)
        
        return FileResponse(
            path=output_path,
            filename="describex_captions.txt",
            media_type="text/plain",
        )
    except DescribeXError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/export/video")
async def export_burned_video(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
    caption_text: Annotated[str, Form()] = "",
) -> FileResponse:
    """Burn captions onto a video and return the result."""
    if not video.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")
    if not caption_text:
        raise HTTPException(status_code=400, detail="No caption text provided.")

    ext = os.path.splitext(video.filename)[1].lower()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_in:
        shutil.copyfileobj(video.file, tmp_in)
        in_path = tmp_in.name

    fd, out_path = tempfile.mkstemp(suffix=ext)
    os.close(fd)

    background_tasks.add_task(_cleanup_temp_file, in_path)
    background_tasks.add_task(_cleanup_temp_file, out_path)

    try:
        burn_captions(in_path, caption_text, out_path)
        
        return FileResponse(
            path=out_path,
            filename=f"captioned_{video.filename}",
            media_type="video/mp4",
        )
    except DescribeXError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
