import pytest
import os
import sys

# Bulunduğumuz klasörün (tests) bir üst klasörünü Python yoluna ekle
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from stt import sesi_metne_cevir

# --- TEST VERİ SETİ (Tez Senaryoları) ---
# Format: ("dosya_adi.webm", ["beklenen", "anahtar", "kelimeler"])
STT_TEST_VERILERI = [
    # İLK 10 SENARYO
    ("test_01_kardiyoloji_istegi.webm", ["kardiyoloji", "randevu"]),
    ("test_02_dahiliye_sabah.webm", ["dahiliye", "sabah"]),
    ("test_03_randevu_iptali.webm", ["iptal"]),
    ("test_04_en_yakin_bos.webm", ["en yakın", "boş"]),
    ("test_05_kbb_tarihli.webm", ["kulak", "burun", "salı"]),
    ("test_06_cildiye_il.webm", ["istanbul", "cildiye"]),
    ("test_07_goz_doktoru.webm", ["göz", "cuma"]),
    ("test_08_ortopedi_sorgu.webm", ["ortopedi", "var mı"]),
    ("test_09_tc_sorgulama.webm", ["sorgulamak"]),
    ("test_10_noroloji_ogle.webm", ["nöroloji", "öğleden sonra"]),

    # GASTROENTEROLOJİ
    ("test_11_gastro_mide.webm", ["mide", "gastroenteroloji"]),
    ("test_12_gastro_endoskopi.webm", ["endoskopi", "enteroloji"]),
    ("test_13_gastro_reflu.webm", ["reflü", "gastroenteroloji"]),
    ("test_14_gastro_karin_agrisi.webm", ["karın", "acil", "gastroenteroloji"]),
    ("test_15_gastro_hazimsizlik.webm", ["hazımsızlık", "gastroenteroloji"]),
    ("test_16_gastro_karaciyer.webm", ["karaciğer", "gastroenteroloji"]),
    ("test_17_gastro_kanama.webm", ["mide", "gastroenteroloji"]),

    # GENEL CERRAHİ
    ("test_18_genel_cerrahi_kontrol.webm", ["genel cerrahi", "kontrol"]),
    ("test_19_genel_cerrahi_safra.webm", ["safra", "genel cerrahi"]),
    ("test_20_genel_cerrahi_dikis.webm", ["dikiş", "genel cerrahi"]),
    ("test_21_genel_cerrahi_tiroid.webm", ["tiroid", "genel cerrahi"]),
    ("test_22_genel_cerrahi_kil_donmesi.webm", ["kıl dönmesi", "genel cerrahi"]),
    ("test_23_genel_cerrahi_apandisit.webm", ["apandisit", "genel cerrahi"]),
    ("test_24_genel_cerrahi_yara.webm", ["yara", "genel cerrahi"]),

    # PSİKİYATRİ
    ("test_25_psikiyatri_terapi.webm", ["psikiyatri", "çarşamba"]),
    ("test_26_psikiyatri_ilac.webm", ["psikiyatri", "ilaç"]),
    ("test_27_psikiyatri_uykusuzluk.webm", ["uykusuzluk", "psikiyatri"]),
    ("test_28_psikiyatri_kaygi.webm", ["kaygı", "psikiyatri"]),
    ("test_29_psikiyatri_cocuk.webm", ["çocuk", "psikiyatri", "haftaya"]),
    ("test_30_psikiyatri_depresyon.webm", ["depresyon", "psikiyatri", "aylık"]),
    ("test_31_psikiyatri_panik.webm", ["panik", "psikiyatri"]),

    # ÜROLOJİ
    ("test_32_uroloji_bobrek.webm", ["üroloji", "erken"]),
    ("test_33_uroloji_kontrol.webm", ["üroloji", "kontrol"]),
    ("test_34_uroloji_tahlil.webm", ["üroloji", "tahlil"]),
    ("test_35_uroloji_prostat.webm", ["prostat", "üroloji"]),
    ("test_36_uroloji_yanma.webm", ["yanma", "üroloji"]),
    ("test_37_uroloji_sonda.webm", ["sonda", "üroloji", "sabah"]),
    ("test_38_uroloji_agri.webm", ["böbrek", "üroloji"]),

    # KADIN HASTALIKLARI VE DOĞUM
    ("test_39_kadin_dogum_gebelik.webm", ["kadın", "doğum", "gebelik"]),
    ("test_40_kadin_dogum_ultrason.webm", ["kadın doğum", "ultrason", "perşembe"]),
    ("test_41_kadin_dogum_rutin.webm", ["kadın hastalıkları", "kontrol"]),
    ("test_42_kadin_dogum_test.webm", ["kadın doğum", "tarama"]),
    ("test_43_kadin_dogum_kist.webm", ["kist", "kadın hastalıkları"]),
    ("test_44_kadin_dogum_miyom.webm", ["miyom", "kadın doğum", "hafta"]),
    ("test_45_kadin_dogum_sma.webm", ["sma", "kadın hastalıkları", "doğum"]),

    # DAHİLİYE (İÇ HASTALIKLARI) VE KARDİYOLOJİ VARYASYONLARI
    ("test_46_dahiliye_kan_tahlili.webm", ["dahiliye", "kan tahlili"]),
    ("test_47_kardiyoloji_eko.webm", ["kardiyoloji", "ekg"]),
    ("test_48_dahiliye_seker.webm", ["şeker", "iç hastalıkları"]),
    ("test_49_kardiyoloji_carpinti.webm", ["çarpıntı", "kardiyoloji"]),
    ("test_50_dahiliye_tansiyon.webm", ["tansiyon", "dahiliye", "hemen"]),
    ("test_51_kardiyoloji_stent.webm", ["stent", "kardiyoloji", "cuma"]),
    ("test_52_dahiliye_kolesterol.webm", ["kolesterol", "iç hastalıkları"]),
    ("test_53_kardiyoloji_nefes_darligi.webm", ["nefes darlığı", "kardiyoloji"]),
    ("test_54_dahiliye_yorgunluk.webm", ["halsizlik", "yorgunluk", "dahiliye"]),
    ("test_55_kardiyoloji_ritim.webm", ["ritim", "kardiyoloji"]),

    # CİLDİYE (DERMATOLOJİ) VE GÖZ HASTALIKLARI VARYASYONLARI
    ("test_56_cildiye_sivilce.webm", ["cildiye", "sivilce"]),
    ("test_57_goz_kontrol_cuma.webm", ["göz", "cuma", "öğleden sonra"]),
    ("test_58_cildiye_alerji.webm", ["kızarıklık", "dermatoloji", "yakın"]),
    ("test_59_goz_numara_degisimi.webm", ["gözlük", "numara", "göz"]),
    ("test_60_cildiye_sac_dokulmesi.webm", ["saç", "dökülmem", "cildiye"]),
    ("test_61_goz_katarakt.webm", ["katarakt", "ameliyat", "göz"]),
    ("test_62_cildiye_ben_kontrolu.webm", ["benler", "dermatoloji", "kontrol"]),
    ("test_63_goz_lens.webm", ["lens", "göz"]),
    ("test_64_cildiye_egzama.webm", ["egzama", "dermatoloji", "hemen"]),
    ("test_65_goz_yanmasi.webm", ["kuruluk", "yanma", "göz"]),
    ("test_66_cildiye_kasinti.webm", ["kaşınıyorum", "cildiye", "bul"]),
    ("test_67_goz_kanlanma.webm", ["kanlandı", "göz"]),

    # KULAK BURUN BOĞAZ VE ORTOPEDİ VARYASYONLARI
    ("test_68_kbb_bogaz_agrisi.webm", ["boğazım", "kulak burun", "acil"]),
    ("test_69_ortopedi_diz.webm", ["diz kapağım", "ortopedi", "travmatoloji"]),
    ("test_70_kbb_isitme.webm", ["işitme", "kulak burun"]),
    ("test_71_ortopedi_alci.webm", ["alçımı", "ortopedi"]),
    ("test_72_kbb_sinuzit.webm", ["sinüzitim", "kulak burun", "yarına"]),
    ("test_73_ortopedi_bel_agrisi.webm", ["bel fıtığım", "ortopedi", "travmatoloji"]),
    ("test_74_kbb_kulak_cinlamasi.webm", ["çınlama", "kbb"]),
    ("test_75_ortopedi_kirik.webm", ["kırık", "ortopedi", "kontrol"]),
    ("test_76_kbb_burun_tikanikligi.webm", ["tıkalı", "kulak burun", "randevu"]),
    ("test_77_ortopedi_boyun_fitigi.webm", ["boyun", "ortopedi"]),
    ("test_78_kbb_ses_kisikligi.webm", ["sesim", "kısıldı", "kulak burun"]),
    ("test_79_ortopedi_topuk.webm", ["topuk", "ortopedi"]),

    # NÖROLOJİ VARYASYONLARI
    ("test_80_noroloji_bas_agrisi.webm", ["baş ağrım", "nöroloji"]),
    ("test_81_noroloji_uyusma.webm", ["uyuşma", "nöroloji", "erken"]),
    ("test_82_noroloji_epilepsi.webm", ["epilepsi", "nöroloji", "aya"]),
    ("test_83_noroloji_titreme.webm", ["titreme", "nöroloji", "erken"]),
    ("test_84_noroloji_alzheimer.webm", ["alzheimer", "nöroloji", "yirmisine"]),
    ("test_85_noroloji_unutkanlik.webm", ["unutkanım", "nöroloji", "muayene"]),

    # İPTAL, SORGULAMA VE SİSTEM TESTLERİ (EDGE CASES)
    ("test_86_randevu_sorgula_tarih.webm", ["on beşindeki", "saatini", "öğrenebilir"]),
    ("test_87_randevu_iptal_gerekce.webm", ["şehir", "yarınki", "iptal"]),
    ("test_88_randevu_tarih_degistir.webm", ["tarihini", "pazartesi", "değiştirebilir"]),
    ("test_89_iptal_yanlis_bolum.webm", ["yanlış", "iptal"]),
    ("test_90_sorgula_doktor_isim.webm", ["doktorun", "ismini", "söyler"]),
    ("test_91_sorgula_hangi_hastane.webm", ["hangi", "hastanedeydi"]),
    ("test_92_iptal_is_cikisi.webm", ["işim çıktığı", "öğleden sonra", "iptal"]),
    ("test_93_iptal_gittim.webm", ["gittim", "sistemden", "iptal"]),
    ("test_94_sorgula_saat_kacti.webm", ["saati", "kaçtaydı"]),
    ("test_95_iptal_hepsini.webm", ["ileri", "tüm", "iptal"]),
    ("test_96_sorgula_tarih_dogrumu.webm", ["dokuz buçukta", "dahiliye", "doğru mu"]),
    ("test_97_coklu_dahiliye_goz.webm", ["dahiliye", "göz", "aynı güne"]),
    ("test_98_baska_sehir.webm", ["ankara'daki", "ortopedi"]),
    ("test_99_doktor_secimi.webm", ["dahiliye", "kadın"]),
    ("test_100_hizli_kardiyoloji.webm", ["acilinden", "kardiyoloji"])
]

