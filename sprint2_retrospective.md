## Sprint 2 Review

**Tamamlanan Story'ler:**
* CNN ve LSTM modellerinin çıktılarını birleştiren ensemble katmanı yazıldı ve test edildi.
* Verim kaybı regresyon modülü eğitilerek ensemble skoruna başarıyla bağlandı.
* Orkestratör Ajan (Groq altyapısı ile), tahmin modellerini ve regresyonu "tool" olarak çağırabilir hale getirildi.
* Çiftçi hafızası (geçmiş hastalık kayıtları) ajana entegre edildi ve LLM üzerinden bağlamsal tavsiye metni üretimi sağlandı.
* FastAPI backend'i ile ajan uçtan uca bağlandı; JWT tabanlı RBAC (Rol Bazlı Erişim Kontrolü) yetkilendirmesi uygulandı.
* Streamlit frontend'inde risk skoru, verim kaybı ve ajan tavsiyesini içeren sonuç ekranı tasarlandı.

**Demo Notları:**
Sistem uçtan uca çalışır durumda. Arayüze yüklenen bir fotoğraf ve konum bilgisi, orkestratör ajan tarafından yakalanıp hem görüntü hem de zaman serisi modellerine (paralel olarak) iletiliyor. Dönüşte alınan % risk skoru ve rekolte kaybı tahmini, çiftçinin hafızasıyla harmanlanarak önleyici bir karar destek metnine (örn: "Geçen ayki durumunuza benzer bir risk var, sulamayı azaltın") dönüşüyor. Jüri puanlama listesindeki "Agent kullanımı, hafıza ve orkestrasyon" adımı başarıyla kanıtlandı.

---

## Sprint 2 Retrospective

| İyi Gitti | Zorlandık | Deneyeceğiz |
| :--- | :--- | :--- |
| Orkestratör Ajanın modelleri birer "araç" (tool-calling) olarak tetikleme mantığı çok temiz ve hızlı çalıştı. | Görüntü (CNN) ve zaman serisi (LSTM) modellerinin çıktı formatları birleşirken JSON şemalarında tip uyuşmazlıkları (type mismatch) yaşadık. | API endpoint'lerinin kabul edeceği ve döneceği veri tiplerini, kodlamaya başlamadan önce Pydantic şemaları ile çok daha katı bir şekilde sabitleyeceğiz. |
| Slack üzerinden yürüttüğümüz asenkron Daily Scrum'lar sayesinde blocker'ları 24 saat geçmeden çözebildik. | LLM'in (Groq/Llama 3) tavsiye metnini üretirken zaman zaman istediğimiz formatın dışına çıkıp gereksiz uzatması prompt optimizasyonu gerektirdi. | Sprint 3'te Deployment (Canlıya Alma) sırasında oluşabilecek çevre değişkeni (.env) sorunlarını önlemek için lokalde Docker container simülasyonu yapacağız. |
| FastAPI üzerindeki JWT rol kontrolü (RBAC) beklediğimizden daha sorunsuz entegre oldu. | Backend ve UI tarafını eşzamanlı geliştirirken Streamlit'in API'den dönen yanıtı bekleme (loading) süreçlerini yönetmek biraz oyaladı. | Pull Request (PR) süreçlerinde takım arkadaşlarımızın kodlarını gözden geçirirken (review) DRY (Don't Repeat Yourself) prensibine daha fazla dikkat edeceğiz. |

**Aksiyon Maddesi:**
Sprint 3'ün ilk günü, UI ve Backend arasındaki tüm veri iletişim formatlarını (JSON Data Contracts) net olarak dökümante edip sabitleyeceğiz ve canlı ortam (deployment) kurulum adımlarına erkenden başlayacağız.