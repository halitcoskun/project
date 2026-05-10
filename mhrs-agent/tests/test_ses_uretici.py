import os
import subprocess
from gtts import gTTS

def ses_dosyalarini_uret():
    """
    Testlerde kullanılmak üzere 100 farklı MHRS senaryosunu
    otomatik olarak sese çevirir ve .webm formatında kaydeder.
    """
    # Seslerin kaydedileceği klasörü oluştur (test_core.py içindeki yolla aynı)
    klasor_adi = "tests/test_data"
    os.makedirs(klasor_adi, exist_ok=True)
    
    # 100 Farklı Test Senaryosu (Input)
    senaryolar = {
        "test_01_kardiyoloji_istegi": "Yarın için kardiyoloji bölümünden randevu almak istiyorum.",
        "test_02_dahiliye_sabah": "Dahiliye doktoruna sabah saatleri için randevu al.",
        "test_03_randevu_iptali": "Mevcut randevumu iptal etmek istiyorum.",
        "test_04_en_yakin_bos": "En yakın boş randevu ne zaman?",
        "test_05_kbb_tarihli": "Kulak burun boğaz bölümünden haftaya salı gününe randevu bak.",
        "test_06_cildiye_il": "İstanbul'da Cildiye için bir randevu ayarlar mısın?",
        "test_07_goz_doktoru": "Göz hastalıkları bölümü için cuma gününe randevu istiyorum.",
        "test_08_ortopedi_sorgu": "Ortopedi bölümü doktorlarına randevu var mı?",
        "test_09_tc_sorgulama": "Randevumu sorgulamak istiyorum.",
        "test_10_noroloji_ogle": "Nöroloji için öğleden sonra müsaitlik var mı?",

        # GASTROENTEROLOJİ
        "test_11_gastro_mide": "Mide ağrım var, gastroenteroloji bölümüne randevu alabilir miyim?",
        "test_12_gastro_endoskopi": "Gastroenteroloji bölümünden endoskopi göstermek için gün almak istiyorum.",
        "test_13_gastro_reflu": "Reflü şikayetim için gastroenteroloji bölümünden randevu ayarla.",
        "test_14_gastro_karin_agrisi": "Şiddetli karın ağrım var, gastroenterolojiye acil randevu alabilir miyiz?",
        "test_15_gastro_hazimsizlik": "Hazımsızlık şikayetiyle gastroenterolojiye muayene olmak istiyorum.",
        "test_16_gastro_karaciyer": "Karaciğer enzimlerim yüksek çıkmış, gastroenterolojiye randevu bul.",
        "test_17_gastro_kanama": "Mide rahatsızlığı şüphesiyle acil gastroenteroloji randevusu lazım.",

        # GENEL CERRAHİ
        "test_18_genel_cerrahi_kontrol": "Genel cerrahi bölümünde ameliyat sonrası kontrolüm için randevu bakıyorum.",
        "test_19_genel_cerrahi_safra": "Genel cerrahiye safra kesesi şikayetiyle haftaya randevu al.",
        "test_20_genel_cerrahi_dikis": "Dikişlerimi aldırmak için genel cerrahiye randevu bulabilir misin?",
        "test_21_genel_cerrahi_tiroid": "Tiroid ameliyatı görüşmesi için genel cerrahiye randevu istiyorum.",
        "test_22_genel_cerrahi_kil_donmesi": "Kıl dönmesi şikayeti için genel cerrahi bölümüne yer var mı?",
        "test_23_genel_cerrahi_apandisit": "Apandisit şüphesiyle genel cerrahi polikliniğine görünmek istiyorum.",
        "test_24_genel_cerrahi_yara": "Kapanmayan yaram var, genel cerrahi polikliniğine randevu oluştur.",

        # PSİKİYATRİ
        "test_25_psikiyatri_terapi": "Psikiyatri bölümünden haftaya çarşamba günü için boşluk var mı?",
        "test_26_psikiyatri_ilac": "Psikiyatri doktorumdan ilaç yazdırmak için kısa bir randevu alabilir miyim?",
        "test_27_psikiyatri_uykusuzluk": "Uykusuzluk problemi çekiyorum, psikiyatri bölümüne randevu almak istiyorum.",
        "test_28_psikiyatri_kaygi": "Kaygı bozukluğu için psikiyatri doktorumdan yeni bir randevu al.",
        "test_29_psikiyatri_cocuk": "Çocuk psikiyatrisi bölümü için haftaya bir randevu oluşturur musun?",
        "test_30_psikiyatri_depresyon": "Depresyon tedavim için psikiyatri bölümünden aylık kontrol randevumu al.",
        "test_31_psikiyatri_panik": "Panik atak geçiriyorum, psikiyatriden hemen bir randevu bulur musun?",

        # ÜROLOJİ
        "test_32_uroloji_bobrek": "Üroloji doktorundan en erken tarihe randevu bulur musun?",
        "test_33_uroloji_kontrol": "Üroloji bölümüne kontrol randevusu oluşturmak istiyorum.",
        "test_34_uroloji_tahlil": "Üroloji bölümüne tahlil sonuçlarımı göstermek için yer var mı?",
        "test_35_uroloji_prostat": "Prostat kontrolü için üroloji bölümünden sabah saatlerine randevu ayarla.",
        "test_36_uroloji_yanma": "İdrarda yanma şikayetiyle üroloji doktoruna görünmem gerekiyor.",
        "test_37_uroloji_sonda": "Sonda değişimi için üroloji bölümüne sabah erkenden randevu lazım.",
        "test_38_uroloji_agri": "Böbreklerim çok ağrıyor, ürolojiye randevu verin.",

        # KADIN HASTALIKLARI VE DOĞUM
        "test_39_kadin_dogum_gebelik": "Kadın hastalıkları ve doğum bölümüne gebelik takibi için randevu alacağım.",
        "test_40_kadin_dogum_ultrason": "Kadın doğum bölümünden ultrason için perşembe gününe yer var mı?",
        "test_41_kadin_dogum_rutin": "Kadın hastalıkları bölümüne rutin kontrol için bir randevu oluştur.",
        "test_42_kadin_dogum_test": "Kadın doğum bölümüne tarama testi için randevu almak istiyorum.",
        "test_43_kadin_dogum_kist": "Kist kontrolü için kadın hastalıkları bölümünden randevu ayarlar mısın?",
        "test_44_kadin_dogum_miyom": "Miyom tedavisi için kadın doğum bölümüne önümüzdeki hafta yer var mı?",
        "test_45_kadin_dogum_sma": "SMA taraması için kadın hastalıkları ve doğum bölümünden randevu istiyorum.",

        # DAHİLİYE (İÇ HASTALIKLARI) VE KARDİYOLOJİ VARYASYONLARI
        "test_46_dahiliye_kan_tahlili": "Dahiliye bölümüne kan tahlili sonuçlarımı göstermek için randevu istiyorum.",
        "test_47_kardiyoloji_eko": "Kardiyoloji doktoruna ekg çektirmek için sabah erkenden randevu lazım.",
        "test_48_dahiliye_seker": "Şeker hastalığı kontrolüm için iç hastalıkları bölümünden randevu istiyorum.",
        "test_49_kardiyoloji_carpinti": "Kalp çarpıntım var, kardiyoloji bölümüne bugün için yer bulunur mu?",
        "test_50_dahiliye_tansiyon": "Tansiyonum sürekli yüksek, dahiliye bölümünden hemen randevu al.",
        "test_51_kardiyoloji_stent": "Stent kontrolüm için kardiyoloji bölümüne haftaya cuma randevu bak.",
        "test_52_dahiliye_kolesterol": "Kolesterol ilacımı yazdırmak için iç hastalıkları bölümüne randevu bul.",
        "test_53_kardiyoloji_nefes_darligi": "Nefes darlığı çekiyorum, kardiyoloji bölümüne bugün randevu var mı?",
        "test_54_dahiliye_yorgunluk": "Sürekli halsizlik ve yorgunluk için dahiliyeden randevu istiyorum.",
        "test_55_kardiyoloji_ritim": "Ritim bozukluğu şikayetiyle kardiyoloji bölümüne randevu al.",

        # CİLDİYE (DERMATOLOJİ) VE GÖZ HASTALIKLARI VARYASYONLARI
        "test_56_cildiye_sivilce": "Cildiye bölümünden sivilce tedavisi için uygun bir saate randevu bakar mısın?",
        "test_57_goz_kontrol_cuma": "Cuma öğleden sonra göz hastalıkları için randevum var mıydı?",
        "test_58_cildiye_alerji": "Vücudumda kızarıklıklar çıktı, dermatoloji bölümüne en yakın randevuyu verin.",
        "test_59_goz_numara_degisimi": "Gözlük numaramı değiştirmek için göz doktoruna randevu alacağım.",
        "test_60_cildiye_sac_dokulmesi": "Aşırı saç dökülmem var, cildiye bölümüne muayene olmak istiyorum.",
        "test_61_goz_katarakt": "Katarakt ameliyatı kontrolü için göz hastalıklarına randevu al.",
        "test_62_cildiye_ben_kontrolu": "Vücudumdaki benlerin kontrolü için dermatolojiden randevu bakar mısın?",
        "test_63_goz_lens": "Kontakt lens muayenesi için göz hastalıkları bölümünden randevu al.",
        "test_64_cildiye_egzama": "Egzamam tekrar alevlendi, dermatoloji doktorumdan hemen randevu ver.",
        "test_65_goz_yanmasi": "Gözlerimde kuruluk ve yanma var, göz bölümüne randevu bakar mısın?",
        "test_66_cildiye_kasinti": "Çok kaşınıyorum, cildiye randevusu bul bana.",
        "test_67_goz_kanlanma": "Gözüm kanlandı, göz doktoruna ne zaman gidebilirim?",

        # KULAK BURUN BOĞAZ VE ORTOPEDİ VARYASYONLARI
        "test_68_kbb_bogaz_agrisi": "Boğazım çok ağrıyor, kulak burun boğazdan acil randevu bulabilir miyiz?",
        "test_69_ortopedi_diz": "Diz kapağım ağrıyor, ortopedi ve travmatolojiye randevu almak istiyorum.",
        "test_70_kbb_isitme": "İşitme kaybı yaşıyorum, kulak burun boğaza randevu bakar mısın?",
        "test_71_ortopedi_alci": "Alçımı çıkarttırmak için ortopedi bölümünden randevu almam gerekiyor.",
        "test_72_kbb_sinuzit": "Sinüzitim azdı, kulak burun boğaz bölümünden yarına yer bulunur mu?",
        "test_73_ortopedi_bel_agrisi": "Bel fıtığım için ortopedi ve travmatoloji bölümüne randevu rica ediyorum.",
        "test_74_kbb_kulak_cinlamasi": "Geçmeyen kulak çınlamam var, kbb bölümüne randevu rica ediyorum.",
        "test_75_ortopedi_kirik": "Kırık tedavisi sonrası kontrol için ortopedi doktoruna randevu lazım.",
        "test_76_kbb_burun_tikanikligi": "Aylardır burnum tıkalı, kulak burun boğaz bölümünden randevu rica ediyorum.",
        "test_77_ortopedi_boyun_fitigi": "Boyun fıtığım için ortopedi bölümüne gitmem lazım, yer var mı?",
        "test_78_kbb_ses_kisikligi": "Sesim kısıldı çıkmıyor, kulak burun boğaz bölümüne bir randevu ayarla.",
        "test_79_ortopedi_topuk": "Topuk dikenim var, ortopedi doktoru için yer bakar mısın?",

        # NÖROLOJİ VARYASYONLARI
        "test_80_noroloji_bas_agrisi": "Sürekli baş ağrım var, nöroloji bölümünden bir doktora görünmem gerek.",
        "test_81_noroloji_uyusma": "Kollarımda uyuşma var, nöroloji doktoruna en erken ne zaman gidebilirim?",
        "test_82_noroloji_epilepsi": "Epilepsi kontrolüm için nöroloji bölümünden önümüzdeki aya randevu bak.",
        "test_83_noroloji_titreme": "Ellerimde titreme başladı, nöroloji bölümünden en erken randevuyu al.",
        "test_84_noroloji_alzheimer": "Alzheimer kontrolü için nöroloji bölümüne ayın yirmisine randevu al.",
        "test_85_noroloji_unutkanlik": "Son zamanlarda çok unutkanım, nörolojiye muayene olmak istiyorum.",

        # İPTAL, SORGULAMA VE SİSTEM TESTLERİ (EDGE CASES)
        "test_86_randevu_sorgula_tarih": "Ayın on beşindeki randevumun saatini öğrenebilir miyim?",
        "test_87_randevu_iptal_gerekce": "Şehir dışına çıkacağım için yarınki randevumu iptal edin.",
        "test_88_randevu_tarih_degistir": "Mevcut randevumun tarihini haftaya pazartesi olarak değiştirebilir miyiz?",
        "test_89_iptal_yanlis_bolum": "Yanlış bölümden almışım, o randevuyu tamamen iptal eder misin?",
        "test_90_sorgula_doktor_isim": "Randevu aldığım doktorun ismini tekrar söyler misin?",
        "test_91_sorgula_hangi_hastane": "Benim randevum tam olarak hangi hastanedeydi?",
        "test_92_iptal_is_cikisi": "İşim çıktığı için öğleden sonraki randevumu iptal etmek zorundayım.",
        "test_93_iptal_gittim": "Ben zaten hastaneye gittim, o randevuyu sistemden iptal edebilir misin?",
        "test_94_sorgula_saat_kacti": "Bugün bir randevum olacaktı ama saati tam olarak kaçtaydı?",
        "test_95_iptal_hepsini": "Sistemdeki ileri tarihli tüm randevularımı iptal etmek istiyorum.",
        "test_96_sorgula_tarih_dogrumu": "Yarın sabah dokuz buçukta dahiliye randevum var, doğru mu?",
        "test_97_coklu_dahiliye_goz": "Hem dahiliyeden hem de göz hastalıklarından aynı güne randevu alabilir miyiz?",
        "test_98_baska_sehir": "Ankara'daki bir hastanenin ortopedi bölümünden randevu ayarlayabilir misin?",
        "test_99_doktor_secimi": "Dahiliye bölümünden sadece kadın bir doktora randevu almak istiyorum.",
        "test_100_hizli_kardiyoloji": "En acilinden kardiyoloji randevusu ver."
    }

    print(f"Toplam {len(senaryolar)} test sesi üretilmeye başlanıyor...\n")

    for dosya_adi, metin in senaryolar.items():
        print(f"Üretiliyor: {dosya_adi}.webm ...")
        
        mp3_yolu = os.path.join(klasor_adi, f"{dosya_adi}.mp3")
        webm_yolu = os.path.join(klasor_adi, f"{dosya_adi}.webm")
        
        # 1. Adım: gTTS ile metni sese çevir ve geçici olarak MP3 olarak kaydet
        tts = gTTS(text=metin, lang='tr')
        tts.save(mp3_yolu)
        
        # 2. Adım: ffmpeg kullanarak MP3'ü WebM formatına dönüştür
        # Not: Sisteminize ffmpeg'in kurulu ve PATH'e eklenmiş olması gerekir.
        try:
            subprocess.run(
                ['ffmpeg', '-i', mp3_yolu, '-y', webm_yolu], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            # İşlem bittikten sonra geçici MP3 dosyasını sil (sadece .webm kalsın)
            if os.path.exists(mp3_yolu):
                os.remove(mp3_yolu)
        except FileNotFoundError:
            print(f"UYARI: Sisteminizde 'ffmpeg' bulunamadı! {dosya_adi} dosyası .mp3 olarak bırakıldı.")
            print("Whisper modeli .mp3 dosyalarını da doğrudan okuyabilir, testlerinizde mp3 kullanabilirsiniz.")

    print("\n✅ Harika! Tüm test ses dosyaları 'test_data' klasörüne başarıyla üretildi!")

if __name__ == "__main__":
    ses_dosyalarini_uret()