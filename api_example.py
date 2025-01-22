import requests
import numpy as np
import pandas as pd
from pathlib import Path
import time
import json

def test_static_clustering():
    """Test static clustering API endpoints."""
    print("\nTesting Static Clustering API...")
    
    # Model yükleme
    response = requests.post(
        "http://localhost:8000/load_model",
        json={
            "model_path": "output/models/static_cluster_model",
            "method": "static"
        }
    )
    print("Model Yükleme:", response.json())
    
    # Model bilgisi alma
    response = requests.get("http://localhost:8000/model_info")
    print("Model Bilgisi:", response.json())
    
    # Örnek veri oluştur
    n_samples = 10
    n_features = 5
    X = np.random.randn(n_samples, n_features)
    
    # Tahmin yap
    data = {
        "data": [{"features": row.tolist()} for row in X]
    }
    response = requests.post(
        "http://localhost:8000/predict",
        json=data
    )
    print("Tahmin Sonuçları:", response.json())

def test_streaming_clustering():
    """Test streaming clustering API endpoints."""
    print("\nTesting Streaming Clustering API...")
    
    # Model yükleme
    response = requests.post(
        "http://localhost:8000/load_model",
        json={
            "model_path": "output/models/streaming_cluster_model",
            "method": "streaming"
        }
    )
    print("Model Yükleme:", response.json())
    
    # Model bilgisi alma
    response = requests.get("http://localhost:8000/model_info")
    print("Model Bilgisi:", response.json())
    
    # Streaming veri simülasyonu
    for batch in range(3):
        print(f"\nBatch {batch + 1}")
        
        # Örnek veri oluştur
        n_samples = 5
        n_features = 5
        X = np.random.randn(n_samples, n_features)
        
        # Veriyi gönder ve model güncelle
        data = {
            "data": [{"features": row.tolist()} for row in X]
        }
        response = requests.post(
            "http://localhost:8000/partial_fit",
            json=data
        )
        print("Kısmi Eğitim Sonuçları:", response.json())
        
        # Tahmin yap
        response = requests.post(
            "http://localhost:8000/predict",
            json=data
        )
        print("Tahmin Sonuçları:", response.json())
        
        time.sleep(1)  # Simüle edilmiş gecikme

if __name__ == "__main__":
    print("API Test Başlıyor...")
    print("Not: API servisinin çalışır durumda olduğundan emin olun (uvicorn api_service:app --reload)")
    
    try:
        # Statik kümeleme testi
        test_static_clustering()
        
        # Streaming kümeleme testi
        test_streaming_clustering()
        
    except requests.exceptions.ConnectionError:
        print("\nHata: API servisine bağlanılamadı!")
        print("Lütfen API servisinin çalıştığından emin olun:")
        print("Terminal'de şu komutu çalıştırın: uvicorn api_service:app --reload") 