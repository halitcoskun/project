# Otonom MHRS Randevu Asistanı (LLM & STT Tabanlı)

## 🚀 MHRS Agent Kurulumu

**1. Projeyi Klonlayın ve Klasöre Girin**

```
git clone https://github.com/halitcoskun/project.git
cd mhrs-agent
```

**2. Bağımlılıkları Yükleyin**

Sistemin çalışması için gerekli kütüphaneleri tek komutla kurun:

```
pip install -r requirements.txt
```

🎙️ **Whisper STT Modelinin Yüklenmesi (Otomatik İndirme)**

Projede sesten metne (STT) dönüşüm için **OpenAI Whisper Large** modeli kullanılmaktadır. Modelin boyutu oldukça büyük (~2.9 GB) olduğu için GitHub deposuna dahil edilmemiştir. 

Sistemi kendi bilgisayarınızda ayağa kaldırırken modeli manuel olarak bir yerden indirmenize **gerek yoktur.** Gerekli yapılandırmalar kod içerisine entegre edilmiştir.

**Model Nasıl İndirilir?**

Projenin gereksinimlerini (`pip install -r requirements.txt`) kurduktan sonra test betiklerini veya ana sunucuyu ilk kez çalıştırdığınızda, sistem modeli otomatik olarak indirecektir.

Örneğin, aşağıdaki test komutunu ilk kez çalıştırdığınızda:
`python tests/test_core.py`

* Whisper kütüphanesi arka planda `large` modelini OpenAI sunucularından çekecektir.
* İndirilen model bilgisayarınızın önbellek (cache) dizinine (Windows için genellikle `C:\Users\KullaniciAdi\.cache\whisper`) kaydedilir.
* İndirme işlemi internet hızınıza bağlı olarak birkaç dakika sürebilir. İndirme tamamlandıktan sonraki tüm çalıştırmalarda sistem önbellekteki modeli kullanacağı için STT motoru saniyeler içinde anında hazır hale gelecektir.

**Not:** Modelin çalışabilmesi ve sesten metne dönüşüm yapabilmesi için sisteminizde [FFmpeg](https://ffmpeg.org/) aracının kurulu ve sistem `PATH` değişkenine eklenmiş olması gerekmektedir.


⚙️ **FFmpeg Kurulumu ve PATH Ayarları (Zorunlu Gereksinim)**

Whisper modelinin ses dosyalarını (mikrofondan gelen veya kayıtlı dosyaları) işleyebilmesi için işletim sisteminizde FFmpeg aracının kurulu ve sistem değişkenlerine (PATH) eklenmiş olması zorunludur. Aksi takdirde FileNotFoundError veya ffprobe hataları alırsınız.

İşletim sisteminize göre aşağıdaki kurulum adımlarını izleyin:

⚙️ **Windows Kullanıcıları İçin Kurulum:**

Windows'ta FFmpeg'i kurmak ve sisteme tanıtmak için şu adımları sırasıyla uygulayın:

İndirme: gyan.dev/ffmpeg/builds/ adresine gidin ve ffmpeg-git-full.7z (veya .zip) sürümünü indirin.

Çıkartma: İndirdiğiniz arşiv dosyasını C:\ dizinine çıkartın ve klasörün adını ffmpeg olarak kısaltın. (Örnek yol: C:\ffmpeg olmalıdır).

PATH (Ortam Değişkenleri) Ayarı:

Windows Başlat menüsüne "Ortam değişkenleri" (Environment variables) yazın ve "Sistem ortam değişkenlerini düzenle" seçeneğine tıklayın.

Açılan pencerede sağ alttaki "Ortam Değişkenleri..." butonuna tıklayın.

Alt kısımdaki "Sistem değişkenleri" listesinden Path satırını bulup çift tıklayın.

Sağ üstteki "Yeni" butonuna basarak şu dizini ekleyin: C:\ffmpeg\bin

Tüm pencerelere "Tamam" diyerek kapatın.

Doğrulama: Sistemin FFmpeg'i tanıdığından emin olmak için VS Code'u veya terminalinizi kapatıp yeniden açın. Yeni terminalde şu komutu çalıştırın:

Bash
```
ffmpeg -version
```
Eğer ekranda FFmpeg versiyon bilgileri listeleniyorsa, kurulum kusursuz tamamlanmış demektir.

🍏 macOS Kullanıcıları İçin:
Terminal üzerinden Homebrew kullanarak tek komutla kurabilirsiniz:

Bash
```
brew install ffmpeg
```
🐧 **Linux (Ubuntu/Debian) Kullanıcıları İçin:**
Terminal üzerinden apt paket yöneticisi ile kurabilirsiniz:

Bash
```
sudo apt update && sudo apt install ffmpeg
```


## ⚙️ Uygulamayı Çalıştırma

Tüm kurulumlar tamamlandıktan sonra FastAPI sunucusunu ayağa kaldırmak için ana dizinde şu komutu çalıştırın:

```
uvicorn main:app --reload
```

Sistem `http://localhost:8000` portu üzerinden dinlemeye başlayacaktır.
