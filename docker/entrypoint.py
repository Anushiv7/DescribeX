"""
Docker entrypoint for the AMD Developer Hackathon submission.

This script acts as a thin wrapper around the Caption Engine.
It reads tasks from `/input/tasks.json`, processes them using
the engine, and writes the results to `/output/results.json`.
"""

import json
import logging
import os
import sys
import urllib.parse
from engine.utils.download import download_video
from urllib.error import URLError

from engine.core.caption_engine import CaptionEngine
from engine.utils.exceptions import DescribeXError

# Configure basic logging for the Docker container stdout.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | docker | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("entrypoint")


def main() -> None:
    input_path = "/input/tasks.json"
    output_path = "/output/results.json"
    input_dir = "/input"

    if not os.path.isfile(input_path):
        logger.error("Input tasks file not found: %s", input_path)
        sys.exit(1)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse tasks JSON: %s", exc)
        sys.exit(1)

    # Instantiate the core engine.
    try:
        engine = CaptionEngine()
    except Exception as exc:
        logger.error("Failed to initialize CaptionEngine: %s", exc)
        sys.exit(1)

    results = []
    has_errors = False

    for task in tasks:
        task_id = task.get("task_id")
        video_filename = task.get("video")
        video_url = task.get("video_url")
        requested_styles = task.get("styles")

        if not task_id:
            logger.warning("Skipping invalid task without task_id: %s", task)
            results.append({"task_id": task_id, "error": "Invalid task definition (missing task_id)"})
            has_errors = True
            continue

        if not video_filename and not video_url:
            logger.warning("Skipping invalid task %s (no video or video_url)", task_id)
            results.append({"task_id": task_id, "error": "Invalid task definition (missing video and video_url)"})
            has_errors = True
            continue

        # Prioritize video -> video_url -> error
        video_path = None
        downloaded = False
        if video_filename:
            video_path = os.path.join(input_dir, video_filename)
            if not os.path.exists(video_path):
                logger.warning("Local video file not found: %s", video_path)
                if video_url:
                    video_path = None # Fallback to URL
                else:
                    results.append({"task_id": task_id, "error": f"Local video file not found: {video_filename}"})
                    has_errors = True
                    continue

        if not video_path and video_url:
            try:
                video_path = download_video(video_url, input_dir, prefix=f"downloaded_{task_id}_")
                downloaded = True
            except Exception as exc:
                logger.error("Failed to download video for task %s: %s", task_id, exc)
                results.append({"task_id": task_id, "error": f"Failed to download video: {exc}"})
                has_errors = True
                continue

        if not video_path:
             results.append({"task_id": task_id, "error": "Could not determine video path"})
             has_errors = True
             continue

        logger.info("Processing task %s (video: %s)", task_id, video_path)

        try:
            captions = engine.generate_captions(video_path)
            
            # Filter by requested styles if provided, ignoring unsupported styles
            if requested_styles and isinstance(requested_styles, list):
                filtered_captions = {
                    style: text for style, text in captions.items()
                    if style in requested_styles
                }
                captions = filtered_captions
                
            results.append({
                "task_id": task_id,
                "captions": captions
            })
            logger.info("Task %s completed successfully", task_id)
        except DescribeXError as exc:
            logger.error("DescribeXError processing task %s: %s", task_id, exc)
            results.append({"task_id": task_id, "error": str(exc)})
            has_errors = True
        except Exception as exc:
            logger.error("Unexpected error processing task %s: %s", task_id, exc)
            results.append({"task_id": task_id, "error": "Unexpected internal error"})
            has_errors = True
        finally:
            if downloaded and video_path and os.path.exists(video_path):
                try:
                    os.remove(video_path)
                    logger.info("Deleted temporary downloaded video: %s", video_path)
                except Exception as exc:
                    logger.warning("Failed to delete temporary video %s: %s", video_path, exc)

    # Ensure output directory exists (though Docker usually maps it).
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        logger.info("Results written to %s", output_path)
    except Exception as exc:
        logger.error("Failed to write results JSON: %s", exc)
        sys.exit(1)

    if has_errors:
        logger.warning("Execution finished with errors in some tasks.")
        sys.exit(0)  # Still exit 0 so Docker volume map doesn't fail the runner.
    else:
        logger.info("All tasks completed successfully.")
        sys.exit(0)


if __name__ == "__main__":
    main()
