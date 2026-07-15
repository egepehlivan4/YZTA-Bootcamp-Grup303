## Daily Scrum - 15 Temmuz 2026

| Kişi | Dün Yaptığım | Bugün Yapacağım | Blocker |
| :--- | :--- | :--- | :--- |
| **Product Owner** | Verim kaybı regresyon modeli için kullanılacak veri setini temizledim ve ön işlemeyi bitirdim. | Scikit-learn kullanarak regresyon modelinin ilk (baseline) eğitimini gerçekleştireceğim. | Yok |
| **Scrum Master** | Orkestratör ajanın Groq (Llama 3) altyapısında CNN ve LSTM modellerini tool olarak çağırabilmesi için gerekli fonksiyon iskeletini yazdım. | Hafıza mekanizmasını (geçmiş kayıtlar) ajana bağlayacağım ve bağlamsal tavsiye prompt'larını test edeceğim. | Yok |
| **Developer 1** | CNN modelinin doğruluk oranını artırmak için hiperparametre optimizasyonu (epoch/batch size) yaptım. | Modelin ensemble katmanına göndereceği API çıktısını (olasılık skoru) JSON formatında standartlaştıracağım. | Yok |
| **Developer 2** | Ensemble birleştirme mantığının ağırlıklarını (0.55 CNN, 0.45 LSTM) koda entegre ettim. | Regresyon modülü çıktısıyla ensemble skorunu bağlayan ara katmanı yazacağım. | **Var:** Dev 1'in API çıktı formatını (JSON şeması) netleştirmesini bekliyorum (Gün içinde Slack'ten çözülecek). |
| **Developer 3** | FastAPI üzerinde JWT tabanlı RBAC (Rol Bazlı Erişim Kontrolü) iskeletini kurdum ve test ettim. | Streamlit frontend'inde, backend'den dönecek risk skoru, verim kaybı ve ajan tavsiyesini gösterecek sonuç ekranını tasarlayacağım. | Yok |

**Scrum Master Notu:** Developer 2'nin belirttiği JSON şeması engeli için gün içinde Developer 1 ile kısa bir senkronizasyon görüşmesi planlanmıştır; geliştirmeyi durduracak kritik bir blocker değildir. Sprint hedeflerine uygun şekilde ilerliyoruz.