"""Complete report fields and export findings; writes audit artifacts only."""
import csv
import json
import re
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path('/Users/yavuz/prg/dr-cil')
OUT = ROOT / 'docs/audit/results/2026-11-24'
EV = OUT / 'evidence'

effects = {
 'NET-01':'Kayıt zamanındaki web adresleri çözümlenemediği için kullanıcı ve crawler erişimi engellenir; geçmiş kayıp/süre ve güncel tekrar sonucu bilinmiyor.',
 'UI-01':'Masaüstü menü etiketleri okunurluğunu ve gezinme rahatlığını kaybediyor; sıralama etkisi ölçülmedi.',
 'UI-02':'Hekimin istenen uzmanlık alanı kartta doğru anlamla anlatılmıyor.',
 'UI-03':'Mobil menünün klavyeyle kullanım ve kapanış yolu eksik; açık kalınca sayfa kaydırması kilitli kalabiliyor.',
 'UI-04':'Klavye/yardımcı teknoloji kullanıcısı modal dışına kaçabiliyor veya açıcı odağını kaybediyor.',
 'UI-05':'Sayfa diliyle uyuşmayan kontrol ve durum metinleri kullanım ve anlaşılmayı zorlaştırır.',
 'UI-06':'JS/CDN başarısızlığında bazı temel eylemler için dayanıklı bağlantı yolu eksik olabilir; runtime doğrulanmadı.',
 'UI-07':'Arapça hata sayfası İngilizce mesaj ve İngilizceye çıkış sunarak seçilmiş dilde toparlanma yolunu bozuyor.',
 'SCH-01':'Breadcrumb dizisinin sırası belirsizleşir; Google reddi veya ceza sonucu çıkarılamaz.',
 'SCH-02':'Aynı varlığın çelişen yol tanımları ve yanlış dil hedefleri makine yorumunu belirsizleştirir.',
 'SCH-03':'İşaretlemedeki ilişki sözlük domainine uymaz; tıbbi hizmet ile hekim ilişkisi doğru temsil edilmez.',
 'SCH-04':'Tür sınıfının enum alanında kullanımı sözlük doğrulamasında hata verir.',
 'SCH-05':'Makinenin hekim görseli olarak aldığı URL üretim çıktısında bulunmuyor; görünür hero görseli ayrı var.',
 'SCH-06':'Ziyaretçi ve makineye farklı çalışma saatleri veriliyor; gerçek randevu planı yanlış anlaşılabilir.',
 'SCH-07':'Hastalık/test/işlem konusu yanlış tıbbi entity ve anatomiyle anlatılabiliyor.',
 'SCH-08':'Otomatik review/kurum otoritesi bilgisi gerçekte kanıtlanmış inceleme/onay sanılabilir; gerçek dayanak bilinmiyor.',
 'SCH-09':'Liste, iletişim ve hata sayfaları içerik amaçlarıyla uyuşmayan makale olarak tanımlanıyor.',
 'SCH-10':'Makineye sunulan boş hizmet listesi gerçek görünür hizmet kapsamını açıklamıyor.',
 'STATIC-01':'CTA ve iç gezinme hedefleri üretimde çözülemeyebilir; dosya eksikliği canlı HTTP 404 ölçümü değildir.',
 'STATIC-02':'Sayfa 2+ için ayrı içerik ve eşdeğer dil adresleri yanlış ilk sayfayla ilişkilendiriliyor; Google seçimi bilinmiyor.',
 'STATIC-03':'Üç dil sitemap keşfi ve bakımında tek açık sahiplik yok; bütün dillerin indekssiz olduğu kanıtlanmadı.',
 'STATIC-04':'İngilizce kart istenen hizmet alt bölümüne doğrudan atlamıyor; sabit header etkisi henüz test edilmedi.',
 'STATIC-05':'Boş paralel arşiv/normal sayfalar arama ve gezinmeyi gereksiz seçeneklerle dolduruyor; organik zarar ölçülmedi.',
 'STATIC-06':'Kullanıcı seçtiği dilden farklı içerik açabilir; bunun bilinçli fallback olduğu açıkça anlatılmalı.',
 'STATIC-07':'Sayfa amaçları metadata ile yeterince ayrışmıyor; tekrarı tek başına ceza veya kritik hata saymak doğru değil.',
 'PERF-01':'Model ağ/CPU/GPU işi yaratır; gözlenen erken istek vardır, toplam performans veya pil etkisi nicel ölçülmedi.',
 'PERF-02':'Hareket/veri tercihleriyle uyuşmayan animasyon ve gereksiz model yükü oluşabilir; belirli cihaz etkisi ölçülmedi.',
 'PERF-03':'Senkron vendor zinciri parse/render zamanlamasına katkı yapabilir; ana darboğaz olduğu kanıtlanmadı.',
 'PERF-04':'Kaynak/öncelik seçimi iyileştirilebilir; üretimde LCP/CLS sorunu olduğu henüz ölçülmedi.',
 'PERF-05':'İlk aramada büyük veri ve senkron hazırlık etkileşim gecikmesi adayıdır; INP veya süre etkisi ölçülmedi.',
 'PERF-06':'Eski shortcode yeniden kullanılırsa script ayrışmaz; halen etkin sayfalarda çalışmadığı için mevcut runtime etkisi yok.',
 'CT-01':'Aynı kişinin çelişen doğum bilgisi güven ve doğruluk sorunu yaratır; doğru yıl denetimde seçilmedi.',
 'CT-03':'Okuyucu sayısal deneyim/yayın iddialarının kapsam ve dayanağını göremiyor; iddiaların yanlışlığı kanıtlanmadı.',
 'CT-04':'Hasta klinik oranların hangi grup/takip/sonlanıma ait olduğunu bağımsız doğrulayamıyor; klinik yanlışlık hükmü yok.',
 'CT-05':'Bilgilendirmeden ilgili gerçek hizmete hasta yolculuğu zayıf; sıralama kaybı ölçülmedi.',
 'CT-06':'Yazıdan hekimin mesleki kanıtına doğrudan geçiş eksik; biyografi genel menüde var.',
 'CT-08':'Bilgi/hekim/hizmet niyetleri karışabilir; GSC verisi olmadan cannibalization veya rank nedeni kesinleşmez.',
 'CT-09':'Görünen açıklama gerçek üretim veri akışının tamamını yansıtmayabilir; hukuki ihlal veya consent davranışı doğrulanmadı.',
 'HOST-01':'Yalnız statik dosyalar taşınırsa Netlify form işleme/teslimi kendiliğinden taşınmaz; gerçek teslim testi yapılmadı.',
 'HOST-02':'Eski URL ve hata durumları yeni sunucuda yanlış yanıt verebilir; hedef runtime henüz test edilmedi.',
 'HOST-03':'Yeni sunucuda stale içerik, MIME/güvenlik ve sıkıştırma davranışı kaynak dosyadan garanti edilemez.',
 'HOST-04':'Farklı Hugo sürümü ve destrüktif build adımları tekrarlanabilir yayın/geri dönüşü zorlaştırır; mevcut build geçmiştir.',
}

