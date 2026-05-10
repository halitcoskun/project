from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import uvicorn
import shutil
import uuid
import os
import requests
import json
import re
import datetime
import locale

app = FastAPI()

gunler = {
    0: "Pazartesi", 1: "Salı", 2: "Çarşamba", 3: "Perşembe", 
    4: "Cuma", 5: "Cumartesi", 6: "Pazar"
}

bugun_tarih = datetime.datetime.now().strftime("%Y-%m-%d")
bugun_gun = gunler[datetime.datetime.now().weekday()]

# Oturum bazli konusma gecmisi
konusma_gecmisleri = {}

class Mesaj(BaseModel):
    mesaj: str
    session_id: str

# --- 1. YAPAY ZEKA GÜVENLİK AĞI ---
def parse_ai_response(raw_text):
    # 1. LLM'in ürettiği Llama-3 özel tag'lerini ve sonrasını kesip atalım
    # Eger metin icinde <| tag'i varsa, oradan sonrasini siler.
    if "<|" in raw_text:
        raw_text = raw_text.split("<|")[0]

    # 2. Şimdi kalan temiz metin üzerinden ilk { ve son } parantezini bulalım
    start_idx = raw_text.find('{')
    end_idx = raw_text.rfind('}')
    
    if start_idx != -1 and end_idx != -1:
        clean_json_str = raw_text[start_idx:end_idx+1]
        try:
            data = json.loads(clean_json_str)
            if "function" in data:
                return data
        except json.JSONDecodeError as e:
            print(f"JSON Parse Hatası: {e} -> Temizlenmeye Çalışılan Metin: {clean_json_str}")
            pass 
            
    # Hata durumu: Kullaniciya caktirmadan diyologu basa sar
    return {
        "function": "ask_user",
        "parameters": {"message": "Sizi tam olarak anlayamadım, şikayetinizi veya poliklinik adını tekrar eder misiniz?"}
    }

