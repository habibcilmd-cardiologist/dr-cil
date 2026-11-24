# Kanıtların zamanı ve yeniden üretim

24 Kasım 2026. Yalnız denetim raporları/yardımcıları yazıldı. Mevcut
Hugo süreci durdurulmadı; DNS/Netlify/GSC/GBP ve üretim değiştirilmedi.
Kaynak hash karşılaştırması `recheck-worktree-state.json`; kapanış kontrolü
`recheck-final-validation.json` içindedir. Başlangıç commit'i `2fad17e0`,
çalışma sırasında dışarıdan görülen HEAD `b2944ac5` olarak ayrılmıştır.
Denetim git commit/add/push komutu çalıştırmadı. Başlangıç kaynakları ve
tema aynı kaldı; eşzamanlı dış rapor/commit işlemi sahiplenilmedi.

## Kanıt zinciri

| Kayıt | Kaynak ve gerçek kapsam |
| --- | --- |
| `initial-worktree-state.json`, `production-build.log`, `static-*`, `schema-*`, `content-*` | Başlangıçta mevcut önceki aynı gün denetimi. Kaynakla karşılaştırılarak tekrar okundu; yeni çalıştırma diye sayılmadı. |
| `browser-layout-observations.json`, `browser-keyboard-observations.json`, `browser-dev-diagnostics.json`, `browser-model-observations.json`, `browser-validator-results.json`, `browser-public-dns.json` | Önceki runtime/validator/DNS gözlemleri. DEV ve kod testinin kapsamı dosyalarında açık. Yeni performans benchmark yerine kullanılamaz. |
| `browser-menu-1280-crop.jpg` | Saklanmış gerçek 1280px menü kırpımı. Diğer viewport/hero/AR/zoom için yeni kalıcı screenshot bu tur üretilmedi. |
| `recheck-schema-output.json`, `recheck-content-*`, `recheck-perf-*` | Bu tur bağımsız salt okunur tekrar taramaları ve resmî kaynak kontrolleri; önceki kanıtların üstüne yazılmadı. |
| `recheck-production-build.json`, `.log` | Bu tur yeni, izole, minify production build exit0; tam args/env ve hedef klasör kaydedildi. |
| `recheck-build-comparison.json` | Eski/yeni 976 HTML SHA-256 karşılaştırması: fark0. Bu, mevcut eski çıktı analizlerinin yeni build için de geçerli olduğunu kanıtlar; canlı siteyle eşitlik değildir. |
| `recheck-production-static/`, `.log` | Yeni build'in tamamında statik tarama tekrar çalıştı, exit0. Ham eksik link98; /tr kuralı sonrası çözülemeyen66. Ham/triage sayıları ayrı tutulur. |
| `recheck-404.json` | Yeni production çıktısının üç gerçek 404 dosyasında main başlık/çıkışlar; HTTP durum testi değil. |
| `recheck-runtime-limitations.json` | Bu tur iki CUA bağlantı timeout'u, yeni runtime0, yeni site DNS yanıtı alınamaması. Hata mesajı site DNS cevabı değildir. |

Yardımcıların yaptığı kontroller tam bir HTML, güvenlik, Schema.org reasoner,
Google indeks veya klinik doğruluk garantisi vermez. `scripts/check_schema.py`
üretim grafiğinin tamamı ve güncel sözlük yerine geçmez; kapsamı schema
raporunda incelenmiştir.

## Güvenli ayrı build ve tarama

Yeni build için gerçekten çalıştırılan argümanlar/env
`recheck-production-build.json` içindedir. Yol geçici olduğundan ileride yok
olursa **yeni boş bir geçici klasör** kullanın. Mevcut public/resources'u
hedef göstermeyin. Aynı örüntü:

```sh
audit_tmp=$(mktemp -d -t dr-cil-audit)
HUGO_RESOURCEDIR="$audit_tmp/resources" \
HUGO_CACHEDIR="$audit_tmp/cache" \
hugo --environment production --minify --noBuildLock \
  --destination "$audit_tmp/public" --cacheDir "$audit_tmp/cache"
python3 docs/audit/results/2026-11-24/evidence/static-audit.py \
  "$audit_tmp/public" "$audit_tmp/static-check"
python3 docs/audit/results/2026-11-24/evidence/schema-audit.py \
  "$audit_tmp/public" "$audit_tmp/schema-check"
python3 docs/audit/results/2026-11-24/evidence/recheck-content-check.py \
  --build-root "$audit_tmp/public"
```

Son içerik komutu yalnız denetim `recheck-content-evidence.json` yardımcısını
yeniler; önceki ham kanıt dosyalarına yazmaz. `recheck-schema.py` eski build
klasörünü sabit okur; yeniden build başka yoldaysa bu yardımcı yerine
argümanlı `schema-audit.py` kullanın. Test komutları HTTP/POST isteği göndermez.
`--gc`, `--cleanDestinationDir`, mevcut server restart veya deploy yoktur.

## Runtime paketini tamamlamak

Bir kez, erişilebilir ayrı production test sunucusu ve çalışan tarayıcı
bağlantısı sağlandığında `08-test-coverage.md` içindeki NOT_RUN paketini
uygulayın. Kullanıcının 1313 sunucusuna dokunmayın. Yeni port/sunucu kısıtı
varsa aşmayın. Üretim ≥3+3 cold koşu, aynı profil/sampling penceresi,
sıcak ziyaret ayrı, model açık/engelli ve offscreen/hidden izleri saklanır.
Breakpoint 852/853/854, bütün istenen genişlikler, native %200 zoom ve
üç dil şablonları ekran görüntüsü/computed style ile kaydedilir. OS/DNS/TLS
cache sıfırlanmıyorsa bunu raporlayın. TBT, INP veya saha p75 yerine geçmez.

DNS için önceki dosyanın tam sorgularını tekrar çalıştırıp gerçek response
JSON saklayın; ikinci bağımsız resolver ve doğrudan authoritative cevap
ekleyin. TLS/HTTP/404/redirect/headers/compression ayrı test edilir. Form ve
randevu/mesaj gönderimi bu denetimde yapılmadı.

## Bu tur açılan ortak birincil kaynaklar

- [Hugo komutu ve bayrakları](https://gohugo.io/commands/hugo/): destination,
  cacheDir, noBuildLock, minify; bu komutların etkisi kaydedilmiş build ile ayrıldı.
- [Google DNS JSON API](https://developers.google.com/speed/public-dns/docs/doh/json):
  name/type/Status/Answer alanları; tool error DNS yanıtı değildir.
- [W3C Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html):
  320 CSS px reflow ile native %200 testi ve tam WCAG uygunluğu aynı iddia değil.
- [Google değişiklik kaydı](https://developers.google.com/search/updates):
  FAQ gösteriminin 7 Mayıs 2026'da kaldırılması, 8 Mayıs kaydı;
  görünür SSS'nin yararlılığı ayrı değerlendirilir.

Schema/performans/içerik/SEO alanlarının diğer güncel birincil kaynakları
`recheck-schema-official-sources.json`, `recheck-perf-official-sources.json`,
`recheck-content-sources.md`, `03-schema-audit.md` ve statik alt rapordadır.
Bu bir bağlantı/kapsam kaydıdır; sitenin resmî testleri geçmiş olduğu anlamına gelmez.