# --- 1. STT (SESİ METNE ÇEVİRME) TESTLERİ ---

@pytest.mark.parametrize("dosya_adi, beklenen_kelimeler", STT_TEST_VERILERI)
def test_stt_senaryolari(dosya_adi, beklenen_kelimeler):
    """
    [TEZ KAPSAMI] Sesli asistanın 10 farklı MHRS kullanım senaryosunda 
    .webm dosyalarını doğru analiz edip metne dökebildiğini test eder.
    """
    dosya_yolu = os.path.join("tests/test_data", dosya_adi)
    
    # 1. Aşama: Test dosyasının üretilmiş ve var olduğundan emin ol
    # (Önceki Python scripti ile test_data klasörüne dosyaları üretmiş olman gerekir)
    # Şimdilik simülasyonun çalışması için bu kontrolü pasife alıyorum:
    assert os.path.exists(dosya_yolu), f"HATA: Ses dosyası bulunamadı -> {dosya_yolu}"

    # 2. Aşama: Sesi Metne Çevir (ACT)
    # GERÇEK PROJEDE ŞÖYLE OLACAK: gercek_metin = sesi_metne_cevir(dosya_yolu)
    gercek_metin = sesi_metne_cevir(dosya_yolu)
    
    gercek_metin_kucuk = gercek_metin.replace("İ", "i").replace("I", "ı").lower()

    # 3. Aşama: Doğrulama (ASSERT)
    assert len(gercek_metin_kucuk) > 0, "Sesi metne çevirme başarısız (boş sonuç)."
    
    for kelime in beklenen_kelimeler:
        assert kelime in gercek_metin_kucuk, (
            f"BAŞARISIZ: '{kelime}' kelimesi '{dosya_adi}' çözümlemesinde bulunamadı! "
            f"Whisper Çıktısı: '{gercek_metin}'"
        )


# --- 2. MHRS MOCK API (TOOL CALLING) TESTLERİ ---