ui_steps = {
 'UI-01':'Önceki browser-layout-observations.json ve browser-menu-1280-crop.jpg kaydını aç. Yeniden test: / üzerinde 1024/1280/1440/1920 CSS px, DPR1, %100; her metin düğümünde Range rect satır sayısı ve computed flex/whiteSpace/wordBreak ölç. Bu tur browser tekrar testi NOT_RUN; 852/853/854 ve native200 de NOT_RUN.',
 'UI-02':'ui-static-extract.json kart değerlerini i18n/tr.yaml:12,25–26 ve hero.html:149–150 ile karşılaştır; /, /en/, /ar/ kart metinlerini kontrol et. Dar viewport/zoom yeni testi NOT_RUN.',
 'UI-03':'browser-keyboard-observations.json kaydındaki /hizmetler/dizalti-damar-tikanikligi/ 390×844 senaryosunu incele. Tekrar: menüyü aç, Escape, görünürlük/body scroll ve açıcı tabIndex/role ölç. Yeni runtime NOT_RUN.',
 'UI-04':'Aynı 390×844 sayfada randevu aç/kapat, Shift+Tab ve Escape; aramada Escape sonrası activeElement ölç. Önceki kayıt browser-keyboard-observations.json; yeni runtime NOT_RUN.',
 'UI-05':'Üç dilde header/search/footer metinlerini ui-source-notes.md kaynakları ve ui-static-extract.json ile karşılaştır; tam AR/ekran okuyucu/kontrast testi NOT_RUN.',
 'UI-06':'Belirtilen template içindeki gerçek href ile yalnız onclick eylemini karşılaştır. JS kapalı/CDN engelli tarayıcıda temel gezinmeyi denemek gerekir; bu test NOT_RUN.',
 'UI-07':'evidence/recheck-404.json içindeki üç üretilmiş hata sayfasının main h1 ve href değerlerini karşılaştır; layouts/404.html TR/else dallarını oku. Gerçek olmayan URL için HTTP404 yeni sunucuda ayrıca test edilmeli; NOT_RUN.',
}

