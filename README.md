# Veri Hazırlama ve Temizleme Pipeline'ı

Bu proje, veri hazırlama ve temizleme işlemlerini otomatikleştiren kapsamlı bir pipeline sunar. Temel işlevler arasında eksik değer analizi, aykırı değer tespiti, veri dönüşümleri ve görselleştirme bulunur.

## Özellikler

- Eksik değer analizi ve doldurma
- Yinelenen satırların tespiti ve kaldırılması
- Aykırı değer tespiti ve işleme (IQR ve Z-score yöntemleri)
- Normal dağılıma dönüştürme (Yeo-Johnson transformasyonu)
- Özellik ölçeklendirme (StandardScaler)
- Kategorik değişken kodlama (Label Encoding ve One-Hot Encoding)
- Dağılım görselleştirme (Histogram ve Box plot)
- Dönüştürücüleri kaydetme ve yükleme

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

### Temel Kullanım

```python
from data_preparation import DataPreparation

# Pipeline'ı başlat
prep = DataPreparation()

# Veri yükle
df = prep.load_data("veriler.csv")

# Eksik değer analizi
missing_stats = prep.analyze_missing_values(df)

# Eksik değerleri doldur
strategy = {
    'sayisal_sutun': 'mean',
    'kategorik_sutun': 'mode'
}
df_cleaned = prep.handle_missing_values(df, strategy)

# Aykırı değerleri tespit et ve işle
outliers = prep.detect_outliers(df_cleaned, ['sayisal_sutun'])
df_no_outliers = prep.handle_outliers(df_cleaned, outliers)

# Dağılımları görselleştir
prep.plot_distributions(df_no_outliers, ['sayisal_sutun'])
```

### Örnek Kullanım

Projenin nasıl kullanılacağını gösteren örnek bir script `example_usage.py` dosyasında bulunmaktadır. Bu örneği çalıştırmak için:

```bash
python example_usage.py
```

## Proje Yapısı

```
.
├── data_preparation.py   # Ana pipeline sınıfı
├── example_usage.py      # Örnek kullanım
├── requirements.txt      # Gerekli paketler
└── README.md            # Bu dosya
```

## Çıktılar

Pipeline, işlenmiş verileri ve görselleştirmeleri `output/` dizini altında saklar:

```
output/
├── plots/              # Dağılım grafikleri
└── transformers/       # Kaydedilmiş dönüştürücüler
```

## Özelleştirme

Pipeline'ı özelleştirmek için `DataPreparation` sınıfını başlatırken config parametresi kullanılabilir:

```python
config = {
    'outlier_threshold': 2.0,
    'scaling_method': 'standard'
}
prep = DataPreparation(config=config)
```

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun 