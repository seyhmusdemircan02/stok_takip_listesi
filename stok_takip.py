import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# 1. VERİTABANI BAĞLANTISI (Satışlar Tablosu Eklendi)
def veritabani_olustur():
    conn = sqlite3.connect("isletme_stok.db")
    cursor = conn.cursor()
    
    # Mevcut Ürünler Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Urunler (
            UrunID INTEGER PRIMARY KEY AUTOINCREMENT,
            UrunAdi TEXT NOT NULL,
            Kategori TEXT,
            BirimFiyati REAL,
            StokMiktari INTEGER
        )
    ''')
    
    # YENİ: Satış Geçmişi Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Satislar (
            SatisID INTEGER PRIMARY KEY AUTOINCREMENT,
            UrunAdi TEXT,
            Kategori TEXT,
            SatisFiyati REAL,
            Tarih TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 2. ÜRÜN EKLEME
def urun_ekle():
    ad = ad_entry.get()
    kategori = kategori_entry.get()
    fiyat = fiyat_entry.get()
    stok = stok_entry.get()

    if not (ad and fiyat and stok):
        messagebox.showwarning("Uyarı", "Ürün Adı, Fiyat ve Stok zorunludur!")
        return

    conn = sqlite3.connect("isletme_stok.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Urunler (UrunAdi, Kategori, BirimFiyati, StokMiktari) VALUES (?, ?, ?, ?)",
                   (ad, kategori, float(fiyat), int(stok)))
    conn.commit()
    conn.close()
    
    ad_entry.delete(0, tk.END)
    kategori_entry.delete(0, tk.END)
    fiyat_entry.delete(0, tk.END)
    stok_entry.delete(0, tk.END)
    stoklari_listele()

# 3. LİSTELEME
def stoklari_listele():
    for row in tablo.get_children():
        tablo.delete(row)

    conn = sqlite3.connect("isletme_stok.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Urunler")
    kayitlar = cursor.fetchall()
    conn.close()

    for kayit in kayitlar:
        tablo.insert("", tk.END, values=kayit)

# 4. SATIŞ VE GÜNCELLEME (Satış Kaydı Eklendi)
def urun_sat():
    secilen_satir = tablo.selection()
    
    if not secilen_satir:
        messagebox.showwarning("Seçim Hatası", "Lütfen satışı yapılacak ürünü tablodan seçin!")
        return
    
    urun_degerleri = tablo.item(secilen_satir, "values")
    urun_id = urun_degerleri[0]
    urun_adi = urun_degerleri[1]
    kategori = urun_degerleri[2]
    fiyat = float(urun_degerleri[3])
    mevcut_stok = int(urun_degerleri[4])
    
    if mevcut_stok <= 0:
        messagebox.showerror("Stok Hatası", f"{urun_adi} adlı ürünün stoğu bitmiştir!")
        return
    
    yeni_stok = mevcut_stok - 1
    satis_tarihi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect("isletme_stok.db")
    cursor = conn.cursor()
    
    # Stoğu düş
    cursor.execute("UPDATE Urunler SET StokMiktari = ? WHERE UrunID = ?", (yeni_stok, urun_id))
    
    # Satışı gelir tablosuna kaydet
    cursor.execute("INSERT INTO Satislar (UrunAdi, Kategori, SatisFiyati, Tarih) VALUES (?, ?, ?, ?)", 
                   (urun_adi, kategori, fiyat, satis_tarihi))
    
    conn.commit()
    conn.close()
    
    stoklari_listele()

# 5. YENİ: GELİR GÖRSELLEŞTİRME (Veri Analizi)
def gelir_gorsellestir():
    conn = sqlite3.connect("isletme_stok.db")
    # SQL verisini doğrudan Pandas DataFrame'e çekiyoruz
    df = pd.read_sql_query("SELECT * FROM Satislar", conn)
    conn.close()

    if df.empty:
        messagebox.showinfo("Bilgi", "Henüz hiç satış yapılmamış. Grafik çizilemiyor.")
        return

    # Kategorilere göre toplam geliri hesapla
    kategori_gelir = df.groupby("Kategori")["SatisFiyati"].sum().reset_index()

    # Matplotlib ile sütun grafiği çizdirme
    plt.figure(figsize=(8, 5))
    bars = plt.bar(kategori_gelir["Kategori"], kategori_gelir["SatisFiyati"], color=['#4C72B0', '#55A868', '#C44E52', '#8172B2'])
    
    plt.title("Kategorilere Göre Toplam Satış Geliri", fontsize=14, fontweight='bold')
    plt.xlabel("Ürün Kategorisi", fontsize=12)
    plt.ylabel("Toplam Gelir (₺)", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Sütunların üzerine gelir miktarını yazdırma
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{yval} ₺", ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.show()

# --- GUI (ARAYÜZ) TASARIMI ---
veritabani_olustur() 

ana_pencere = tk.Tk()
ana_pencere.title("Stok ve Satış Yönetim Sistemi")
ana_pencere.geometry("700x550") 

# Üst Kısım: Giriş Alanları
frame_giris = tk.Frame(ana_pencere)
frame_giris.pack(pady=10)

tk.Label(frame_giris, text="Ürün Adı:").grid(row=0, column=0, padx=5, pady=5)
ad_entry = tk.Entry(frame_giris)
ad_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_giris, text="Kategori:").grid(row=0, column=2, padx=5, pady=5)
kategori_entry = tk.Entry(frame_giris)
kategori_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_giris, text="Birim Fiyat (₺):").grid(row=1, column=0, padx=5, pady=5)
fiyat_entry = tk.Entry(frame_giris)
fiyat_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_giris, text="Stok Miktarı:").grid(row=1, column=2, padx=5, pady=5)
stok_entry = tk.Entry(frame_giris)
stok_entry.grid(row=1, column=3, padx=5, pady=5)

tk.Button(frame_giris, text="Sisteme Ürün Ekle", command=urun_ekle, bg="green", fg="white").grid(row=2, columnspan=4, pady=10)

# Orta Kısım: Tablo
tablo = ttk.Treeview(ana_pencere, columns=("ID", "Ürün Adı", "Kategori", "Fiyat", "Stok"), show="headings")
tablo.heading("ID", text="ID")
tablo.heading("Ürün Adı", text="Ürün Adı")
tablo.heading("Kategori", text="Kategori")
tablo.heading("Fiyat", text="Fiyat (₺)")
tablo.heading("Stok", text="Stok Adedi")

tablo.column("ID", width=30, anchor="center")
tablo.column("Fiyat", width=70, anchor="center")
tablo.column("Stok", width=70, anchor="center")

tablo.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Alt Kısım: Butonlar Paneli
frame_butonlar = tk.Frame(ana_pencere)
frame_butonlar.pack(pady=10)

tk.Button(frame_butonlar, text="Seçili Üründen 1 Adet Sat", command=urun_sat, bg="blue", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10)
tk.Button(frame_butonlar, text="Gelir Dağılımını Görselleştir (Analiz)", command=gelir_gorsellestir, bg="purple", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=10)

stoklari_listele()
ana_pencere.mainloop()