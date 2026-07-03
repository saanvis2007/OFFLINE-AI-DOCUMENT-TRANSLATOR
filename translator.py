from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Offline multilingual AI model
MODEL_NAME = "facebook/nllb-200-distilled-600M"

# Language Codes
LANGUAGE_CODES = {
    "English": "eng_Latn",
    "Hindi": "hin_Deva",
    "French": "fra_Latn",
    "German": "deu_Latn",
    "Spanish": "spa_Latn",
    "Italian": "ita_Latn",
    "Portuguese": "por_Latn",
    "Russian": "rus_Cyrl",
    "Chinese": "zho_Hans",
    "Japanese": "jpn_Jpan",
    "Korean": "kor_Hang",
    "Arabic": "arb_Arab",
    "Bengali": "ben_Beng",
    "Tamil": "tam_Taml",
    "Telugu": "tel_Telu",
    "Marathi": "mar_Deva",
    "Gujarati": "guj_Gujr",
    "Punjabi": "pan_Guru",
    "Urdu": "urd_Arab"
}

print("Loading Offline AI Translation Model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

print("Model Loaded Successfully!")

def translate_text(text, source_language="English", target_language="Hindi"):
    if not text.strip():
        return text

    tokenizer.src_lang = LANGUAGE_CODES[source_language]

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():
        translated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids(
                LANGUAGE_CODES[target_language]
            ),
            max_length=512
        )

    translated_text = tokenizer.batch_decode(
        translated_tokens,
        skip_special_tokens=True
    )[0]

    return translated_text