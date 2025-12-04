🚀 Kubecostiq — Kubernetes Gerçek Zamanlı Maliyet Analiz Dashboard’u
Kubecostiq, Kubernetes cluster’ındaki anlık CPU ve bellek tüketimlerini metrics-server üzerinden okuyup bunlardan gerçek zamanlı saatlik maliyet hesaplayan bir Full‑Stack observability uygulamasıdır.

Bu proje;
✔ FastAPI backend
✔ Next.js (React) frontend
✔ Recharts grafikler
✔ Gerçek zamanlı auto-refresh
✔ Dark tema modern UI

ile kullanıma hazır bir maliyet izleme çözümü sunar.

📌 Özellikler
🔹 1. Namespace Bazlı Maliyet Hesaplama
Metrics API’den alınan tüm pod’lar namespace’lere göre gruplandırılır ve:

toplam CPU çekirdek tüketimi

toplam bellek tüketimi

saatlik hesaplanan maliyet

hesaplanır ve grafikte gösterilir.

🔹 2. Pod Bazlı Detaylı Maliyet Tablosu
Her pod için:

CPU (core)

Bellek (GB)

Saatlik maliyet ($)

görüntülenir.

🔹 3. Gerçek Zamanlı Otomatik Güncelleme
Frontend verileri her 10 saniyede bir otomatik yeniler.

🔹 4. Modern Dark Mode UI
Daha okunabilir grafikler ve clean bir dashboard arayüzü.

🏗 Proje Mimarisi
kubecostiq/
│
├── backend/          # FastAPI backend
│   ├── app/
│   │   └── main.py   # Kubernetes metrics to cost conversion API
│
├── frontend/         # Next.js frontend
│   └── src/app/
│       └── dashboard/page.tsx  # Dashboard UI
│
└── README.md
⚙ Backend — FastAPI
Backend, Kubernetes'in metrics.k8s.io API’sinden veriyi okuyarak maliyet hesaplar.
Fiyatlandırma şu şekildedir:

CPU_PRICE = 0.045   # $/core-hour
MEM_PRICE = 0.005   # $/GB-hour
API Endpointleri
Endpoint	Açıklama
/pods/usage	Tüm pod'ların ham CPU/Bellek kullanım verileri
/pods/cost	Pod bazlı maliyet hesapları
/namespaces/cost	Namespace bazlı maliyet özetleri
🎨 Frontend — Next.js + Recharts
Dark theme modern UI

Responsive bar chart

Pod maliyet tablosu

API’den 10 saniyede bir veri çekme

Dashboard görünümü:

Toplam Cluster Maliyeti

Namespace bazlı maliyet grafiği

Pod maliyet tablosu

▶ Projeyi Çalıştırma
1) Backend Başlat
cd backend
uvicorn app.main:app --reload --port 8080
2) Frontend Başlat
cd frontend
npm install
npm run dev
Arayüz burada açılır:

👉 http://localhost:3000/dashboard

🔧 Gereksinimler
Kubernetes cluster (kind/minikube vb.)

metrics-server yüklü olmalı

Python 3.10+

Node.js 18+

📝 Yol Haritası (Future Work)
Bu proje geliştirilmeye devam edecek. Planlanan özellikler:

 Cluster toplam maliyetinin günlük/aylık grafiği

 Node bazlı maliyet hesaplama

 Storage maliyetleri

 Network egress maliyetleri

 Kullanıcı login sistemi

 Helm chart ile deploy

👤 Geliştirici
Halit Emir Turan
DevOps & Cloud Enthusiast