# --- 2. OLLAMA İLETİŞİM FONKSİYONU (Hafıza Destekli) ---
def get_ollama_decision(gecmis):
    url = "http://localhost:11434/api/chat" # /generate yerine chat api'sini kullaniyoruz
    
    # Kullanicinin gecmisini Ollama'ya veriyoruz ki "Evet" dediginde neye evet dedigini bilsin
    payload = {
        "model": "mhrs_asistans",
        "messages": gecmis, 
        "stream": False,
        "format": "json",  # ÇÖZÜM 1: Ollama'yı sadece ve sadece JSON üretmeye zorlar!
        "options": {
            # ÇÖZÜM 2: Modelin kendi kendine konuşmaya başlamasını (halüsinasyonu) anında keser
            "stop": ["<|eot_id|>", "<|end_of_text|>", "<|begin_of_text|>"] 
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=None)
        response.raise_for_status()
        # Chat API'sinde yanit formati biraz farklidir:
        raw_text = response.json().get("message", {}).get("content", "")
        return parse_ai_response(raw_text)
    except Exception as e:
        print(f"Ollama Bağlantı Hatası: {e}")
        return parse_ai_response("")

# --- 3. C# MOCK API FONKSİYONLARI ---

# C# Web API'nin temel adresi (Portu kendi projene göre güncelle)
CSHARP_API_BASE_URL = "http://api.mhrs.com/api/Mhrs"

def api_check_availability(department, date, timePreference, session_id):
    url = f"{CSHARP_API_BASE_URL}/CheckAvailability"
    payload = {"department": department, "date": date, "timePreference": timePreference, "userId": session_id}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # C# tarafından {"isAvailable": true, "doctorName": "...", "timeSlot": "..."} bekleniyor
            if data.get("isAvailable"):
                doctor = data.get("doctorName", "")
                time = data.get("timeSlot", "")
                return f"{department} bölümünde {time} tarihinde {doctor}'a boş randevu buldum. Bu randevuyu sizin için oluşturayım mı?"
            else:
                return f"Maalesef {department} bölümünde boş randevu bulunmamaktadır. Başka bir gün veya poliklinik bakmamı ister misiniz?"
        else:
            return f"Randevu sisteminde geçici bir sorun var (Hata Kodu: {response.status_code}). Lütfen daha sonra tekrar deneyin."
            
    except requests.exceptions.RequestException as e:
        print(f"C# API Hatası (Check): {e}")
        return "Hastane sunucularıyla bağlantı kuramadım, lütfen birazdan tekrar deneyin."

def api_book_appointment(department, date, timePreference, session_id):
    url = f"{CSHARP_API_BASE_URL}/BookAppointment"
    payload = {"department": department, "date": date, "timePreference": timePreference, "userId": session_id}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # C# tarafından {"success": true, "message": "..."} bekleniyor
            if data.get("success"):
                return f"İşleminiz tamamlandı! {department} bölümüne, {date} saat {timePreference} için randevunuz başarıyla oluşturuldu. Sağlıklı günler dileriz."
            else:
                error_msg = data.get("message", "Farklı bir departmana aynı zamanda randevunuz bulunmuş olabilir.")
                return f"Randevunuz oluşturulamadı: {error_msg}"
        else:
            return "Kayıt işlemi sırasında sistemsel bir hata oluştu."
            
    except requests.exceptions.RequestException as e:
        print(f"C# API Hatası (Book): {e}")
        return "Hastane sunucularına şu an ulaşılamıyor."

def api_cancel_appointment(department, date, session_id):
    url = f"{CSHARP_API_BASE_URL}/CancelAppointment"
    payload = {"department": department, "date": date, "userId": session_id}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # C# tarafından {"success": true, "message": "..."} bekleniyor
            if data.get("success"):
                return f"{date} tarihindeki {department} randevunuz sistemden başarıyla iptal edilmiştir."
            else:
                error_msg = data.get("message", "Sistemde böyle bir randevu bulunamadı.")
                return f"İptal işlemi başarısız: {error_msg}"
        else:
            return "İptal işlemi sırasında bir sistem hatası oluştu."
            
    except requests.exceptions.RequestException as e:
        print(f"C# API Hatası (Cancel): {e}")
        return "Hastane sunucularına ulaşılamıyor."

def api_list_appointments(date, session_id):
    url = f"{CSHARP_API_BASE_URL}/ListAppointment"
    payload = {"date": date, "userId": session_id}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # C# tarafından {"appointments": [ {"department": "Göz", "date": "...", "time": "..."} ] } bekleniyor
            appointments = data.get("appointments", [])
            
            if appointments:
                count = len(appointments)
                # Sadece ilk randevuyu okuyarak kısa bir bilgi veriyoruz
                ilk_randevu = appointments[0]
                return f"Bu arama için sistemde kayıtlı toplam {count} adet randevunuz bulunmaktadır. En yakını: {ilk_randevu.get('date')} - {ilk_randevu.get('department')} bölümü."
            else:
                return f"Bu arama için zaman dilimi için sistemde kayıtlı hiçbir randevunuz bulunmamaktadır."
        else:
            return "Randevularınız sorgulanırken bir hata oluştu."
            
    except requests.exceptions.RequestException as e:
        print(f"C# API Hatası (List): {e}")
        return "Hastane sunucularına ulaşılamıyor."

# --- 4. MERKEZİ ORKESTRATÖR (YÖNLENDİRİCİ) ---
def agent_orkestrator(ai_decision, session_id):
    func = ai_decision.get("function")
    
    # Model bazen parametreleri "parameters" içine koymak yerine dışarıda bırakabiliyor.
    # Bu yüzden her iki yere de bakacak güvenli bir yardımcı fonksiyon tanımlıyoruz.
    raw_params = ai_decision.get("parameters", {})
    
    def get_safe_param(key):
        # Önce "parameters" içinde ara, bulamazsan ana sözlükte ara, o da yoksa boş dön.
        return raw_params.get(key) or ai_decision.get(key) or ""

    # --- YAPAY ZEKA HALÜSİNASYON DÜZELTİCİ (ALIAS) ---
    if func in ["create_appointment", "make_appointment"]:
        func = "book_appointment"
    elif func == "check_appointment":
        func = "check_availability"

    # 1. Bilgi eksikse veya onay bekleniyorsa
    if func == "ask_user":
        return get_safe_param("message") or "Size nasıl yardımcı olabilirim?"
        
    # 2. Uygunluk kontrolü
    elif func == "check_availability":
        dept = get_safe_param("department")
        date = get_safe_param("date")
        timePreference = get_safe_param("time_preference")
        return api_check_availability(dept, date, timePreference, session_id)
        
    # 3. Kesin kayit islemi
    elif func == "book_appointment":
        dept = get_safe_param("department")
        date = get_safe_param("date")
        timePreference = get_safe_param("time_preference")
        return api_book_appointment(dept, date, timePreference, session_id)
        
    # 4. Iptal islemi
    elif func == "cancel_appointment":
        dept = get_safe_param("department")
        date = get_safe_param("date")
        return api_cancel_appointment(dept, date, session_id)
        
    # 5. Listeleme islemi
    elif func == "list_appointments":
        date = get_safe_param("date")
        return api_list_appointments(date, session_id)
        
    else:
        return "Sistemde bir hata oluştu, lütfen işleminizi tekrar belirtin."

# --- API ENDPOINT'LERI ---

@app.get("/", response_class=HTMLResponse)
def anasayfa():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html)

