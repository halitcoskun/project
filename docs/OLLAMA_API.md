# Otonom MHRS Randevu Asistanı (LLM & STT Tabanlı)

## 🚀 OLLAMA Üzerinden MODEL İle Konuşma

🦙 **Ollama ile Yerel Çıkarım (Local Inference) Süreci**

Google Colab üzerinde Unsloth ile eğitilen ve GGUF formatında dışa aktarılan modelin, yerel sunucumuzda (localhost) FastAPI ile haberleşebilmesi için Ollama kullanılmıştır. Ollama, yüksek VRAM gereksinimlerini optimize ederek modelin standart bilgisayarlarda yüksek hızda çalışmasını (inference) sağlar.

Kendi eğittiğimiz asistan modelini Ollama'ya entegre etmek için aşağıdaki adımlar izlenmiştir:

**1.Modelfile Oluşturulması**

Ollama'nın modelimizi nasıl çalıştıracağını ve hangi sistem komutlarına uyacağını belirlemek için projenin ana dizininde uzantısız bir Modelfile oluşturulmuştur. Bu dosya, modelin temel (base) dosyasını ve bizim otonom MHRS talimatlarımızı içerir.

Örnek Modelfile İçeriği:
```
**Fine-tune edilmiş GGUF modelinin dosya yolu**
FROM ./mhrs_asistans_q4_k_m.gguf

**Modelin yaratıcılığını (halüsinasyon riskini) düşürmek için sıcaklık ayarı**

TEMPLATE """{{ if .System }}<|start_header_id|>system<|end_header_id|>

{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>

{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>

"""

PARAMETER stop "<|eot_id|>"
PARAMETER stop "<|end_of_text|>"
PARAMETER stop "<|start_header_id|>"
PARAMETER stop "ЎыџN"
PARAMETER stop "<|reserved_special_token_"
PARAMETER stop "・━・━"

PARAMETER temperature 0.1
```


**2. Modelin Ollama'ya Kaydedilmesi ve Çalıştırılması**
Modelfile hazırlandıktan sonra dosyanın olduğu dizin terminal üzerinden açılır, aşağıdaki komut çalıştırılarak model Ollama kütüphanesine mhrs-asistans adıyla inşa edilmiştir (build):

```
ollama create mhrs-asistans -f Modelfile
```

Kurulum tamamlandıktan sonra modeli yerelde test etmek için:

```
ollama run mhrs-asistan
```
Bu işlemin ardından model, FastAPI backend sistemimizin **main.py** port üzerinden istek atıp yanıt alabileceği şekilde arka planda sürekli çalışır hale gelmiştir.

