import json
from engine.core.caption_engine import CaptionEngine

engine = CaptionEngine()

captions = engine.generate_captions("test_video.mp4")

print(json.dumps(captions, indent=2))