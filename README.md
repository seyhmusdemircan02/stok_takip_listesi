# stok_takip_listesi
# 📦 Stok ve Satış Yönetim Sistemi (Inventory & Sales Management System)

Bu proje, işletmelerin günlük stok hareketlerini takip etmelerini ve satış verilerini analiz ederek stratejik kararlar almalarını sağlayan, Python tabanlı bir masaüstü Yönetim Bilişim Sistemi (MIS) uygulamasıdır.

## 📌 Projenin İş Amacı (Business Value)
Küçük ve orta ölçekli işletmelerin (KOBİ) ürün envanterini dijitalleştirmek ve manuel hata payını sıfıra indirmek hedeflenmiştir. Uygulama sadece veriyi depolamakla kalmaz; aynı zamanda bir **Karar Destek Sistemi (Decision Support System)** olarak çalışarak, yöneticilere "Hangi ürün kategorisi işletmeye daha fazla gelir sağlıyor?" sorusunun cevabını görsel raporlarla sunar.

## 🛠️ Kullanılan Teknolojiler
Bu projede veri tabanı yönetimi, arayüz tasarımı ve veri analizi süreçleri uçtan uca entegre edilmiştir:
* **Python 3.x:** Temel programlama ve iş mantığı.
* **SQLite3:** Verilerin ilişkisel (RDBMS) olarak kalıcı ve güvenli bir şekilde saklanması.
* **Tkinter:** Kullanıcı dostu, etkileşimli masaüstü arayüzünün (GUI) oluşturulması.
* **Pandas:** Veritabanından (SQL) çekilen satış verilerinin DataFrame formatında işlenmesi ve gruplanması.
* **Matplotlib:** Finansal verilerin kategorik bazda iş zekası (BI) grafiklerine dönüştürülmesi.

## 🌟 Temel Özellikler
* **CRUD Operasyonları:** Veritabanına yeni ürün ekleme (Create) ve ürünleri listeleme (Read).
* **Dinamik Stok Yönetimi:** Yapılan her satışta `UPDATE` sorgularıyla stok miktarının anında düşürülmesi ve negatif stoğun engellenmesi.
* **Satış Geçmişi Takibi:** Satılan ürünlerin fiyat, kategori ve zaman damgasıyla (timestamp) birlikte ayrı bir `Satislar` SQL tablosuna kaydedilmesi.
* **Finansal Veri Görselleştirme:** Tek tuşla satış geçmişinin analiz edilerek, kategorilere göre elde edilen toplam gelirin sütun grafiği olarak raporlanması.

## 💻 Kurulum ve Çalıştırma

Projeyi bilgisayarınızda çalıştırmak için:

1. Repoyu bilgisayarınıza klonlayın:
   ```bash
   git clone [https://github.com/kullaniciadiniz/stok-satis-yonetim.git](https://github.com/kullaniciadiniz/stok-satis-yonetim.git)
