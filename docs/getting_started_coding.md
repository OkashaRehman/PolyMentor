# PolyMentor — How to Start Coding

> A step-by-step guide for first-time contributors. No prior experience with AI or ML required.

---

## Who This Guide Is For

This guide is for you if:

- You want to contribute to PolyMentor but don't know where to begin.
- You understand basic programming but have never worked on an ML project before.
- You've cloned the repo and are staring at the folder structure wondering what to touch first.

By the end of this guide you will have the project running locally, understand which files do what, and know exactly where to make your first change.

---

## Step 1: Set Up Your Machine

Before writing a single line of code, you need the right tools installed.

### What You Need

| Tool | Why | How to check if you have it |
|---|---|---|
| Python 3.10 or newer | The whole project runs on Python | `python --version` in your terminal |
| Git | To download the code and track changes | `git --version` |
| pip | To install Python packages | `pip --version` |
| A code editor | To read and write code comfortably | See below |

### Recommended Code Editor

Use **VS Code** — it's free, works on every operating system, and has excellent Python support.

Download it from https://code.visualstudio.com

Once installed, add these two extensions (click the Extensions icon on the left sidebar and search for them):
- **Python** (by Microsoft)
- **Pylance** (by Microsoft)

These give you autocomplete, error highlighting, and the ability to run code directly inside the editor.

---

## Step 2: Get the Code onto Your Machine

Open your terminal (Terminal on Mac/Linux, Command Prompt or PowerShell on Windows) and run these commands one at a time:

```bash
# Download the project
git clone https://github.com/your-org/polymentor.git

# Move into the project folder
cd polymentor
```

Now open this folder in VS Code:

```bash
code .
```

You should see the full project tree on the left side of VS Code.

---

## Step 3: Install the Project's Dependencies

The project uses many third-party libraries (PyTorch, Transformers, Tree-sitter, etc.). They are all listed in `requirements.txt`. Install them with:

```bash
pip install -r requirements.txt
pip install -e .
```

The `-e .` flag installs PolyMentor itself in "editable" mode — meaning any changes you make to the source code take effect immediately without reinstalling.

This step may take a few minutes the first time. That's normal.

### Verify the Installation

```bash
python -c "import torch; import transformers; print('All good!')"
```

If you see `All good!` you're ready. If you see an error, re-run `pip install -r requirements.txt` and check that you're using Python 3.10+.

---

## Step 4: Understand the Folder Structure

Before touching anything, take five minutes to read the project layout. Open the folder in VS Code and look at this map:

```
PolyMentor/
│
├── configs/          ← Settings files. Start here to change model behaviour.
├── data/             ← Raw and processed datasets. Don't edit manually.
├── notebooks/        ← Jupyter notebooks for exploration and experiments.
├── src/              ← All the actual code. This is where you'll spend most of your time.
│   ├── data_pipeline/   ← How raw data becomes training data.
│   ├── features/        ← How code is converted into numbers the model understands.
│   ├── models/          ← The ML models themselves.
│   ├── reasoning_engine/← How errors become explanations and hints.
│   ├── training/        ← Training loop — runs the model through examples.
│   ├── evaluation/      ← Measuring how good the model is.
│   ├── inference/       ← The public API. Where external callers enter.
│   └── utils/           ← Small helper functions used everywhere.
├── tests/            ← Automated tests. Run these before submitting any change.
├── scripts/          ← Shell scripts that run common tasks.
└── experiments/      ← Saved results from past training runs.
```

The most important rule: **`src/inference/pipeline.py` is the only public entrypoint.** Everything else is internal. If you are building something that *uses* PolyMentor, only import from `pipeline.py`.

---

## Step 5: Run the Project for the First Time

Do these in order. Each step builds on the last.

### 5a. Prepare the Data

```bash
bash scripts/preprocess.sh
```

This runs the data pipeline: it collects raw code samples, cleans them, tokenises them, and writes `data/processed/train.json`, `val.json`, and `test.json`.

You will see log output as each stage runs. If it completes without errors, your data is ready.

### 5b. Train the Model

```bash
bash scripts/train.sh
```

