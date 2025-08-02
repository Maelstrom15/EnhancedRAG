"""Lightweight Gemini (Google Generative AI) chat wrapper.
Reads `GEMINI_API_KEY` from environment/.env.
"""
from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root if present
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env", override=False)
from typing import List, Dict

import google.generativeai as genai

# Configure Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

genai.configure(api_key=API_KEY)  # type: ignore[attr-defined]
MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")




def chat(messages: List[Dict[str, str]], **kwargs) -> str:
    """Return assistant content from chat completion using Gemini."""
    temperature = kwargs.get("temperature", 0)
    max_tokens = kwargs.get("max_tokens", 512)

    model = genai.GenerativeModel(MODEL)
    prompt = "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in messages)
    response = model.generate_content(
        prompt,
        generation_config={"temperature": temperature, "max_output_tokens": max_tokens},
    )
    return response.text


