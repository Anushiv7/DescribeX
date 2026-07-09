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
        task_id = task.get("id")
        video_filename = task.get("video")

        if not task_id or not video_filename:
            logger.warning("Skipping invalid task: %s", task)
            results.append({"id": task_id, "error": "Invalid task definition"})
            has_errors = True
            continue

        video_path = os.path.join(input_dir, video_filename)
        logger.info("Processing task %s (video: %s)", task_id, video_path)

        try:
            captions = engine.generate_captions(video_path)
            results.append({
                "id": task_id,
                "captions": captions
            })
            logger.info("Task %s completed successfully", task_id)
        except DescribeXError as exc:
            logger.error("DescribeXError processing task %s: %s", task_id, exc)
            results.append({"id": task_id, "error": str(exc)})
            has_errors = True
        except Exception as exc:
            logger.error("Unexpected error processing task %s: %s", task_id, exc)
            results.append({"id": task_id, "error": "Unexpected internal error"})
            has_errors = True

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
