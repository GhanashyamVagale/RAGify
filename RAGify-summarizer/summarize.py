from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# ✅ Move model to CPU and optimize precision
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device).half()  # Convert to FP16 for faster inference

def summarize_text(text, max_length=512, min_length=100, num_beams=4, length_penalty=0.8):
    """
    Summarizes text using T5-Small.
    """
    input_text = "summarize: " + text
    inputs = tokenizer(input_text, return_tensors="pt", max_length=1024, truncation=True)

    inputs = {key: val.to(device) for key, val in inputs.items()}

    with torch.no_grad(): 
        summary_ids = model.generate(
            inputs["input_ids"],
            num_beams=num_beams,
            max_length=max_length,
            min_length=min_length,
            length_penalty=length_penalty,
            early_stopping=True
        )

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)