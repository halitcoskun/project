from gtts import gTTS
import os
import uuid

def metni_sese_cevir(metin: str) -> str:
    """
    Verilen metni Turkce sese cevirir.
    Olusturulan ses dosyasinin yolunu dondurur.
    """
    dosya_adi = f"tts_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=metin, lang="tr", slow=False)
    tts.save(dosya_adi)
    print(f"[TTS] Ses dosyasi olusturuldu: {dosya_adi}")
    return dosya_adi

def tts_dosyasini_sil(yol: str):
    try:
        if os.path.exists(yol):
            os.remove(yol)
    except Exception:
        pass
