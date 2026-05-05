import whisper
import os

# Model bir kez yuklenip hafizada tutulur
# "base" modeli hiz ve dogruluk arasinda iyi denge saglar
# Alternatifler: "tiny" (cok hizli), "small", "medium", "large" (cok dogru ama yavas)
model = None

def model_yukle():
    global model
    if model is None:
        print("Whisper modeli yukleniyor, lutfen bekleyin...")
        model = whisper.load_model("large", download_root="./model/whisper")
        print("Whisper modeli hazir.")
    return model

def sesi_metne_cevir(ses_dosyasi_yolu: str) -> str:
    m = model_yukle()

    # Dosya boyutunu kontrol et
    boyut = os.path.getsize(ses_dosyasi_yolu)
    print(f"Ses dosyasi boyutu: {boyut} byte")

    sonuc = m.transcribe(ses_dosyasi_yolu, language="tr", fp16=False, temperature=0, no_speech_threshold=0.6,  # Sessizse bos don
    condition_on_previous_text=False)
    metin = sonuc["text"].strip()
    print(f"STT sonucu: {metin}")
    return metin

def gecici_dosyayi_sil(yol: str):
    try:
        if os.path.exists(yol):
            os.remove(yol)
    except Exception:
        pass