def reproduction(fid):
    if fid in ui_steps:
        return ui_steps[fid]
    if fid == 'NET-01':
        return 'browser-public-dns.json içindeki tam name/type sorgularını ve google.com kontrolünü oku. Bu tur web aracı site sorgularından yanıt döndürmedi; ikinci resolver ve güncel DNS tekrar ölçümü Doğrulanamadı. Önceki kaydı güncel cevap sayma.'
    if fid.startswith('SCH-'):
        return 'evidence/recheck-schema.py ile tüm build taramasını yeniden üret; recheck-schema-output.json, schema-inventory.csv ve bu kaydın örnek JSON-LD dosyasını karşılaştır. Resmî validator tekrarı ayrı kod girişiyle yapılmalı; bu tur NOT_RUN.'
    if fid.startswith('STATIC-'):
        return 'evidence/static-audit.py BUILD OUT ile ayrı kanıt klasörüne bütün HTML taramasını üret; bu bulgudaki static-*.json örneklerini gerçek çıktı dosyasıyla karşılaştır. /tr/* ilan edilmiş redirect ayrımını static-link-triage.json ile koru. Dosya varlığı HTTP sonucu değildir.'
    if fid.startswith('PERF-'):
        if fid == 'PERF-06':
            return 'node --check evidence/performance-unused-shortcode-syntax.mjs; önceki syntax logunda exit1. recheck-perf-evidence.json eski model yolunun 0 HTML olduğunu doğrular. Üretim timing testi değildir.'
        return '04-performance.md içindeki aktif yol ve satırları, recheck-perf-evidence.json varlık sayımını, varsa önceki browser-dev-diagnostics.json ham koşularını karşılaştır. Production cold/warm, A/B ve CPU/GPU ölçümü NOT_RUN; yeniden koşma protokolü aynı rapordadır.'
    if fid.startswith('CT-'):
        return 'evidence/recheck-content-check.py --build-root BUILD ile 15 örnek çıktıyı tara; recheck-content-evidence.json ve bulgudaki kaynak satırını karşılaştır. Dış CV/klinik/hesap verisi bu komutla doğrulanmaz; gerekli onay/ölçüm ayrı bekler.'
    return '07-self-hosting-readiness.md içindeki dosya/satır ve üç dil form/redirect/header matrisini kaynakla karşılaştır. Hedef sunucuda sentetik staging POST ve GET/HEAD kabulünü çalıştırmak gerekir; bu denetimde NOT_RUN.'

