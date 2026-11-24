# Performans önce/sonra — 24 Kasım 2026

## Sonuç ve ölçüm sınırı

3B kalp ve hero için yerel düzeltmeler uygulandı; sayısal üretim hız artışı
bu dosyada henüz ilan edilmiyor. **Lighthouse puanı/TBT/INP ve saha CWV p75
sonucu yoktur.** Root tarafından çalıştırılan gerçek CDP koşuları varsa
ham çıktısı ve örneklem koşulları ayrıca aşağıdaki ölçüm kayıtlarına eklenir.
Hazırlanmış bir collector veya başarılı build, browser koşusu değildir.

## Başlangıç snapshot'ı

`evidence/baseline-build.json`: minify production, Hugo0.167.0,
exit0,976HTML; ayrı destination/resource/cache ve --noBuildLock.
Değişiklik öncesi root ağacının kimliği baseline manifestinde.
Ana sayfa101605bayt/SHA5443e2b1e1d457569a8dac8ab4b21df104705dbd1bfe8f3484aee8387539b5a8;
1314HTTP gövdesiyle aynı anlık kimlik karşılaştırıldı. Fiziksel telefon veya
canlı origin olarak değerlendirilmez. Yerel ağ RTT/TTFB sonuçları canlı
sunucunun DNS/TLS/CDN koşullarını temsil etmez.

## Gerçek yapılan uygulama

| Alan | Önce | Sonra / kabul sınırı |
| --- | --- | --- |
| 3B yükleme | Observer100px rootMargin + idle timeout2000; desktop eski kayıtta3/3scrollöncesi1.51MBGLB | Anatomik poster + gerçek Load düğmesi; click öncesi modül/CDN/GLB çağrısı yok (kaynak/Node bootstrap). Gerçek ağ kaydı ayrıca gerekir. |
| Model | Aktif1.511.228bayt GLB; eski ayrı shortcode3.255.284bayt yol | Aktif model/kalite korunur; eski bozuk ikinci uygulama aynı partial'a konsolide |
| Render | Sekme gizliyken durma; viewport dışı kapı yok | Tek cancellableRAF; viewport+sekme görünürlük kapısı; re-entry; Node lifecycle testli, GPU frame trace henüz yok |
| Hareket/veri | Reduced-motion yorumu gerçek kontrolle karşılanmıyor | Reduced-motion initial static/on-demand; Pause/Start; tüm bağlantılarda kullanıcı isteği. Save-Data network profili ayrıca test ister |
| Hata | CDN/GLTF hata sonrası kalp simgesi; açık loop kalabiliyor | Gerçek poster + Retry; cleanup/generation guard; WebGL bulunmaması Node stub testiyle doğrulandı, gerçek browser hata senaryosu ayrı |
| Hero | Eager tek kaynak; width/height/srcset/sizes/fetchpriority yok | Eager/intrinsic/responsive/highpriority. Gerçek production LCP öğesi/alt süreleri ve CLS karşılaştırması ayrıca gerekir |
| Vendor/arama | Sync vendor ve büyük ilk arama index'i aday | Ölçülmeden yeni worker/defer dönüşümü yapılmadı; root/SEO/UI değişiklikleri final envanterde ayrı görülebilir |

Ayrıntılı kaynak ve test kaydı:
[evidence/performance-implementation-notes.md](evidence/performance-implementation-notes.md).

## Çalıştırma kayıtları

| Kontrol | Durum / ham kanıt |
| --- | --- |
| Kaynak JS syntax | PASS: node --check assets/js/heart-viewer.js |
| Tek-loop/visibility/motion/dispose/başlangıç/hata/retry | 9PASS; evidence/heart-viewer-node-tests.json — Node/DOM-stub, browser değil |
| Baseline dosya envanteri | Çalıştırıldı; evidence/performance-before-after-assets.json |
| After dosya envanteri | AynıJSONafter alanı: final build verilene kadar null; aşağıdaki komutla tamamlanır |
| Desktop/mobile aynı koşullu≥3cold, sabit12sCDP | Bu alt ajan tarafından NOT_RUN; CUAjs expose edilmedi. Root ham kayıtları varsa bu satır yerine gerçek kayıt eklenir |
| Sıcak tekrar ziyaret | NOT_RUN / root kaydı varsa ayrı profil |
| Lighthouse JSON/HTML/puan | NOT_RUN; PATH'te CLI yok |
| Model tam/engelli kontrollüA/B ve CPU/GPUatfı | NOT_RUN; source değişikliğinden puan/long-task nedeni çıkarılmadı |
| CrUX/GSC/PSI/RUM cihazp75 | Doğrulanamadı; yetkili saha verisi alınmadı |
| Gerçek browser reduced-motion/Save-Data/CDN/WebGL/ikiinstance | NOT_RUN; Node gerçek browserın yerine geçmez |

After varlık envanteri için:

```sh
python3 docs/implementation/seo-remediation/2026-11-24/evidence/performance-implementation-collect.py \
  --before BASELINE_PUBLIC_ROOT --after FINAL_PUBLIC_ROOT \
  --output docs/implementation/seo-remediation/2026-11-24/evidence/performance-before-after-assets.json
```

Dosya baytı HTTP transfer boyutu değildir; gzip/Brotli/cache etkisi gerçek
başlık/yanıt olmadan başarı sayılmaz. Lab kontrolünü sourceharita/DOMcount
ile sınırlama; root izinli browserı kullanabildiğinde LCP öğesi/alt süreleri,
CLS kaynakları, script/task/DOM maliyeti ve ağ isteklerini kaydetsin.

## Saha hedefi ve takip

Güncel web.dev rehberindeki saha hedefleri cihaz grubu p75 için LCP≤2.5s,
INP≤200ms,CLS≤0.1. CDP/lab medyanı saha p75 değildir; long-task toplamı
TBT/INP değildir. Sayısal önce/sonra iddiası ancak aynı URLşablonu, aynı
viewport/DPR/cache/CPU/ağ/sampling penceresi ve kıyaslanabilir production
build kimliğiyle yapılabilir. Dev1313 ile frozen production1314 karşılaştırması
üretim önce/sonra benchmark olarak sunulamaz.

Birincil kaynaklar (2026-11-24'te açıldı):
https://web.dev/articles/vitals ve
https://web.dev/articles/browser-level-image-lazy-loading.

## Root nihai paket notu

Yeni ayrı minify release exit0; nihai varlık karşılaştırması performance-before-after-assets.json içindedir. Runtime süreleri null'dır. CUA1314fetch101605bayt SHA5443e2…9b5a8 frozen baseline ile eş; bu bir hız koşusu değildir. Ölçüm kurulum çağrısı kernel reset nedeniyle çalışmadı, ardından bağlantı timeout oldu. Yeni üretim server1315 bind Operation not permitted; kısıt aşılmadı. Yeni CPU/network/viewport ölçüm profili uygulanmadı. Üretim3+3cold/warm,Lighthouse,trace,A-B,GPU ve gerçek native200 sonuçları NOT_RUN kalır. Kullanıcı isteğinden önce import/model başlamaması kaynak/Node-startup testidir; gerçek after network waterfall sonucu değildir.

Son native Chrome denemesinde `localhost:1313` ERR_CONNECTION_REFUSED verdi; dolayısıyla native%200 ve after görsel/performans kabulü yapılamadı. Önceki kullanıcı penceresi korunarak test penceresi kapatıldı. Kanıt browser-native-attempt.json.
