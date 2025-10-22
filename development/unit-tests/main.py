import sys, os
from pathlib import Path
from development.meeting_summarizer.MeetingSummarizer import MeetingSummarizer
import json

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
base_dir = Path(__file__).resolve().parents[1]
print(base_dir)
transcript_path = base_dir / "test-data" / "meeting-summarizer.txt"

with open(transcript_path, "r") as file:
    transcript = file.read().strip()

summarizer = MeetingSummarizer()
summary,action_items = summarizer.summarize(transcript)
print(summary)
print("JSON:")
print(json.dumps(action_items, indent=2))