text = (OUT / '01-findings.md').read_text()
for before,after in {
 'P1 · Örneklerde doğrulandı;':'P1 · Doğrulandı — örneklerde;',
 'P2 · Boş liste doğrulandı;':'P2 · Doğrulandı — boş liste;',
 'P1 · Statik doğrulandı;':'P1 · Doğrulandı — statik;',
 'P2 · Statik doğrulandı;':'P2 · Doğrulandı — statik;',
 'P2 · Veri doğrulandı;':'P2 · Doğrulandı — veri;',
 'P2 · İlk istek runtime doğrulandı;':'P2 · Doğrulandı — önceki runtime ilk isteği;',
 'P2 · Öznitelikler doğrulandı;':'P2 · Doğrulandı — öznitelikler;',
 'P2 · Çıktı öznitelikleri doğrulandı;':'P2 · Doğrulandı — çıktı öznitelikleri;',
 'P2 · Dosya boyutu/kod doğrulandı;':'P2 · Doğrulandı — dosya boyutu/kod;',
 'P1 · Sabit iddia doğrulandı;':'P1 · Doğrulandı — sabit iddia;',
 'P1 · Kaynak boşluğu doğrulandı;':'P1 · Doğrulandı — kaynak boşluğu;',
 'P1 geçiş kapısı · Kaynak kuralları doğrulandı;':'P1 geçiş kapısı · Doğrulandı — kaynak kuralları;',
 'P2 geçiş kapısı · Kaynak politikası doğrulandı;':'P2 geçiş kapısı · Doğrulandı — kaynak politikası;',
}.items():
    text=text.replace('**'+before,'**'+after)
notice = '''## Bu turdaki tekrar doğrulama ve kanıtın zamanı

Bu çalışma başlarken aynı günün kısmi raporları ve ham kanıtları zaten vardı.
Kaynak hashleri `recheck-worktree-state.json` içinde eski manifestle tamamen
eşleşti. Bu turda schema, içerik ve varlık taramaları yeniden çalıştırıldı;
önceki tarayıcı, DNS ve validator kayıtları korunarak yeniden okunmuştur.
İki yeni tarayıcı bağlantı denemesi zaman aşımına uğradı; bu turda runtime,
gerçek %200 zoom ve yeni Lighthouse sonucu yoktur. NET-01 önceki kamu DNS
yanıtının kayıt zamanında doğrulanmıştır; son durum bu tur yeniden ölçülemedi.
Web aracının site DNS sorgusunda hata vermesi bir DNS cevabı değildir.

Her bulgunun zorunlu alanları aşağıdadır; makineyle işlenebilir aynı alanlar
`09-findings-matrix.csv` içinde de vardır. `Yeniden üretim` adımları yeni bir
testin çalıştırıldığını ifade etmez; NOT_RUN sınırı ayrıca yazılmıştır.

'''
if '## Bu turdaki tekrar doğrulama ve kanıtın zamanı' not in text:
    text = text.replace('## Kanıtın nasıl okunacağı',notice+'## Kanıtın nasıl okunacağı',1)

new_ui = '''### UI-07 — Arapça 404 İngilizce metin ve İngilizce çıkışlar veriyor

**P2 · Doğrulandı — kaynak ve üretim HTML; HTTP durumu NOT_RUN**

- **URL/kapsam:** https://docdrhabibcil.com/ar/404.html; karşılaştırma /404.html ve /en/404.html
- **Kaynak:** layouts/404.html:8–15,19–43; i18n/ar.yaml:48–50
- **Olgu / kök neden:** Özel şablon yalnız TR ve else ayırıyor. AR kök dir=rtl olsa da main başlığı Page Not Found; dönüş /en/ ve iletişim /en/contact/. Arapça 404 çeviri anahtarları var ama bu şablon kullanmıyor. TR çıkışları eski /tr/ yolları; ilan edilmiş 301 ile çalışabilir. Statik dosya olması gerçek HTTP404 sonucunu kanıtlamaz.
- **Öneri:** Üç dil için yerelleştirilmiş mesaj ve gerçek dil köküne/iletişime dönüş; hedef sunucuda doğru dil hata gövdesiyle 404 durumunu ayrıca sağlamak.
- **Kabul:** AR mesaj/çıkış /ar/ ve /ar/contact/; TR kök /; EN /en/. Olmayan gerçek URL GET404, dil korunur; keyboard/focus ve RTL testli.
- **Kanıt:** recheck-404.json; 02-url-and-template-inventory.csv

'''
if '### UI-07 ' not in text:
    text=text.replace('## Yapılandırılmış veri',new_ui+'## Yapılandırılmış veri',1)