@app.post("/konus")
def konus(istek: Mesaj):
    session_id = istek.session_id
    
    # Eger ilk mesajsa, system promptunu oturuma ekle
    if session_id not in konusma_gecmisleri:
        konusma_gecmisleri[session_id] = [
            {"role": "system", "content": f"Sen otonom bir MHRS asistanısın. Kullanıcının randevu taleplerini, tıbbi şikayetlerini, iptal işlemlerini veya konu dışı sohbetlerini analiz et. Çıktılarını her zaman fonksiyon çağrısı içeren JSON formatında üret.\n\nGörevin kullanıcı taleplerini analiz edip SADECE aşağıdaki fonksiyonlardan birini içeren JSON üretmektir:\n1. ask_user\n2. check_availability\n3. book_appointment\n4. cancel_appointment\n5. list_appointments\n\nKESİNLİKLE bu listede olmayan bir fonksiyon adı (örneğin create_appointment vb.) kullanma.\n\nKritik Kural (Departman Kısıtlaması):\nEğer üreteceğin JSON'un içinde bir \"department\" parametresi varsa, bu parametrenin değeri SADECE aşağıdaki listede yer alan standart isimlerden biri olmak ZORUNDADIR. Başka hiçbir kelime veya ek kullanma:\n- \"Dahiliye\"\n- \"Kardiyoloji\"\n- \"Cildiye\"\n- \"Göz Hastalıkları\"\n- \"Gastroenteroloji\"\n- \"Kulak Burun Boğaz\"\n- \"Ortopedi ve Travmatoloji\"\n- \"Nöroloji\"\n- \"Genel Cerrahi\"\n- \"Psikiyatri\"\n- \"Üroloji\"\n- \"Kadın Hastalıkları ve Doğum\"\n\nKullanıcı eşanlamlı veya kısaltma kullansa bile (Örneğin; \"İç hastalıkları\", \"KBB\", \"Cildiye doktoru\", \"Göz\"), sen bunu yukarıdaki listedeki karşılığına çevirmelisin. Eğer kullanıcının şikayetinden hangi polikliniğe gitmesi gerektiğini kesin olarak anlayamıyorsan, \"ask_user\" fonksiyonunu kullanarak hastadan poliklinik adını netleştirmesini iste.\n\nKRİTİK BİLGİ (Zaman Farkındalığı):\nBugünün tarihi: {bugun_tarih}\nBugün günlerden: {bugun_gun}\nEğer kullanıcı \"yarın\", \"haftaya\", \"salı günü\" gibi göreceli zaman dilimleri kullanırsa, yukarıdaki bugünün tarihini baz alarak hesaplama yap. Üreteceğin JSON içindeki \"date\" parametresini KESİNLİKLE \"YYYY-MM-DD\" formatında mutlak bir tarihe çevirerek ver.\nEğer kullanıcı \"sabah\", \"öğlen\", \"öğleden sonra\", \"akşam\" gibi bir zaman dilimi veya \"saat 14:00\" gibi net bir saat belirtirse, bunu JSON içinde \"time_preference\" adında yeni bir parametre olarak ekle. Model olarak saat uydurma, sadece kullanıcının niyetini (sabah, 14:00 vb.) bu alana yaz."}
        ]
        
    gecmis = konusma_gecmisleri[session_id]
    gecmis.append({"role": "user", "content": istek.mesaj})

    # 1. Ollama'dan Karar Al (Tum gecmisi veriyoruz)
    ai_decision = get_ollama_decision(gecmis)
    
    # 2. Karari Orkestratore Gonderip Yaniti Al
    yanit = agent_orkestrator(ai_decision, session_id)

    gecmis.append({"role": "assistant", "content": yanit})
    konusma_gecmisleri[session_id] = gecmis

    # TTS: yaniti sese cevir
    from tts import metni_sese_cevir
    tts_dosyasi = metni_sese_cevir(yanit)

    return {
        "yanit": yanit,
        "ses_url": f"/tts-ses/{tts_dosyasi}"
    }

