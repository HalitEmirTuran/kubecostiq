# 🚀 Kubecostiq Kubernetes Gerçek Zamanlı Maliyet Analiz Dashboard’u!!!!

**Kubecostiq**, Kubernetes cluster’ındaki anlık CPU ve bellek kullanımını  
`metrics-server` üzerinden okuyup gerçek zamanlı saatlik maliyet hesaplayan  
modern bir **Full‑Stack Observability** uygulamasıdır.

Bu proje aşağıdaki teknolojilerle geliştirilmiştir:

- ⚡ FastAPI (Backend)
- ⚛️ Next.js / React (Frontend)
- 📊 Recharts (Grafikler)
- 🌙 Dark Theme UI
- 🔄 Gerçek zamanlı otomatik veri yenileme

---

## 📌 Özellikler

### 🔹 1. Namespace Bazlı Maliyet Hesaplama
Metrics API’den alınan pod verileri namespace’lere göre gruplanır ve:

- Toplam CPU çekirdek tüketimi  
- Toplam bellek tüketimi  
- Hesaplanan saatlik maliyet  

otomatik olarak hesaplanarak grafikte gösterilir.

---

### 🔹 2. Pod Bazlı Detaylı Maliyet Tablosu
Her pod için:

- CPU (cores)  
- Bellek (GB)  
- Saatlik maliyet ($)

şeffaf şekilde listelenir.

---

### 🔹 3. Gerçek Zamanlı Otomatik Güncelleme
Frontend, API verilerini **her 10 saniyede bir** yeniler.

---

### 🔹 4. Modern Dark Mode UI
Grafikler daha okunabilir, arayüz modern ve sade olacak şekilde tasarlanmıştır.

---

## ⚙ Backend — FastAPI

Backend, Kubernetes’in `metrics.k8s.io` API’sini kullanarak tüm pod’ların  
CPU ve bellek tüketimlerini toplar ve bunları maliyete çevirir.

### 💵 Fiyatlandırma Modeli

```python
CPU_PRICE = 0.045      # $ / core-hour
MEM_PRICE = 0.005      # $ / GB-hour
📡 API Endpointleri
Endpoint	Açıklama
/pods/usage	Pod’ların ham CPU/Bellek kullanım verileri
/pods/cost	Pod bazlı maliyet hesapları
/namespaces/cost	Namespace bazlı maliyet özetleri

🎨 Frontend — Next.js + Recharts
Modern dark theme

Responsive bar chart

Pod maliyet tablosu

API’den 10 saniyede bir veri yenileme

Temiz dashboard görünümü

Dashboard’da gösterilenler:

Toplam cluster maliyeti

Namespace bazlı maliyet grafiği

Pod bazlı maliyet tablosu

▶ Projeyi Çalıştırma
Backend
bash
Kodu kopyala
cd backend
uvicorn app.main:app --reload --port 8080
Frontend
bash
Kodu kopyala
cd frontend
npm install
npm run dev
Arayüz:
👉 http://localhost:3000/dashboard

🔧 Gereksinimler
Kubernetes cluster (kind / minikube / k3d vb.)

metrics-server kurulu olmalı

Python 3.10+

Node.js 18+

📝 Yol Haritası (Future Work)
Günlük / Aylık cluster maliyet grafikleri

Node bazlı maliyet hesaplama

Storage maliyetleri

Network egress maliyetleri

Auth / Login sistemi

Helm chart ile deploy

Trend analizi grafikleri

👤 Geliştirici
Halit Emir Turan
DevOps & Cloud Enthusiast
