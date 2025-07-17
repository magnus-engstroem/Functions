import torch
from transformers import MarianMTModel, MarianTokenizer

def load_model(src_lang="no", tgt_lang="de"):
    model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    return tokenizer, model, device

def translate(text, tokenizer, model, device):
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)
    translated = model.generate(**tokens)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

# Example usage
tokenizer, model, device = load_model("no", "en")
print(translate("Hvordan går det?", tokenizer, model, device))