This trains the error detection model and saves the result to `models_saved/`. Training on CPU is slow — expect 20–60 minutes for a full run. If you have a GPU, training will be much faster.

You don't need to wait for training to finish before exploring the code. Open a second terminal window and keep working.

### 5c. Run the Tutor

```bash
bash scripts/run_tutor.sh
```

This launches the interactive CLI. Paste in a code snippet and press Enter. You should see an error type, an explanation, a hint, and a quality score come back.

If this works, the full pipeline is running correctly on your machine.

---

## Step 6: Run the Tests

Before making any changes, run the test suite once to confirm everything passes on your machine:

```bash
pytest tests/ -v
```

You should see a list of tests with green `PASSED` next to each one. If anything is red, note it down — it was already broken before you touched anything, and it's not your fault.

Get in the habit of running tests before *and* after every change you make.

---

## Step 7: Where to Start Coding

This is the most important section. There are several entry points depending on what you want to work on. Start with the one that matches your interest.

---

### Entry Point A: You Want to Understand the Flow First

**Start here:** `src/inference/pipeline.py`

Read this file top to bottom before touching anything else. It is short — under 100 lines — and it calls every other major component in order. Reading it gives you a map of how all the pieces connect.

Then follow the calls: `pipeline.py` calls `predict.py`, which calls `model_factory.py`, which loads `error_detector.py`. Trace this chain and you'll understand the whole system in an hour.

---

### Entry Point B: You Want to Work on Data

**Start here:** `src/data_pipeline/cleaner.py`

This is the simplest module in the pipeline. It takes raw text and cleans it — strips HTML, normalises whitespace, removes non-code content. The logic is straightforward Python with no ML involved.

Good first tasks here:
- Add a new cleaning rule for a specific noise pattern you notice in the raw data.
- Improve the code block extraction from Stack Overflow HTML.
- Add logging to track how many samples are dropped at each cleaning step.

After `cleaner.py`, move to `dataset_builder.py` to understand how the train/val/test splits are constructed.

---

### Entry Point C: You Want to Work on Features

**Start here:** `src/features/ast_parser.py`

This module takes source code and builds a syntax tree using Tree-sitter. It's a great entry point because it's mostly about understanding Tree-sitter's API rather than ML concepts.

Good first tasks here:
- Add support for a new node type that isn't currently extracted.
- Improve the error recovery behaviour when Tree-sitter encounters malformed code.
- Add tests in `tests/test_data_pipeline.py` for edge cases (empty files, single-line snippets, deeply nested code).

---

### Entry Point D: You Want to Work on the Reasoning Engine

**Start here:** `src/reasoning_engine/error_classifier.py`

This is the concept mapping module — it takes an error type label and maps it to the programming concepts the learner needs to understand. The concept taxonomy is defined in `data/labels/error_types.json`.

Good first tasks here:
- Add a new error type to the taxonomy and map it to existing concepts.
- Improve the concept chain for an existing error type.
- Add a new concept to the hierarchy that an existing error type should link to.

This module has no ML — it's pure logic and data. It's one of the best places to make a meaningful contribution without needing to understand model training.

---

### Entry Point E: You Want to Work on the Models

**Start here:** `src/models/model_factory.py`

The factory is short and shows you how models are loaded and routed. Once you understand it, move to `src/models/error_detector.py` to see the classifier architecture.

Good first tasks here:
- Read the CodeBERT fine-tuning code and add a comment explaining each section.
- Experiment with a different classifier head (a different number of layers, a different activation function) and compare results.
- Add model versioning — right now `model_factory.py` loads a fixed path; make it accept a version tag.

Only tackle this entry point once you're comfortable with PyTorch basics. If you haven't used PyTorch before, work through the official 60-minute beginner tutorial at https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html first.

---

### Entry Point F: You Want to Write Tests

**Start here:** `tests/test_inference.py`

Writing tests is one of the most valuable contributions you can make. The test file for inference is the easiest to read because it tests the public API — you call `pipeline.analyze()` with a code snippet and assert that the output looks right.

Good first tasks here:
- Add a test for a code snippet with a logical error (not just a syntax error).
- Add a test for each supported language (currently Python and JavaScript are well covered; C++ and Java need more tests).
- Add a test that verifies the quality score is always between 0 and 100.

