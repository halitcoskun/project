# Otonom MHRS Randevu Asistanı (LLM & STT Tabanlı)

## 📊 Testlerin Koşulması

Projedeki STT başarı oranlarını (WER) ve LLM entegrasyon hata toleransını ölçmek için test betiklerini çalıştırabilirsiniz:

* Jiwer kütüphanesi ile ölçülen kelime hata oranı (WER); 

* ```python tests/wer_analizi.py```

* Ajan (Agent) fonksiyon çağırma doğruluğu; 

* ```python tests/test_agent.py```

* Kapsam dışı senaryolarda llm modelinin davranış testti; 

* ```python tests/test_sistem.py```

* 100 senaryolu ses dosyası oluşturmak için; 

* ```python tests/test_ses_uretici.py```

* 100 senaryolu ses dosyasını test için; 

* ```python tests/test_core.py```
