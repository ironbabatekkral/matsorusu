# 📐 Matematik Soru Hazırlayıcı

TYT/AYT seviyesinde rastgele matematik soruları üreten ve PDF olarak kaydeden Tkinter tabanlı masaüstü uygulaması.

## 🎯 Özellikler

- **8 Farklı Konu:** Temel İşlemler, Sayılar, 1. ve 2. Derece Denklemler, Fonksiyonlar, Mutlak Değer, Üslü ve Köklü İfadeler
- **Konu Seçimi:** Checkbox ile istediğiniz konuları seçin
- **Ayarlanabilir Soru Sayısı:** 10 ile 2000 arası, butonlarla veya elle giriş
- **PDF Çıktısı:** Sorular + Cevap Anahtarı, opsiyonel çözümlü PDF
- **Modern Arayüz:** Koyu tema, kullanıcı dostu tasarım

## 📦 Kurulum

### Gereksinimler

- Python 3.7+
- `fpdf2` kütüphanesi

### Bağımlılık Kurulumu

```bash
pip install fpdf2
```

> **Not:** Uygulama açılırken `fpdf2` kurulu değilse otomatik olarak kurmaya çalışır.

## 🚀 Kullanım

```bash
cd matsorusu
python mat_soru_gui.py
```

### Adımlar

1. **Konu Seçin:** Checkbox'lardan istediğiniz konuları işaretleyin
2. **Soru Sayısını Ayarlayın:** `+`, `-`, `+10`, `-10`, `+100` butonlarını kullanın veya sayıyı direkt yazın
3. **Çözümlü PDF:** "Çözümlü PDF de oluştur" seçeneğini işaretleyin (varsayılan açık)
4. **PDF Oluştur:** Butona basın, kayıt klasörünü seçin
5. PDF dosyaları seçtiğiniz klasöre kaydedilir

## 📚 Konu Detayları

| Konu | İçerik |
|------|--------|
| Temel İşlemler | Toplama, çıkarma, çarpma, bölme |
| Sayılar | Ardışık sayılar, toplam/fark problemleri |
| 1. Derece Denklemler | ax+b=c, ax+b=cx+d, parantezli denklemler |
| 2. Derece Denklemler | Köklerin toplamı/çarpımı, diskriminant |
| Fonksiyonlar | f(x) hesaplama, bileşke (fog/gof), ters fonksiyon |
| Mutlak Değer | |ax+b|=c, çözüm sayısı, köklerin toplamı |
| Üslü İfadeler | Üs kuralları, sadeleştirme |
| Köklü İfadeler | Karekök, sadeleştirme, işlemler |

## 📄 Çıktı Dosyaları

- `Matematik_N_Soru.pdf` – Sorular + Cevap Anahtarı
- `Matematik_N_Soru_Cozumlu.pdf` – Sorular + Adım Adım Çözümler + Cevap Anahtarı

## 🛠️ Eski Script

`generate_questions.py` – Orijinal CLI tabanlı soru üretici (800 soru, sadece denklem soruları). Geriye dönük uyumluluk için korunmuştur.

## 📝 Lisans

Eğitim amaçlı kullanım içindir.