new_ct = '''### CT-09 — Gizlilik açıklaması ile gerçek üretim veri akışı eşlenmeli

**P2 · Güçlü aday — kaynak doğrulandı; runtime/hukuki sonuç Doğrulanamadı**

- **URL/kapsam:** https://docdrhabibcil.com/kvkk/; /en/privacy/ ve /ar/privacy/; üç dil iletişim formları
- **Kaynak:** content/tr/kvkk/index.md:30–55; layouts/partials/extend-head-uncached.html:9–24; üç contact index.md:56–58
- **Olgu / kök neden:** Gizlilik sayfaları var; TR metin form/WhatsApp/sağlık verisini anıyor. Üretimde Google tag kodu ve Netlify form bağımlılığı var. Metinlerde bu altyapı ve saklama süresi açıklaması saptanmadı. Gerçek veri akışı/çerez/tercih davranışı ölçülmedi; bunların her birinin yasal zorunluluğu veya ihlal olduğu ileri sürülmüyor.
- **Öneri:** Seçilen backend/analitik ve gerçek veri akışını görünür metin/tercihlerle yetkili uzman üzerinden eşlemek; gereksiz hasta verisi toplamamak.
- **Kabul:** Üretim istek/çerez ve tercih testi; gerçek sağlayıcı/amaç/saklama kararları; üç dilde doğru açıklama; hukuki uygunluk için yetkili inceleme.
- **Kanıt:** recheck-content-evidence.json; recheck-content-sources.md; 07-self-hosting-readiness.md/CT-09

'''
if '### CT-09 ' not in text:
    text=text.replace('## Kendi sunucusuna geçiş kapıları',new_ct+'## Kendi sunucusuna geçiş kapıları',1)

# Preserve existing evidence/diagnoses; append the two missing mandatory fields.
for match in reversed(list(re.finditer(r'^### ((?:NET|UI|SCH|STATIC|PERF|CT|HOST)-\d+) — (.+)$',text,re.M))):
    fid=match.group(1)
    start=match.end()
    following=re.search(r'^#{2,3} ',text[start:],re.M)
    end=start+following.start() if following else len(text)
    block=text[start:end]
    if '**Yeniden üretim:**' not in block:
        addition=f'- **Yeniden üretim:** {reproduction(fid)}\n- **Kullanıcı/arama etkisi:** {effects[fid]}\n\n'
        text=text[:end].rstrip()+'\n'+addition+text[end:]
(OUT/'01-findings.md').write_text(text)

rows=[]
for match in re.finditer(r'^### ((?:NET|UI|SCH|STATIC|PERF|CT|HOST)-\d+) — (.+)$',text,re.M):
    start=match.end(); following=re.search(r'^#{2,3} ',text[start:],re.M)
    block=text[start:start+following.start()] if following else text[start:]
    status=re.search(r'\*\*(P[0-3][^\n]*)\*\*',block).group(1)
    fields=dict(re.findall(r'^- \*\*([^*]+):\*\* (.*)$',block,re.M))
    row={'ID':match.group(1),'Öncelik':status.split(' · ')[0],'Durum/güven':status.split(' · ',1)[-1],
      'URL/şablon':fields['URL/kapsam'],'Kaynak dosya:satır':fields['Kaynak'],
      'Gerçek çıktı/ölçüm':fields['Olgu / kök neden'],'Yeniden üretim':fields['Yeniden üretim'],
      'Kullanıcı/arama etkisi':fields['Kullanıcı/arama etkisi'],'Kök neden':fields['Olgu / kök neden'],
      'En küçük çözüm önerisi':fields['Öneri'],'Kabul testi':fields['Kabul'],
      'Kanıt dosyası/resmî kaynak':fields['Kanıt']}
    rows.append(row)
with (OUT/'09-findings-matrix.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

print(json.dumps({'findings':len(rows),'mandatory_fields_complete':all(all(str(v).strip() for v in r.values()) for r in rows),'source_changed_by_this_script':False},ensure_ascii=False))