You don't need to understand the internals to write tests. You only need to know what the output *should* look like for a given input.

---

## Step 8: Making Your First Change

Here is the recommended first change for someone completely new to the project. It is small, safe, and touches real code.

### Task: Add a New Entry to the Error Taxonomy

1. Open `data/labels/error_types.json`.
2. Find an error category (e.g. `bad_practice`).
3. Add a new specific error type under it — for example, `hardcoded_password` under `bad_practice`.
4. Open `src/reasoning_engine/error_classifier.py`.
5. Add the concept mapping for your new error type — what programming concept does a hardcoded password violate? (Answer: `security_basics` → `credential_management`.)
6. Open `tests/test_inference.py` (or create `tests/test_error_classifier.py`).
7. Add a test that verifies your new error type maps to the correct concept.
8. Run `pytest tests/ -v` and confirm your new test passes.

That's it. You've made a real, meaningful contribution: the taxonomy is richer, the reasoning engine knows about a new concept, and there's a test to make sure it keeps working.

---

## Step 9: The Development Loop

Every change you make should follow this loop:

```
1. Read the relevant module and its test file.
2. Make your change.
3. Run the tests: pytest tests/ -v
4. Run the linter: flake8 src/ --max-line-length=100
5. If tests pass and linter is clean → open a pull request.
```

Never skip step 3. Tests exist specifically so that changes in one part of the system don't silently break another part.

---

## Step 10: Common Problems and How to Fix Them

### "ModuleNotFoundError: No module named 'src'"

You forgot to install the project in editable mode. Run:
```bash
pip install -e .
```

### "FileNotFoundError: data/processed/train.json not found"

You haven't run the preprocessing step yet. Run:
```bash
bash scripts/preprocess.sh
```

### "RuntimeError: CUDA out of memory"

Your GPU doesn't have enough memory for the batch size configured in `configs/training_config.yaml`. Open that file and reduce `batch_size` from its current value to `4` or `2`.

### "pytest: command not found"

pytest isn't installed. Run:
```bash
pip install pytest
```

### The model runs but the explanations look nonsensical

The explanation model checkpoint hasn't been trained yet (it's currently planned — see the roadmap). The inference pipeline falls back to a template-based explanation. This is expected behaviour for now.

### "Tree-sitter grammar not found for language X"

Tree-sitter requires language grammars to be compiled and available. Run:
```bash
python -c "from src.features.ast_parser import ASTParser; ASTParser.setup_grammars()"
```

---

## Useful Commands at a Glance

```bash
# Install everything
pip install -r requirements.txt && pip install -e .

# Run the full pipeline
bash scripts/preprocess.sh
bash scripts/train.sh
bash scripts/evaluate.sh
bash scripts/run_tutor.sh

# Run tests
pytest tests/ -v

# Run a single test file
pytest tests/test_inference.py -v

# Check code style
flake8 src/ --max-line-length=100

# Try the API directly in Python
python -c "
from src.inference.pipeline import PolyMentorPipeline
mentor = PolyMentorPipeline.from_pretrained('models_saved/best_mentor_model.pt')
result = mentor.analyze('if x = 5: pass', language='python', level='beginner')
print(result.explanation)
"
```

---

## Where to Go Next

Once you've made your first change and the tests pass, here's a suggested learning path through the codebase:

| Week | Focus | Files to Read |
|---|---|---|
| 1 | Understand the full flow | `pipeline.py` → `predict.py` → `model_factory.py` |
| 2 | Understand data | `collector.py` → `cleaner.py` → `dataset_builder.py` |
| 3 | Understand features | `ast_parser.py` → `code_embeddings.py` |
| 4 | Understand the model | `error_detector.py` → `trainer.py` → `metrics.py` |
| 5 | Understand the reasoning engine | `error_classifier.py` → `hint_system.py` → `feedback_scorer.py` |
| 6 | Understand evaluation | `evaluate.py` → `learning_effectiveness_score.py` |

After week 6 you will have a thorough understanding of every layer of the system and be ready to take on larger features independently.

For questions, open an issue on GitHub. For bigger changes, open an issue *before* writing code to align with the team on direction.
