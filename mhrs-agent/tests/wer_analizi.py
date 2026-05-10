import jiwer

test_analiz_verileri = [
    {
        "dosya": "test_12_gastro_endoskopi.webm",
        "referans": "gastroenteroloji bölümünden endoskopi göstermek için gün almak istiyorum",
        "hipotez": "dastroenteroloji bölümünden endoskopi göstermek için gün almak istiyorum"
    },
    {
        "dosya": "test_44_kadin_dogum_miyom.webm",
        "referans": "miyom tedavisi için kadın doğum bölümüne önümüzdeki hafta yer var mı",
        "hipotez": "miom tedavisi için kadın doğum bölümüne önümüzdeki hafta yer var mı"
    },
    {
        "dosya": "test_86_randevu_sorgula_tarih.webm",
        "referans": "ayın on beşindeki randevumun saatini öğrenebilir miyim",
        "hipotez": "ayın 15'indeki randevumun saatini öğrenebilir miyim"
    },
    {
        "dosya": "test_96_sorgula_tarih_dogrumu.webm",
        "referans": "yarın sabah dokuz buçukta dahiliye randevum var doğru mu",
        "hipotez": "yarın sabah 9.30'da dahiliye randevum var doğru mu"
    }
]

print("--- ORİJİNAL JİWER (WER) HATA ANALİZİ RAPORU ---\n")

toplam_wer = 0

for veri in test_analiz_verileri:
    # Orijinal jiwer kütüphanesinin kendi fonksiyonunu kullanıyoruz!
    hata_orani = jiwer.wer(veri["referans"], veri["hipotez"])
    toplam_wer += hata_orani
    
    dogruluk_yuzdesi = max(0, (1 - hata_orani)) * 100
    
    print(f"Dosya: {veri['dosya']}")
    print(f"Referans (Beklenen): {veri['referans']}")
    print(f"Hipotez  (Çıkan)   : {veri['hipotez']}")
    print(f"WER Skoru          : {hata_orani:.3f}")
    print(f"Kelime Doğruluğu   : %{dogruluk_yuzdesi:.1f}\n")

ortalama_wer = toplam_wer / len(test_analiz_verileri)
print("-" * 50)
print(f"Başarısız Senaryoların Ortalama WER Skoru: {ortalama_wer:.3f}")
print(f"Başarısız Senaryoların Ortalama Doğruluğu: %{(1 - ortalama_wer) * 100:.1f}")