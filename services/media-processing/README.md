# Media Processing Service

Deterministic, dependency-free MVP logic for field media. **No real vision or
transcription models** are called — these are mocks with stable output.

## Files
- `photo_quality.py` — `assess_photo()` / `assess_photos()` → quality verdicts
  (`accepted` / `documentation_only` / `needs_retake` / `rejected`) + field feedback.
- `voice_metadata.py` — `structure_voice_note()` / `structure_voice_notes()` →
  transcript (mock), structured observations, confidence, follow-up question.

## Hard rules
- No mineral identification. No claims of value from any image or audio.
- Photo/voice/transcript data is RESTRICTED — never exposed publicly.

## Try it
```bash
python3 services/media-processing/photo_quality.py
python3 services/media-processing/voice_metadata.py
```
