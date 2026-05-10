# Otonom MHRS Randevu Asistanı (LLM & STT Tabanlı)

## 🚀 Meta Llama 3 8B Modelin FineTuning İle Eğitilmesi

📊 **Eğitim Veri Seti (Hugging Face)**

Bu projedeki Llama 3 modeli, MHRS randevu süreçlerini otonom olarak yönetebilmesi için özel olarak oluşturulmuş Türkçe bir komut-yanıt (Instruction Tuning) veri seti ile eğitilmiş/ince ayar (Fine-Tuning) yapılmıştır. Veri seti, modelin kullanıcının tıbbi şikayetlerini, randevu taleplerini, iptal işlemlerini ve konu dışı sohbetlerini analiz edip standart JSON formatında fonksiyon çağrılarına (Tool Calling) dönüştürebilmesi amacıyla hazırlanmıştır.

Kullanılan veri seti JSON/JSONL formatında yapılandırılmış olup, açık kaynak topluluğunun erişimine sunulmak üzere Hugging Face Hub üzerine yüklenmiştir.

🔗 **Veri Setine Erişim**

Veri setini doğrudan Hugging Face üzerinden inceleyebilir veya kendi projelerinize dahil edebilirsiniz:

Hugging Face Dataset: [[https://huggingface.co/datasets/halitcoskun/mhrs-randevu-veri-seti]](https://huggingface.co/datasets/halitcoskun/mhrs-randevu-veri-seti)

📝 **Veri Seti Yapısı ve Örnek Format**

Veri seti, modelin "System", "User" ve "Assistant" rollerini anlayabilmesi için aşağıdaki JSON yapısına uygun olarak dizayn edilmiştir.

Sistem promptu şu çekirdek talimat üzerine kuruludur: "Sen otonom bir MHRS asistanısın. Kullanıcının randevu taleplerini, tıbbi şikayetlerini, iptal işlemlerini veya konu dışı sohbetlerini analiz et."

Örnek Veri Satırı:

JSON
```
{
  "messages": [
    {
      "role": "system",
      "content": "Sen otonom bir MHRS asistanısın. Kullanıcının randevu taleplerini, tıbbi şikayetlerini, iptal işlemlerini veya konu dışı sohbetlerini analiz et. Çıktılarını her zaman fonksiyon çağrısı içeren JSON formatında üret.\n\nGörevin kullanıcı taleplerini analiz edip SADECE aşağıdaki fonksiyonlardan birini içeren JSON üretmektir:\n1. ask_user\n2. check_availability\n3. book_appointment\n4. cancel_appointment\n5. list_appointments\n\nKESİNLİKLE bu listede olmayan bir fonksiyon adı (örneğin create_appointment vb.) kullanma.\n\nKritik Kural (Departman Kısıtlaması):\nEğer üreteceğin JSON'un içinde bir \"department\" parametresi varsa, bu parametrenin değeri SADECE aşağıdaki listede yer alan standart isimlerden biri olmak ZORUNDADIR. Başka hiçbir kelime veya ek kullanma:\n- \"Dahiliye\"\n- \"Kardiyoloji\"\n- \"Cildiye\"\n- \"Göz Hastalıkları\"\n- \"Gastroenteroloji\"\n- \"Kulak Burun Boğaz\"\n- \"Ortopedi ve Travmatoloji\"\n- \"Nöroloji\"\n- \"Genel Cerrahi\"\n- \"Psikiyatri\"\n- \"Üroloji\"\n- \"Kadın Hastalıkları ve Doğum\"\n\nKullanıcı eşanlamlı veya kısaltma kullansa bile, sen bunu yukarıdaki listedeki karşılığına çevirmelisin. Eğer kesin anlayamıyorsan \"ask_user\" ile netleştir.\n\nKRİTİK BİLGİ (Zaman Farkındalığı):\nBugünün tarihi: 2023-09-22\nBugün günlerden: Cuma\nEğer kullanıcı \"yarın\", \"haftaya\" gibi göreceli zaman kullanırsa, bugünü baz alarak hesapla ve JSON içindeki \"date\" parametresini KESİNLİKLE \"YYYY-MM-DD\" formatında mutlak bir tarihe çevir. \"sabah\", \"öğlen\" veya \"14:00\" gibi net saatleri \"time_preference\" parametresi olarak ekle. Eğer kullanıcı net veya göreceli bir tarih belirtmezse (örneğin 'en yakın tarih', 'en erken', 'fark etmez' derse), üreteceğin JSON içine KESİNLİKLE 'date' parametresi ekleme."
    },
    {
      "role": "user",
      "content": "Merhaba, şiddetli mide ağrım var. Gastroenteroloji bölümünden yarın sabah için randevu bulabilir misiniz?"
    },
    {
      "role": "assistant",
      "content": "{\"function\": \"check_availability\", \"parameters\": {\"department\": \"Gastroenteroloji\", \"date\": \"2026-05-11\", \"time_preference\": \"sabah\"}}"
    }
  ]
}
```

💻 **Python ile Veri Setini Yükleme**

Veri setini Hugging Face datasets kütüphanesini kullanarak doğrudan Python veya Google Colab ortamınıza çekebilirsiniz:

Python
```
from datasets import load_dataset

# MHRS JSON veri setini indir
dataset = load_dataset("hf_kullanici_adiniz/mhrs-asistan-veriseti")

# Eğitim (train) setinden ilk örneği görüntüle
print(dataset['train'][0])
```

🧠 **Model Eğitimi ve İnce Ayar (Fine-Tuning) Süreci**

Bu projede kullanılan Llama 3 8B modelinin otonom bir MHRS asistanına dönüştürülmesi (Instruction Fine-Tuning) işlemi, model eğitim süreçlerini optimize eden Unsloth kütüphanesi kullanılarak Google Colab üzerinde gerçekleştirilmiştir. Unsloth, standart QLoRA tabanlı eğitimlere kıyasla çok daha hızlı eğitim süreleri ve düşük VRAM (ekran kartı belleği) tüketimi sunarak modelin verimli bir şekilde eğitilmesini sağlamıştır.

🚀 **Google Colab Notebook**

Eğitim sürecini baştan sona (adım adım) incelemek, Hugging Face entegrasyonlarını görmek veya modeli kendi verilerinizle yeniden eğitmek için hazırlamış olduğum Google Colab defterine aşağıdaki bağlantıdan doğrudan ulaşabilirsiniz:

Colab Linki: [[Colab_MHRS_Llama3_Egitim.ipynb]](https://colab.research.google.com/drive/1lBxioQdWi6Y-R2PCGi-leoE74qTN7fu6#scrollTo=FqfebeAdT073)

GitHub Linki: [[Git_MHRS_Llama3_Egitim.ipynb]](https://github.com/halitcoskun/project/blob/main/MHRS_Llama3_Egitim.ipynb)

(Not: Colab linkini açtıktan sonra "File > Save a copy in Drive" diyerek kendi çalışma alanınıza kopyalayabilirsiniz.)

🛠️ **Eğitim Aşamaları (Unsloth & QLoRA)**

Colab defteri içerisinde sırasıyla şu mimari adımlar izlenmiştir:

Ortam Hazırlığı: Unsloth kütüphanesinin ve Hugging Face transformers, trl, peft bağımlılıklarının Colab GPU ortamına kurulması.

Modelin 4-bit Yüklenmesi: Llama 3 8B modelinin bellek optimizasyonu amacıyla 4-bit (quantization) formatında yüklenmesi.

Veri Formatlama: MHRS veri setimizin, Llama 3'ün System, User, Assistant (ChatML/Instruct) konuşma şemasına (Prompt Template) uygun olarak formatlanması.

LoRA Adaptör Eğitimi: Bütün modeli eğitmek yerine, sadece belirli ağırlık matrislerini eğiten QLoRA (Quantized Low-Rank Adaptation) tekniği ile modelin asistan rolünü öğrenmesi.

GGUF Formatında Dışa Aktarma: Eğitim tamamlandıktan sonra, modelin yerel donanımda (Ollama üzerinden) çalışabilmesi için 16-bit GGUF formatında derlenip yerel ortama indirilmesi.

Model bu süreçlerin sonunda, sistemdeki FastAPI ve C# Mock API katmanlarıyla haberleşecek standart JSON formatını kusursuz bir şekilde üretebilir hale getirilmiştir.
