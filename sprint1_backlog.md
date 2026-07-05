# Sprint 1 — Backlog Dağıtma Mantığı ve Board Durumu

**Sprint Aralığı:** 19 Haziran – 5 Temmuz 2026
**Sprint Hedefi:** Mimarinin iskeletini kurmak; CNN ve LSTM için çalışan birer prototip üretmek; proje yönetim altyapısını (GitHub, Board, README) işler hale getirmek.

---

## Backlog Dağıtma Mantığı

Sprint 1 backlog'u oluşturulurken şu önceliklendirme mantığı izlenmiştir: Değerlendirme kriterlerinde en yüksek ağırlık **Yapay Zeka Öğeleri (35 puan)** ve **AI Agent orkestrasyonu (15 puan)** başlıklarında olduğundan, ilk sprint'te tüm teknik riskin erken görülmesi hedeflendi. Bu nedenle iki model prototipinin (CNN ve LSTM) "mükemmel değil ama çalışır" seviyede ayağa kaldırılması, arayüz cilalamasından önce öne alındı. Proje yönetimi puanı sprint bazında değerlendirildiği için repo, README ve board kurulumu sprint'in ilk günlerine yerleştirildi. Story başına tahmin puanları, ekip üyelerinin bootcamp dışı ders/iş yükleri göz önüne alınarak muhafazakâr tutuldu.

> ⚠️ **Durum notu (dürüst kayıt):** Sprint'in son bölümünde takım içi iletişimde kopukluk yaşanmış, bazı story'ler planlandığı gibi paralel ilerletilememiştir. Aşağıdaki board durumu **gerçek durumu** yansıtmaktadır; tamamlanamayan işler Sprint 2 backlog'una devredilecektir. Bu durum Retrospective'de ele alınmıştır.

---

## Board Durumu (Sprint 1 Sonu)

### ✅ Done

- [JS-01] GitHub reposunun oluşturulması, public yapılması ve branch stratejisinin belirlenmesi (`main` + feature branch)
- [JS-02] README: ürün fikri, takım rolleri (taslak), ürün özellikleri ve hedef kitlenin belgelenmesi
- [JS-03] Backend API iskeleti (FastAPI) — temel endpoint yapısı
- [JS-04] Frontend iskeleti (Streamlit) — fotoğraf yükleme ekranı
- [JS-05] CNN ve LSTM prototip mimarilerinin kodlanması (dummy veri ile ileri besleme doğrulandı)

### 🔄 In Progress

- [JS-06] Yaprak görüntü veri setinin belirlenmesi ve ön işleme pipeline'ı
- [JS-07] Hava durumu / nem / sıcaklık verisi için kaynak (API veya açık veri seti) araştırması

### 📋 To Do (Sprint 2'ye devrediliyor)

- [JS-08] CNN modelinin gerçek veri setiyle ilk (baseline) eğitimi
- [JS-09] LSTM modelinin gerçek zaman serisiyle ilk (baseline) eğitimi
- [JS-10] Geçmiş hastalık kayıtları için veri şeması (agent hafızasının temeli)
- [JS-11] Sprint Board'un (Trello/Miro) tüm ekiple senkronize edilmesi

---

## Story Tahmin Notu

Tahminler Planning Poker yerine (ekip senkron toplanamadığından) T-shirt sizing (S/M/L) ile yapılmış, S=1-2 saat, M=yarım gün, L=1+ gün olarak kabul edilmiştir. JS-01…05: S-M; JS-06…09: L.
