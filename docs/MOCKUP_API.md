# Otonom MHRS Randevu Asistanı (LLM & STT Tabanlı)

## 🏥 MHRS Mock API - C# / .NET 8 Entegrasyon Rehberi

Bu doküman, Otonom MHRS Asistanı'nın Python tabanlı backend sistemi ile haberleşen, randevu süreçlerini simüle eden C# Mock API'nin kurulumunu, IIS (Internet Information Services) konfigürasyonunu ve gerekli ortam ayarlarını içermektedir.

**Proje Genel Bakış**

Mock API, gerçek MHRS servislerini taklit eden bir ASP.NET Core Web API projesidir. Yapay zeka ajanı (Llama 3), kullanıcıdan aldığı sesli komutları analiz ederek bu API üzerindeki endpoint'lere istek (request) atar ve randevu kayıtlarını yönetir.

**Sistem Gereksinimleri**

API'nin çalışabilmesi ve IIS üzerinde barındırılabilmesi için aşağıdaki bileşenlerin yüklü olması zorunludur:

.NET 8 SDK & Runtime: Projenin derlenmesi ve çalışması için en güncel .NET 8 sürümü gereklidir.

.NET Core Hosting Bundle: IIS üzerinde .NET 8 uygulamalarını çalıştırmak için Microsoft .NET 8 Hosting Bundle kurulmalıdır.

IIS (Internet Information Services): Windows üzerinde yerel bir sunucu hizmeti.

**IIS ve Windows Özelliklerinin Yapılandırılması**

IIS'in API'yi doğru bir şekilde sunabilmesi için aşağıdaki özelliklerin Windows üzerinden aktif edilmesi gerekir:

Denetim Masası > Programlar > Windows Özelliklerini Aç veya Kapat menüsüne gidin.

Internet Information Services ana düğümünü bulun ve şu özellikleri işaretleyin:

World Wide Web Hizmetleri > Uygulama Geliştirme Özellikleri:

.NET Extensibility 4.8

ASP.NET 4.8

WebSocket Protokolü

Tamam'a basarak kurulumun tamamlanmasını bekleyin.

**IIS Üzerinde Site Yayını (Deployment)**

Derlenmiş (Publish alınmış) Mock API dosyalarını IIS üzerine taşımak için şu adımları izleyin:

**1. Application Pool (Uygulama Havuzu) Ayarı**

IIS Manager'ı açın ve Application Pools sekmesine gelin.

Yeni bir havuz oluşturun (Örn: MHRS_Pool).

.NET CLR Version kısmını "No Managed Code" (Yönetilen Kod Yok) olarak ayarlayın. (Not: .NET Core/5/6/8 projeleri kendi çalışma zamanlarını kullandıkları için IIS tarafında yönetilen koda ihtiyaç duymazlar).

**2. Site Ekleme ve Binding**

Sites klasörüne sağ tıklayın ve Add Website seçeneğine basın.

Physical Path: Projenin yayın (publish) dosyalarının bulunduğu klasörü seçin.

Binding:

Port: 5001 (Veya Python kodunuzdaki MOCK_API_URL değişkeni ile eşleşen port).

IP Address: All Unassigned veya 127.0.0.1.

**API Endpoint ve Veri Yapısı**

Asistanın kullandığı temel API rotaları şunlardır:

Metot,Endpoint,İşlev
POST,/api/Mhrs/CheckAvailability,Uygun poliklinik ve saatleri listeler.
POST,/api/Mhrs/BookAppointment,Yeni bir randevu kaydı oluşturur.
POST,/api/Mhrs/CancelAppointment,Mevcut bir randevuyu iptal eder.
POST,/api/Mhrs/ListAppointment,Kayıtlı randevuları listeler.

Örnek JSON Yanıtı (Success Response):

```
{
  "isAvailable": true,
  "doctorName": "Dr. Nebahat Çağla",
  "timeSlot": "2026-05-10 09:30:00"
}
```

**Python Backend Bağlantısı**

API başarıyla ayağa kalktıktan sonra, main.py dosyanızdaki BASE_URL değişkeninin IIS üzerindeki adresle eşleştiğinden emin olun:

```
# main.py içindeki API konfigürasyonu
MOCK_API_URL = "http://localhost:5001/api/Appointment"
```

**Hata Giderme (Troubleshooting)**

500.19 Error: web.config dosyasındaki izinlerin yetersiz olduğunu gösterir. Klasör izinlerinden IIS_IUSRS kullanıcısına "Okuma ve Yazma" yetkisi verin.

502.5 Process Failure: .NET Core Hosting Bundle'ın kurulu olmadığını veya yanlış mimaride (x86/x64 çakışması) kurulduğunu gösterir. Hosting Bundle'ı onarın.

CORS Hatası: Eğer tarayıcı üzerinden erişimde sorun yaşıyorsanız, C# projesindeki Program.cs içinde app.UseCors() politikasının tanımlı olduğundan emin olun.

**Veritabanı Entegrasyonu ve ORM Yapısı**

Mock API, randevu verilerini yalnızca çalışma zamanında (in-memory) tutmak yerine, gerçek dünya senaryolarını tam anlamıyla simüle edebilmek için kalıcı bir ilişkisel veritabanı ile entegre edilmiştir. Veri erişim katmanında (Data Access Layer) modern .NET mimarisinin standart ORM (Object-Relational Mapping) aracı olan Entity Framework Core (EF Core) kullanılmıştır. Code-First yaklaşımı ile oluşturulan modeller, appsettings.json içerisindeki Connection String üzerinden veritabanına bağlanarak ajanın otonom olarak ürettiği randevu oluşturma, iptal etme ve uygunluk sorgulama işlemlerinin ACID (Atomicity, Consistency, Isolation, Durability) prensiplerine uygun olarak diske yazılmasını ve yönetilmesini sağlamaktadır.

MSSQL DB Script: [[https://github.com/halitcoskun/project/blob/main/mhrsdb.sql]](https://github.com/halitcoskun/project/blob/main/mhrsdb.sql)
