# PolyMentor Architecture

PolyMentor is now a Groq-powered coding tutor chatbot.

## Goal

The system should teach code, write code, identify likely bugs, explain fixes,
and support multiple programming languages. It should not present itself as a
numeric scoring engine.

## Runtime Flow

```text
Website / CLI / API
        |
        v
src.inference.pipeline.PolyMentorPipeline
        |
        v
Groq Chat Completions API
        |
        v
MentorResponse
  - answer
  - suspected_bugs
  - fixed_code
  - lesson
  - next_steps
```

## Main Components

| Component | Role |
| --- | --- |
| `src/inference/pipeline.py` | Builds the tutor prompt, calls Groq, and returns structured mentor output. |
| `src/api/app.py` | Exposes `/chat`, `/review`, and `/teach` endpoints. |
| `src/inference/tutor.py` | Runs an interactive terminal tutor. |
| `src/models/groq_model.py` | Provides a model-facing adapter for the Groq chatbot. |
| `src/models/*_error_detector.py` | Optional local helpers for future prompt context. |
| `website/` | Explains the product, supported languages, Groq setup, and roadmap. |

## Provider

The provider is Groq. Set:

```bash
export GROQ_API_KEY="your_key"
export GROQ_MODEL="llama-3.3-70b-versatile"
```

## No Default Local Training

The old local training path is no longer the primary architecture. Training
files can remain for future experiments, but the default application does not
load `models_saved/best_mentor_model.pt` and does not compute user-facing code
quality scores.
