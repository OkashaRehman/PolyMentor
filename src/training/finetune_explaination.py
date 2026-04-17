from transformers import T5ForConditionalGeneration, AutoTokenizer, Seq2SeqTrainer
from transformers import Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
from datasets import Dataset
import json

# Load your annotated explanation pairs
with open("data/processed/train.json") as f:
    train_data = json.load(f)

model_name = "Salesforce/codet5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)


def preprocess(sample):
    error_label = sample["error_types"][0] if sample["error_types"] else "unknown"
    prompt = f"explain error: [{error_label}]\ncode:\n{sample['code']}"
    target = sample["explanation"]

    model_inputs = tokenizer(
        prompt, max_length=512, truncation=True, padding="max_length"
    )
    labels = tokenizer(target, max_length=256, truncation=True, padding="max_length")
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


dataset = Dataset.from_list(train_data)
tokenized = dataset.map(preprocess)

args = Seq2SeqTrainingArguments(
    output_dir="models_saved/explanation_model",
    num_train_epochs=5,
    per_device_train_batch_size=8,
    learning_rate=5e-5,
    predict_with_generate=True,
    save_strategy="epoch",
    fp16=True,
)

trainer = Seq2SeqTrainer(
    model=model,
    args=args,
    train_dataset=tokenized,
    tokenizer=tokenizer,
    data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
)

trainer.train()
model.save_pretrained("models_saved/explanation_model/final")
tokenizer.save_pretrained("models_saved/explanation_model/final")
