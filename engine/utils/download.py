import os
import urllib.request
import urllib.parse
from engine.utils.logging import get_logger

logger = get_logger(__name__)

def download_video(video_url: str, output_dir: str, prefix: str = "downloaded_") -> str:
    """Download a video from a remote URL to a local directory.
    
    Args:
        video_url: The URL of the video to download.
        output_dir: The directory to save the downloaded file.
        prefix: Prefix for the filename if one cannot be derived from the URL.
        
    Returns:
        The absolute path to the downloaded video file.
        
    Raises:
        Exception: If the download fails.
    """
    parsed_url = urllib.parse.urlparse(video_url)
    filename = os.path.basename(parsed_url.path) or f"{prefix}video.mp4"
    video_path = os.path.join(output_dir, filename)
    
    logger.info("Downloading remote video from %s to %s", video_url, video_path)
    try:
        urllib.request.urlretrieve(video_url, video_path)
        return video_path
    except Exception as exc:
        logger.error("Failed to download video from %s: %s", video_url, exc)
        raise
