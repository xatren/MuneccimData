from data_preparation import DataPreparation
import pandas as pd
from pathlib import Path

def main():
    # Veri hazırlama sınıfını başlat
    prep = DataPreparation()
    
    # Örnek veri yükle (bu kısımda kendi veri dosyanızın yolunu kullanın)
    try:
        df = prep.load_data("data\example.csv")
    except FileNotFoundError:
        # Örnek veri oluştur
        df = pd.DataFrame({
            'numeric_col': [1, 2, None, 4, 5, 100, 6, 7, 8, 9],
            'category_col': ['A', 'B', 'A', None, 'C', 'B', 'A', 'C', 'B', 'A'],
            'text_col': ['örnek', 'metin', None, 'veri', 'seti', 'test', 'deneme', 'python', 'veri', 'bilimi']
        })
    
    # 1. Eksik değer analizi
    missing_stats = prep.analyze_missing_values(df)
    print("\nEksik Değer Analizi:")
    print(missing_stats['missing_percentages'])
    
    # 2. Eksik değerleri doldur
    strategy = {
        'numeric_col': 'mean',
        'category_col': 'mode',
        'text_col': 'mode'
    }
    df_cleaned = prep.handle_missing_values(df, strategy)
    
    # 3. Yinelenen satırları kaldır
    df_unique = prep.remove_duplicates(df_cleaned)
    
    # 4. Aykırı değerleri tespit et ve işle
    numeric_columns = ['numeric_col']
    outliers = prep.detect_outliers(df_unique, numeric_columns, method='iqr')
    df_no_outliers = prep.handle_outliers(df_unique, outliers, method='clip')
    
    # 5. Normal dağılıma dönüştür
    df_normalized = prep.normalize_distribution(df_no_outliers, numeric_columns)
    
    # 6. Özellikleri ölçeklendir
    df_scaled = prep.scale_features(df_normalized, numeric_columns)
    
    # 7. Kategorik değişkenleri kodla
    categorical_columns = ['category_col']
    df_encoded = prep.encode_categorical(df_scaled, categorical_columns, method='onehot')
    
    # 8. Dağılımları görselleştir
    output_dir = Path("output/plots")
    prep.plot_distributions(df_encoded, numeric_columns, save_path=output_dir)
    
    # 9. Dönüştürücüleri kaydet
    prep.save_transformers("output/transformers")
    
    print("\nVeri hazırlama işlemi tamamlandı!")
    print(f"Son veri seti boyutu: {df_encoded.shape}")
    print("\nİlk birkaç satır:")
    print(df_encoded.head())

if __name__ == "__main__":
    main() 