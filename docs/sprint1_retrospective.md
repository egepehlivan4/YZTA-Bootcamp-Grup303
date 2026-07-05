# Sprint 1 Review & Retrospective

**Tarih:** 5 Temmuz 2026
**Katılım:** Ege Pehlivan (diğer üyelere ulaşılamadı — durum akademi ekibine bildirildi)

---

## Sprint 1 Review

**Sprint Hedefi:** Mimari iskelet + model prototipleri + proje yönetim altyapısı.
**Durum:** Kısmen tamamlandı.

**Tamamlanan Story'ler:**
- GitHub repo, branch stratejisi ve README (JS-01, JS-02)
- FastAPI backend iskeleti — sağlık kontrolü, tahmin ve geçmiş endpoint'leri (JS-03)
- Streamlit frontend iskeleti — fotoğraf yükleme ve önizleme ekranı (JS-04)
- CNN ve LSTM prototip mimarileri; dummy veri ile ileri besleme (forward pass) doğrulandı (JS-05)

**Tamamlanamayanlar ve nedeni:**
- Gerçek veri setiyle baseline eğitimler (JS-08, JS-09) — veri seti seçimi ve ekip içi iş bölümü, iletişim kopukluğu nedeniyle tamamlanamadı. Sprint 2'ye devredildi.

**Demo Notları:**
- `uvicorn src.main:app` ile API ayağa kalkıyor, `/health` ve `/predict` (stub) yanıt veriyor.
- `streamlit run src/app.py` ile fotoğraf yükleme ekranı çalışıyor; yüklenen görsel önizleniyor.
- `python src/model_prototypes.py` çalıştırıldığında her iki model dummy girdilerle çıktı üretiyor.

---

## Sprint 1 Retrospective

| İyi Gitti | Zorlandık | Deneyeceğiz |
|---|---|---|
| Teknik iskelet (API + UI + model prototipleri) tek seferde, temiz klasör yapısıyla kuruldu. | **Takım iletişimi:** Sprint'in son bölümünde üyelerin çoğuna ulaşılamadı; asenkron Daily Scrum düzeni oturmadı. | Sprint 2 başında zorunlu bir senkron "yeniden başlatma" toplantısı; herkesin uygunluk takvimini paylaşması. |
| Master plan dokümanı önceliklendirmeyi kolaylaştırdı; puan ağırlıklı story seçimi işe yaradı. | **Zaman yönetimi:** İş yükü sprint sonuna yığıldı; story'ler erken bölünmediği için paralelleşemedi. | Story'leri sprint'in ilk 2 gününde kişilere atamak; "2 gün üst üste güncelleme yoksa SM devralır/yeniden atar" kuralı. |
| Blocker'ın (ulaşılamayan ekip) resmi kanala bildirilmesi — kılavuzdaki prosedür izlendi. | Board (Trello/Miro) ekiple senkronize kurulamadı. | Board'u Sprint 2'nin 1. günü kurup linkini README'ye sabitlemek; Daily Scrum'ı boardla eşleştirmek. |

**Aksiyon Maddesi (Sprint 2'ye taşınan):** Sprint 2'nin ilk 48 saati içinde tüm üyelerle senkron bir toplantı yapılacak; katılamayan üyeler için akademi ekibiyle (kılavuzdaki "takımda kalan kişilerle devam" prosedürü kapsamında) resmi süreç netleştirilecek. Sorumlu: Ege (SM).