@app.post("/ses-konus")
async def ses_konus(dosya: UploadFile = File(...), session_id: str = Form(...)):

    gecici_ad = f"gecici_{uuid.uuid4().hex}.wav"
    with open(gecici_ad, "wb") as f:
        shutil.copyfileobj(dosya.file, f)

    try:
        # STT: sesi metne cevir
        from stt import sesi_metne_cevir
        algilanan_metin = sesi_metne_cevir(gecici_ad)

        if not algilanan_metin:
            return {
                "algilanan_metin": "(ses algilanamadi)",
                "yanit": "Sesinizi anlayamadim, tekrar dener misiniz?",
                "ses_url": None
            }
        
        if session_id not in konusma_gecmisleri:
            konusma_gecmisleri[session_id] = [
                {"role": "system", "content": "Sen otonom bir MHRS asistanısın. Kullanıcının randevu taleplerini, tıbbi şikayetlerini, iptal işlemlerini veya konu dışı sohbetlerini analiz et. Çıktılarını her zaman fonksiyon çağrısı içeren JSON formatında üret.\n\nGörevin kullanıcı taleplerini analiz edip SADECE aşağıdaki fonksiyonlardan birini içeren JSON üretmektir:\n1. ask_user\n2. check_availability\n3. book_appointment\n4. cancel_appointment\n5. list_appointments\n\nKESİNLİKLE bu listede olmayan bir fonksiyon adı (örneğin create_appointment vb.) kullanma.\n\nKritik Kural (Departman Kısıtlaması):\nEğer üreteceğin JSON'un içinde bir \"department\" parametresi varsa, bu parametrenin değeri SADECE aşağıdaki listede yer alan standart isimlerden biri olmak ZORUNDADIR. Başka hiçbir kelime veya ek kullanma:\n- \"Dahiliye\"\n- \"Kardiyoloji\"\n- \"Cildiye\"\n- \"Göz Hastalıkları\"\n- \"Gastroenteroloji\"\n- \"Kulak Burun Boğaz\"\n- \"Ortopedi ve Travmatoloji\"\n- \"Nöroloji\"\n- \"Genel Cerrahi\"\n- \"Psikiyatri\"\n- \"Üroloji\"\n- \"Kadın Hastalıkları ve Doğum\"\n\nKullanıcı eşanlamlı veya kısaltma kullansa bile (Örneğin; \"İç hastalıkları\", \"KBB\", \"Cildiye doktoru\", \"Göz\"), sen bunu yukarıdaki listedeki karşılığına çevirmelisin. Eğer kullanıcının şikayetinden hangi polikliniğe gitmesi gerektiğini kesin olarak anlayamıyorsan, \"ask_user\" fonksiyonunu kullanarak hastadan poliklinik adını netleştirmesini iste.\n\nKRİTİK BİLGİ (Zaman Farkındalığı):\nBugünün tarihi: {bugun_tarih}\nBugün günlerden: {bugun_gun}\nEğer kullanıcı \"yarın\", \"haftaya\", \"salı günü\" gibi göreceli zaman dilimleri kullanırsa, yukarıdaki bugünün tarihini baz alarak hesaplama yap. Üreteceğin JSON içindeki \"date\" parametresini KESİNLİKLE \"YYYY-MM-DD\" formatında mutlak bir tarihe çevirerek ver.\nEğer kullanıcı \"sabah\", \"öğlen\", \"öğleden sonra\", \"akşam\" gibi bir zaman dilimi veya \"saat 14:00\" gibi net bir saat belirtirse, bunu JSON içinde \"time_preference\" adında yeni bir parametre olarak ekle. Model olarak saat uydurma, sadece kullanıcının niyetini (sabah, 14:00 vb.) bu alana yaz."}
            ]

        gecmis = konusma_gecmisleri[session_id]
        gecmis.append({"role": "user", "content": algilanan_metin})

        # 1 ve 2. Adimlar
        ai_decision = get_ollama_decision(gecmis)
        yanit = agent_orkestrator(ai_decision, session_id)

        gecmis.append({"role": "assistant", "content": yanit})
        konusma_gecmisleri[session_id] = gecmis

        # TTS: yaniti sese cevir
        from tts import metni_sese_cevir
        tts_dosyasi = metni_sese_cevir(yanit)

        return {
            "algilanan_metin": algilanan_metin,
            "yanit": yanit,
            "ses_url": f"/tts-ses/{tts_dosyasi}"
        }

    finally:
        from stt import gecici_dosyayi_sil
        gecici_dosyayi_sil(gecici_ad)



@app.get("/tts-ses/{dosya_adi}")
async def tts_ses_getir(dosya_adi: str):
    """Olusturulan TTS ses dosyasini tarayiciya gonderir ve siler."""
    # Guvenlik: sadece tts_ ile baslayan mp3 dosyalarina izin ver
    if not dosya_adi.startswith("tts_") or not dosya_adi.endswith(".mp3"):
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Gecersiz dosya adi")

    if not os.path.exists(dosya_adi):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Ses dosyasi bulunamadi")

    return FileResponse(
        path=dosya_adi,
        media_type="audio/mpeg",
        filename=dosya_adi,
        background=None
    )

@app.delete("/tts-ses/{dosya_adi}")
async def tts_ses_sil(dosya_adi: str):
    """Tarayici sesi oynadiktan sonra dosyayi siler."""
    from tts import tts_dosyasini_sil
    tts_dosyasini_sil(dosya_adi)
    return {"ok": True}


import uvicorn

# ... (Senin yazdığın tüm o route ve fonksiyon kodları yukarıda kalacak) ...

# Eger bu dosya dogrudan calistiriliyorsa (VSCode F5 ile yaptigimiz gibi), Uvicorn motorunu calistir:
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

