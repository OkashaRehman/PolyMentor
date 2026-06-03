"""
Fine-tune a small local PolyMentor chatbot adapter.

This script is intentionally separate from the Groq runtime. Groq remains the
default production model, while this creates a local LoRA adapter checkpoint for
experiments on an NVIDIA GPU such as an RTX 4050.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

import torch
from datasets import Dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)


LANGUAGE_BY_SUFFIX = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".c": "c",
    ".h": "c/cpp",
    ".hpp": "cpp",
    ".rs": "rust",
    ".go": "go",
    ".php": "php",
    ".rb": "ruby",
    ".swift": "swift",
    ".kt": "kotlin",
    ".sql": "sql",
    ".html": "html",
    ".css": "css",
}


def load_json_records(path: Path) -> list[dict[str, Any]]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception:
        return []
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        return [data]
    return []


def sample_to_training_text(sample: dict[str, Any], tokenizer: AutoTokenizer) -> str:
    language = sample.get("language", "code")
    level = sample.get("difficulty") or sample.get("difficulty_level") or "beginner"
    code = sample.get("code", "").strip()
    errors = ", ".join(sample.get("error_types") or [sample.get("error_type", "unknown")])
    explanation = sample.get("explanation", "Explain the issue clearly and teach the concept.")
    concept = sample.get("concept_taught", "Programming concept")
    hints = sample.get("hint_steps", [])
    hints_text = "\n".join(f"- {hint}" for hint in hints)

    user = (
        f"I am a {level} learner. Review this {language} code, identify likely "
        f"bugs, explain the concept, and show how to fix my thinking.\n\n"
        f"```{language}\n{code}\n```"
    )
    assistant = (
        f"Likely bugs:\n- {errors}\n\n"
        f"Explanation:\n{explanation}\n\n"
        f"Lesson:\n{concept}\n\n"
        f"Next steps:\n{hints_text or '- Try a small test case and trace the code line by line.'}"
    )
    return render_chat(tokenizer, user, assistant)


def vendor_to_training_text(path: Path, tokenizer: AutoTokenizer, max_chars: int) -> str | None:
    language = LANGUAGE_BY_SUFFIX.get(path.suffix.lower())
    if not language:
        return None
    try:
        code = path.read_text(encoding="utf-8", errors="ignore").strip()
    except Exception:
        return None
    if len(code) < 80:
        return None
    code = code[:max_chars]
    user = (
        f"Teach me how to read this {language} code snippet. Explain the syntax "
        "patterns and what a learner should notice.\n\n"
        f"```{language}\n{code}\n```"
    )
    assistant = (
        "This is a reference code-reading example. Focus on the structure, "
        "the names, the control flow, and the language syntax. A good way to "
        "study it is to identify the inputs, the important declarations, the "
        "main operations, and any edge cases before changing anything."
    )
    return render_chat(tokenizer, user, assistant)


def render_chat(tokenizer: AutoTokenizer, user: str, assistant: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are PolyMentor, a coding tutor chatbot. Teach code, help "
                "identify likely bugs, explain fixes clearly, and avoid numeric "
                "quality scores."
            ),
        },
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]
    if getattr(tokenizer, "chat_template", None):
        return tokenizer.apply_chat_template(messages, tokenize=False)
    return (
        "System: "
        + messages[0]["content"]
        + "\n\nUser: "
        + user
        + "\n\nAssistant: "
        + assistant
    )


def build_texts(args: argparse.Namespace, tokenizer: AutoTokenizer) -> list[str]:
    texts: list[str] = []
    for pattern in args.data_globs:
        for path in sorted(Path().glob(pattern)):
            for sample in load_json_records(path):
                if sample.get("code"):
                    texts.append(sample_to_training_text(sample, tokenizer))

    if args.include_vendor:
        vendor_files = []
        for suffix in LANGUAGE_BY_SUFFIX:
            vendor_files.extend(Path("vendor").rglob(f"*{suffix}"))
        random.Random(args.seed).shuffle(vendor_files)
        for path in vendor_files[: args.max_vendor_files]:
            text = vendor_to_training_text(path, tokenizer, args.max_vendor_chars)
            if text:
                texts.append(text)

    random.Random(args.seed).shuffle(texts)
    return texts


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune PolyMentor chatbot LoRA adapter.")
    parser.add_argument("--base-model", default="Qwen/Qwen2.5-Coder-0.5B-Instruct")
    parser.add_argument("--output-dir", default="models_saved/polymentor-chatbot-lora")
    parser.add_argument("--epochs", type=float, default=3)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--max-length", type=int, default=1024)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--include-vendor", action="store_true")
    parser.add_argument("--max-vendor-files", type=int, default=200)
    parser.add_argument("--max-vendor-chars", type=int, default=2400)
    parser.add_argument(
        "--data-globs",
        nargs="+",
        default=[
            "data/raw/*.json",
            "data/raw_samples/*.json",
            "data/processed/*.json",
        ],
    )
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise SystemExit(
            "CUDA is not available in this Python environment. Install a CUDA "
            "PyTorch build before training on the RTX 4050."
        )

    print(f"CUDA device: {torch.cuda.get_device_name(0)}")
    print(f"Base model: {args.base_model}")

    tokenizer = AutoTokenizer.from_pretrained(args.base_model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    texts = build_texts(args, tokenizer)
    if not texts:
        raise SystemExit("No training examples found. Add JSON samples under data/.")

    dataset = Dataset.from_dict({"text": texts})

    def tokenize(batch: dict[str, list[str]]) -> dict[str, Any]:
        return tokenizer(
            batch["text"],
            truncation=True,
            max_length=args.max_length,
            padding=False,
        )

    tokenized = dataset.map(tokenize, batched=True, remove_columns=["text"])

    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
    )
    model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.learning_rate,
        fp16=True,
        logging_steps=5,
        save_strategy="epoch",
        save_total_limit=3,
        report_to=[],
        remove_unused_columns=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
    )
    trainer.train()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    (output_dir / "training_manifest.json").write_text(
        json.dumps(
            {
                "base_model": args.base_model,
                "examples": len(texts),
                "include_vendor": args.include_vendor,
                "cuda_device": torch.cuda.get_device_name(0),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Saved PolyMentor LoRA checkpoint to {output_dir}")


if __name__ == "__main__":
    main()
