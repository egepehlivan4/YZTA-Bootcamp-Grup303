# Sprint 2: Entegrasyon ve Zeka Backlog Raporu

**Sprint Süresi:** 6 Temmuz - 19 Temmuz 2026  
**Sprint Hedefi:** CNN ve LSTM modellerinin çıktılarını ensemble katmanında birleştirmek, Orkestratör Ajanı tool-calling ve hafıza mekanizmasıyla tam işler hale getirmek ve regresyon modülünü sisteme entegre etmek.

## 1. Backlog Listesi ve Görev Dağılımı

| Epic Numarası ve Adı | Story (Görev) | Sorumlu | Tahmini Efor (Story Point) |
| :--- | :--- | :--- | :--- |
| **Epic 5: Ensemble ve Regresyon** | CNN ve LSTM çıktılarını birleştiren ensemble katmanının yazılması | Developer 2 | 5 |
| **Epic 5: Ensemble ve Regresyon** | Verim kaybı regresyon modelinin eğitilmesi ve ensemble skoruna bağlanması | Product Owner | 5 |
| **Epic 6: Agent Orkestrasyonu** | Orkestratör ajanın CNN/LSTM/regresyon modüllerini tool olarak çağırabilmesi | Scrum Master | 8 |
| **Epic 6: Agent Orkestrasyonu** | Hafıza mekanizmasının (çiftçi geçmişi) agent'a bağlanması | Scrum Master | 5 |
| **Epic 6: Agent Orkestrasyonu** | Agent'ın bağlamsallaştırılmış tavsiye metni üretmesi | Scrum Master | 3 |
| **Epic 7: Backend/Frontend Entegrasyonu** | Backend API'nin agent ile uçtan uca bağlanması | Developer 3 | 5 |
| **Epic 7: Backend/Frontend Entegrasyonu** | Frontend'de sonuç ekranının (risk skoru, verim kaybı, tavsiye) tasarlanması | Developer 3 | 3 |
| **Epic 8: Güvenlik Temeli** | RBAC iskeletinin (rol tanımları, yetkilendirme middleware) yazılması | Developer 3 | 5 |
| **(Model İyileştirme)** | CNN modeli iyileştirme ve ensemble'a bağlanacak API çıktısının hazırlanması | Developer 1 | 5 |

## 2. Backlog Dağıtma ve Efor Tahmini Mantığı

Jüri değerlendirme kriterlerine istinaden Sprint 2 iş dağılımımız şu prensiplere göre yapılmıştır:

* **Teknik Odaklı Rol Dağılımı:** Ekip üyelerinin Sprint 1'deki uzmanlaşma alanları Sprint 2'de korunmuştur. Görüntü işleme tarafında çalışan Developer 1 model iyileştirmelerine odaklanırken, zaman serisi uzmanımız (Developer 2) iki modelin birleşim noktası olan Ensemble katmanını üstlenmiştir.
* **Orkestrasyon ve Liderlik:** Scrum Master, sürecin orkestrasyonunu sağlarken aynı zamanda sistemin "beyni" olan yapay zeka ajanı (Orkestratör) tarafındaki geliştirmeleri üstlenmiştir. Product Owner ise veri yönetimi yetkinliğini kullanarak regresyon modülünün inşasını ve entegrasyonunu sağlamaktadır.
* **Tam Yığın (Full-Stack) Entegrasyonu:** Backend ve UI tarafındaki veri akışının kopmaması adına API bağlantıları, yetkilendirme (RBAC) iskeleti ve sonuç ekranı arayüz tasarımı doğrudan Developer 3'ün sorumluluğuna verilmiştir.
* **Efor Tahmini (Story Points):** Puanlama Fibonacci dizisi (1, 2, 3, 5, 8, 13) kullanılarak yapılmıştır. Tool-calling entegrasyonu (8 puan) en yüksek eforu gerektiren karmaşık iş olarak belirlenirken, UI tasarımları ve prompt/metin üretim işleri (3 puan) daha düşük eforlu olarak planlanmıştır. Hiyerarşik olmayan yapımız gereği, herkes geliştirme sürecine aktif bir biçimde katılmaktadır.