# Gelişmiş Veri Hazırlama ve Kümeleme Pipeline'ı

Bu proje, veri hazırlama, kümeleme optimizasyonu ve gerçek zamanlı kümeleme analizi için kapsamlı bir çözüm sunar. Sistem, hem statik veri kümeleri hem de streaming veri akışları için optimize edilmiş algoritmalar içerir.

## 🔬 Bilimsel Altyapı

### 1. Veri Hazırlama ve Ön İşleme

#### 1.1 Eksik Veri Analizi
- **Matematiksel Temel**: Eksik veri oranı (ρ) hesaplaması:
  ```
  ρ = (n_missing / n_total) × 100
  ```
- **Doldurma Stratejileri**:
  - Sayısal değişkenler için: μ (ortalama), η (medyan)
  - Kategorik değişkenler için: mod (en sık değer)

#### 1.2 Aykırı Değer Tespiti
- **IQR (Interquartile Range) Yöntemi**:
  ```
  IQR = Q3 - Q1
  alt_sınır = Q1 - k × IQR
  üst_sınır = Q3 + k × IQR
  ```
  Burada k genellikle 1.5 olarak alınır.

- **Z-Score Yöntemi**:
  ```
  z = (x - μ) / σ
  ```
  |z| > threshold olan değerler aykırı kabul edilir.

#### 1.3 Dağılım Normalizasyonu
- **Yeo-Johnson Transformasyonu**:
  ```
  f(x;λ) = {
    ((x + 1)^λ - 1) / λ,     x ≥ 0, λ ≠ 0
    ln(x + 1),               x ≥ 0, λ = 0
    -((-x + 1)^(2-λ) - 1) / (2-λ), x < 0, λ ≠ 2
    -ln(-x + 1),            x < 0, λ = 2
  }
  ```

### 2. Kümeleme Algoritmaları ve Optimizasyon

#### 2.1 K-Means Kümeleme
- **Matematiksel Formülasyon**:
  ```
  minimize Σ Σ ||x_i - μ_k||²
  ```
  Burada x_i veri noktaları, μ_k küme merkezleridir.

- **Optimizasyon Metrikleri**:
  - Silhouette Skoru (S):
    ```
    s(i) = (b(i) - a(i)) / max{a(i), b(i)}
    ```
    Burada a(i) iç-küme mesafesi, b(i) en yakın komşu kümeye olan mesafedir.
  
  - Calinski-Harabasz Indeksi:
    ```
    CH = [tr(B_k)/(k-1)] / [tr(W_k)/(n-k)]
    ```
    B_k: kümeler arası kovaryans matrisi
    W_k: küme içi kovaryans matrisi

#### 2.2 DBSCAN (Density-Based Spatial Clustering)
- **Parametre Optimizasyonu**:
  - ε (epsilon): Komşuluk yarıçapı
  - MinPts: Minimum nokta sayısı
  ```
  core_point := |N_ε(p)| ≥ MinPts
  ```

#### 2.3 Hiyerarşik Kümeleme
- **Bağlantı Kriterleri**:
  - Ward Minimum Varyans:
    ```
    d(u,v) = √[(|v|+|s|)/(|v|+|s|+|t|) × d²(v,s) + 
              (|v|+|t|)/(|v|+|s|+|t|) × d²(v,t) -
              |v|/(|v|+|s|+|t|) × d²(s,t)]
    ```

### 3. Gerçek Zamanlı Kümeleme (Streaming)

#### 3.1 Mini-Batch K-Means
- **Güncelleme Formülü**:
  ```
  c_t = c_{t-1} × (1 - 1/n_t) + x_t × (1/n_t)
  ```
  Burada c_t merkez güncellemesi, n_t atama sayısıdır.

#### 3.2 Incremental Learning
- **Online PCA**:
  ```
  Σ_t = (1 - α)Σ_{t-1} + αx_tx_t^T
  ```
  α öğrenme oranıdır.

## 🛠 Teknik Özellikler

### API Endpoints

#### 1. Model Yönetimi
- `POST /load_model`: Model yükleme
  ```json
  {
    "model_path": "string",
    "method": "static|streaming"
  }
  ```

#### 2. Tahmin ve Güncelleme
- `POST /predict`: Küme tahminleri
- `POST /partial_fit`: Streaming model güncelleme

### Veri Formatları

#### 1. Giriş Verisi
```json
{
  "data": [
    {"features": [float, ...]}
  ]
}
```

#### 2. Çıkış Formatı
```json
{
  "labels": [int, ...],
  "metrics": {
    "cluster_distribution": [int, ...],
    "total_samples": int
  }
}
```

## 📊 Performans Metrikleri

### 1. Kümeleme Kalitesi
- Silhouette Skoru: [-1, 1]
- Calinski-Harabasz Indeksi: [0, ∞)
- Davies-Bouldin Indeksi: [0, ∞)

### 2. Hesaplama Karmaşıklığı
- K-Means: O(kndi)
  - k: küme sayısı
  - n: örnek sayısı
  - d: boyut
  - i: iterasyon sayısı
- DBSCAN: O(n log n)
- Hiyerarşik: O(n²)

## 🚀 Kurulum ve Kullanım

### 1. Gereksinimler
```bash
pip install -r requirements.txt
```

### 2. Örnek Kullanım
```python
from data_preparation import DataPreparation
from clustering import ClusteringOptimizer

# Veri hazırlama
prep = DataPreparation()
df = prep.load_data("data.csv")
df_processed = prep.handle_missing_values(df, strategy={'numeric': 'mean'})

# Kümeleme optimizasyonu
optimizer = ClusteringOptimizer()
results = optimizer.find_optimal_kmeans(X, k_range=range(2, 11))
```

### 3. API Servisi
```bash
uvicorn api_service:app --reload
```

## 📚 Referanslar

1. Ester, M., et al. (1996). "A Density-Based Algorithm for Discovering Clusters"
2. Lloyd, S. (1982). "Least squares quantization in PCM"
3. Ward Jr, J. H. (1963). "Hierarchical Grouping to Optimize an Objective Function"
4. Yeo, I. K., & Johnson, R. A. (2000). "A New Family of Power Transformations to Improve Normality"

## 🤝 Katkıda Bulunma

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 