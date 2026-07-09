"""
Prompting — Prompt templates, loading, and construction.

Prompt templates are stored independently from Python source code
to enable rapid experimentation without modifying engine implementation.
"""

from engine.prompting.builder import build_scene_prompt, build_style_prompt
from engine.prompting.loader import load_template

__all__ = [
    "build_scene_prompt",
    "build_style_prompt",
    "load_template",
]
