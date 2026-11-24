"""Assemble implementation deliverables from real local acceptance artifacts."""
import collections
import csv
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit

ROOT=Path('/Users/yavuz/prg/dr-cil')
OUT=ROOT/'docs/implementation/seo-remediation/2026-11-24'
EV=OUT/'evidence'
PUBLIC=Path('/tmp/dr-cil-implementation-after-20261124-release/public')
AUDIT=ROOT/'docs/audit/results/2026-11-24'
def read(name): return json.loads((EV/name).read_text())
before=read('static-before/static-summary.json'); after=read('static-after/static-summary.json')
schema=read('schema-after-final.json'); ui=read('ui-contract-final.json'); release=read('seo-release-final.json')
assert schema['error_count']==0 and not ui['errors'] and release['error_count']==0
assert read('contact-form-tests.json')['passed']==8
assert read('heart-viewer-node-tests.json')['passed']==9
assert read('final-build-manifest.json')['exit_code']==0

actions={
 'NET-01':('DNS kayıtları değiştirilmedi; iki DoH yüzeyi site için yanıt getirmedi, kontrol yanıtı var.','06-launch-readiness.md','dns-readonly-recheck.json','Yetkili zone/iki resolver/origin/TLS'),
 'UI-01':('Başlık parametresi ve koşulu, alan hesabı, nowrap ve 1024 breakpoint düzeltildi.','layouts/partials/header/basic.html; assets/css/custom.css','ui-contract-final.json','Görünüm matrisi ve native %200'),
 'UI-02':('Doğrudan/fallback uzmanlık üç dilde Girişimsel Kardiyoloji anlamına eşitlendi.','i18n/tr.yaml; i18n/en.yaml; i18n/ar.yaml; layouts/partials/home/hero.html','ui-static-validation.json','Dar ekran/görsel kabul'),
 'UI-03':('Semantik menü düğmeleri, expanded, Escape, odak ve scroll yönetimi.','assets/js/mobilemenu.js; layouts/partials/header/basic.html','ui-contract-final.json','Gerçek klavye/ekran okuyucu'),
 'UI-04':('Ortak modal focus trap/inert, odak dönüşü; arama adı ve durum alanları.','assets/js/mobilemenu.js; assets/js/search.js; layouts/partials/extend-footer.html','ui-contract-final.json','Gerçek Tab/Shift+Tab ve modal kabulü'),
 'UI-05':('Üç dil metin/adlar, AR yönleri ve diğer dil arama etiketi.','i18n; layouts/partials/search.html; assets/js/search.js','ui-static-validation.json','EN/AR runtime ve ekran okuyucu'),
 'UI-06':('Native details gezinme ve gerçek href ile iletişim fallback.','layouts/partials/header/basic.html; layouts/partials/home/hero.html','ui-contract-final.json','JS/CDN kapalı gerçek tarayıcı'),
 'UI-07':('Üç dil 404 metni ve doğru dilde home/contact çıkışları.','layouts/404.html','ui-contract-final.json','Gerçek HTTP404 ve RTL kabulü'),
 'SCH-01':('Tek breadcrumb verisi, artan 1..N.','layouts/partials/schema-breadcrumb-items.html','schema-after-final.json','Resmî temsilci kod testi'),
 'SCH-02':('Tek breadcrumb tanımı ve canonical ile tutarlı kimlik.','layouts/partials/schema.html; layouts/partials/seo/current-page-url.html','schema-after-final.json','Resmî temsilci kod testi/HTTP'),
 'SCH-03':('Event dışı performer merge kaldırıldı.','layouts/partials/schema-procedure.html; layouts/partials/schema.html','schema-after-final.json','Resmî sözlük doğrulayıcı tekrarı'),
 'SCH-04':('Sınıf ile enum ayrıldı; geçersiz procedureType üretilmiyor.','layouts/partials/schema-procedure.html; data/schema_content_types.yaml','schema-after-final.json','Resmî test ve klinik sınıflandırma onayı'),
 'SCH-05':('Gerçek yayımlanmış image resource URL kullanılıyor.','layouts/partials/schema.html','schema-after-final.json','Public GET/MIME/taranabilirlik'),
 'SCH-06':('Çelişkili otomatik saat üretimi kaldırıldı; gerçek saat seçilmedi.','layouts/partials/schema.html; medical-review/00-identity-and-clinic-approval.md','schema-after-final.json','Gerçek klinik saatleri/GBP kaydı'),
 'SCH-07':('Kör Heart/status/anatomi varsayımları kaldırıldı; başlığa dayalı dar harita ve genel Service fallback.','layouts/partials/schema-procedure.html; data','schema-content-classification.csv','Hekimin tüm sınıflandırma/klinik ayrıntı onayı'),
 'SCH-08':('Lastmod-review, otomatik dernek onayı/koordinat/fiyat/sameAs iddiaları üretilmiyor.','layouts/partials/schema.html; layouts/partials/schema-procedure.html','schema-after-final.json','Gerçek inceleme/otorite/ofis kaydı'),
 'SCH-09':('Makale, koleksiyon, profil, iletişim ve yardımcı sayfa türleri ayrıldı.','layouts/partials/schema.html','schema-after-final.json','Resmî temsilci tür testleri'),
 'SCH-10':('Boş ItemList yerine görünür gerçek hizmet bağlantıları.','layouts/partials/schema.html','schema-after-final.json','Resmî temsilci kod testi'),
 'STATIC-01':('45 dosyada 98 eski/bozuk literal hedef onarıldı; nihai çözülemeyen link 0.','content; evidence/static-link-replacements.json','static-after/static-summary.json','Gerçek HTTP kabulü'),
 'STATIC-02':('15 gerçek pagination self-canonical; kanıtlanmamış sayfa2+ hreflang omit, normal çeviriler korunur.','layouts/partials/head.html; layouts/partials/seo','seo-release-final.json','Gerçek HTTP/GSC canonical seçimi'),
 'STATIC-03':('Üç açık sitemap ve robots; çakışan static/custom native sahipliği kaldırıldı.','hugo.toml; layouts/home.sitemappages.xml; static/robots.txt','static-after/static-sitemaps.json','Üretim XML GET200/keşif'),
 'STATIC-04':('EN home pacemaker anchor gerçek bölüm ID ile eşlendi.','content/en/_index.md','static-after/static-broken-fragments.json','Browser scroll/header kabulü'),
 'STATIC-05':('53 kesin term eşleşmesi gerçek içerikle dolduruldu; 2 belirsiz sayfa ve konsolidasyon kararı açık.','layouts/partials/seo/manual-taxonomy-links.html; layouts/_default/single.html','static-taxonomy-exact-matches.json','İki eşleşme ve indeks/URL politikası'),
 'STATIC-06':('Bilinçli dil fallback korundu, language/name ve sonuç dil etiketi eklendi.','layouts/_default/index.json; assets/js/search.js','seo-release-final.json','Gerçek üç dil arama akışı'),
 'STATIC-07':('Önemli sayfa ve pagination metadata ayrıştırıldı; genel arşiv fallback tekrarları tamamen bitmedi.','layouts/partials/head.html; content/tr','static-after/static-duplicate-descriptions.json','Kalan arşiv metadata/ürün kararı'),
 'PERF-01':('Poster + kullanıcı isteği, tek frame zinciri ve offscreen/hidden duruş.','assets/js/heart-viewer.js; layouts/partials/three-heart.html','heart-viewer-node-tests.json','Gerçek production trace/A-B/WebGL'),
 'PERF-02':('Reduced-motion, Pause, hata/Retry ve kullanıcı isteği; CSS hareket tercihi.','assets/js/heart-viewer.js; assets/css/custom.css','heart-viewer-node-tests.json','OS tercihi/Save-Data/CDN hatası runtime'),
 'PERF-03':('Senkron vendor için ölçülmemiş darboğaz hükmü verilmedi; kör defer uygulanmadı.','layouts/partials/head.html; 05-performance-before-after.md','performance-before-after-assets.json','Production CPU/ağ izleri'),
 'PERF-04':('Hero intrinsic boyut, responsive srcset/sizes ve eager/high priority.','layouts/partials/home/hero.html','performance-before-after-assets.json','Production LCP/CLS ve görsel kalite'),
 'PERF-05':('İndeks dil/veri yapısı iyileştirildi; Fuse/parse gecikmesi ölçülmeden worker kararı alınmadı.','layouts/_default/index.json; assets/js/search.js','performance-before-after-assets.json','Yavaş mobil ilk arama/long task ölçümü'),
 'PERF-06':('Bozuk ikinci shortcode kaldırılıp çalışan tek partial/module yoluna bağlandı.','layouts/shortcodes/three-heart.html','heart-viewer-node-tests.json','Ortak gerçek WebGL kabulü genel pakette'),
 'CT-01':('Doğum yılı seçilmedi; üç dil çelişkisi onay matrisine alındı.','medical-review/00-identity-and-clinic-approval.md','initial-worktree.json','Doğru CV/kişisel bilgi onayı'),
 'CT-03':('25+/20K+/100+ için dayanak/bağlam isteniyor; yeni iddia eklenmedi.','medical-review/00-identity-and-clinic-approval.md','initial-worktree.json','Kayıt sahibi/CV ve kapsam onayı'),
 'CT-04':('47 yüzde satırı korunup 12 somut kaynaklı inceleme taslağı hazırlandı.','medical-review/01-clinical-claims-review.md','clinical-claims-preserved.json','Hekim onayı/popülasyon/sonlanım/takip kaynağı'),
 'CT-05':('İki rehber ile gerçek vasküler/dizaltı hizmetler çift yönlü bağlandı.','content/tr/blog; content/tr/hizmetler','seo-release-final.json','Gerçek HTTP kabulü genel staging kapısı'),
 'CT-06':('Yazar adı doğru dilde mevcut hekim biyografisine bağlandı.','layouts/partials/author.html','static-after/static-summary.json','Gerçek HTTP kabulü genel staging kapısı'),
 'CT-08':('Sekiz sorgu mevcut farklı amaçlara eşlendi; yeni benzer keyword sayfaları yok.','02-keyword-content-map.csv; content/tr','seo-release-final.json','Hizmet kapsamı onayı/GSC baseline'),
 'CT-09':('Varsayılan form kapalı; gerçek veri akışı/analitik inceleme formu hazırlandı.','medical-review/02-data-flow-and-privacy-review.md','contact-form-tests.json','Veri sorumlusu/sağlayıcı/saklama ve runtime/hukuki inceleme'),
 'HOST-01':('Provider kapısı, gerçek fallback ve 3 bağımsız noindex teşekkür URL; sahte teslim iddiası yok.','layouts/shortcodes/contact-form.html; content/tr/iletisim-sonrasi/index.md; content/en/contact-success/index.md; content/ar/contact-success/index.md; config/_default/params.toml','contact-form-tests.json','Gerçek backend seçimi ve yetkili teslim testi'),
 'HOST-02':('Yerel Netlify eski URL kuralları, doğrudan legacy home hedefleri ve lokalize404 şablonu.','static/_redirects; layouts/404.html','seo-release-final.json','Hedef sunucu ürünü/gerçek HTTP301/404'),
 'HOST-03':('Mevcut header politikası korunur; bilinmeyen sunucu için çalışmış ayar uydurulmadı.','06-launch-readiness.md; netlify.toml','test-server-attempt.json','Origin/TLS/cache/sıkıştırma/HTTP kabulü'),
 'HOST-04':('Yeni/boş hedef zorunlu güvenli release builder, manifest ve 0.167.0 pin; yıkıcı Netlify temizliği kaldırıldı.','scripts/build-production.py; hugo-version.txt; netlify.toml','build-existing-output-guard.json','Tema destek aralığı uyarısı ve gerçek yayın/rollback kabulü'),
}
blocked={'NET-01','SCH-06','CT-01','CT-03','CT-04','CT-09','HOST-03','PERF-03','PERF-05'}
verified={'CT-05','CT-06','PERF-06'}
audit_rows=list(csv.DictReader((AUDIT/'09-findings-matrix.csv').open(encoding='utf-8-sig')))
assert set(actions)=={r['ID'] for r in audit_rows}
def status(fid): return 'Bloke' if fid in blocked else 'Doğrulandı' if fid in verified else 'Uygulandı–Doğrulama Bekliyor'
def cell(value): return str(value).replace('|',' / ').replace('\n',' ')
progress=['# Uygulama ilerlemesi — 24 Kasım 2026','',
 'Yerel kaynak düzeltmeleri uygulandı. `Doğrulandı` yalnız satırda belirtilen yerel kabulü ifade eder; gerçek HTTP, Google, klinik veya tüm site WCAG geçişi değildir. Görsel/runtime kabulü olmayan işler kapatılmadı. Klinik/dış hesap engelleri bağımsız kod işlerini durdurmadı.','',
 '| ID | Güncel teşhis / uygulama | Değişiklik/dosya | Önceki kanıt | Kabul testi | Sonraki kanıt | Durum | Dış bağımlılık |',
 '| --- | --- | --- | --- | --- | --- | --- | --- |']
for row in audit_rows:
 fid=row['ID']; action,files,evidence,dependency=actions[fid]
 progress.append('| '+' | '.join(map(cell,[fid,action,files,'Audit01/'+fid+'; '+row['Kanıt dosyası/resmî kaynak'].replace('](evidence/', '](../../../audit/results/2026-11-24/evidence/'),row['Kabul testi'],'evidence/'+evidence,status(fid),dependency]))+' |')
progress+=['','## B01–B15 paketleri','', '| Paket | Yerel sonuç | Açık kabul |','| --- | --- | --- |']
package_notes=[
 ('B01','Salt okunur DNS tekrar denemesi; kayıt değişikliği yok','Zone/iki resolver/TLS/origin'),
 ('B02','Header/uzmanlık uygulandı; HTML/i18n kontrolü geçti','12 genişlik, yeni1023/1024/1025 ve native200'),
 ('B03','Menü/modal/arama semantiği ve odak kodu uygulandı','Gerçek keyboard/ekran okuyucu'),
 ('B04','Nihai link/asset/fragment0','Gerçek HTTP/anchor scroll'),
 ('B05','Provider-gated form ve gerçek teşekkür/404 sayfaları','Backend/teslim ve hedef301/404'),
 ('B06','Bütün JSON-LD hedefli tarama0','Resmî araç/klinik sınıflandırma'),
 ('B07','8 kimlik onayı,12 klinik taslak,47yüzde envanteri','Kayıt sahibi/hekim onayı'),
 ('B08','Canonical/hreflang0;3XML','Origin XML/redirect/GSC'),
 ('B09','3B9test;poster/lifecycle/hero kaynağı uygulandı','Production cold/warm/trace/A-B/CWV'),
 ('B10','8sorgu/53kesin arşiv, iç bağlantılar','2taxonomy,kalan metadata,53statik orphan adayı/GSC'),
 ('B11','Üç dil/RTL/fallback kaynağı ve HTML kontratı','Gerçek JS-off/RTL/reflow/kontrast'),
 ('B12','Doğru yardımcı sayfa türleri/dolu ItemList','Resmî temsilci test'),
 ('B13','Güvenli builder/pin/manifest; mevcut hedef koruma geçti','Tema uyarısı/origin header ve rollback'),
 ('B14','Veri akışı onay formu; varsayılan form alanı yok','Gerçek analitik/çerez/sağlayıcı/hukuki inceleme'),
 ('B15','İkinci bozuk shortcode tek modüle konsolide','Genel WebGL kabulü')]
progress += ['| '+' | '.join(map(cell,x))+' |' for x in package_notes]
progress += ['','Durum toplamı: '+json.dumps(dict(collections.Counter(status(r['ID']) for r in audit_rows)),ensure_ascii=False),
 '', 'Önceki tam bulgu/kabul: [01-findings.md](../../../audit/results/2026-11-24/01-findings.md). Yeni kanıtlar bu klasörde korunur.']
(OUT/'00-progress.md').write_text('\n'.join(progress)+'\n')

keywords=list(csv.DictReader((AUDIT/'05-keyword-url-map.csv').open(encoding='utf-8-sig')))
changes=[
 'Mevcut home title yayımlanır; biyografi/yayın/klinik bağlantıları, uzmanlık ve hizmet yolları.',
 'Aynı home/kimlik niyeti korunur; gerçek biyografi ve yazar bağlantısı.',
 'Rehber description dengelendi; mevcut vasküler hizmet/rehber bağlantıları eklendi; klinik sayılar değişmedi.',
 'Hizmet hub başlığı/description ve koroner/periferik/diğer dallara açıklayıcı navigasyon.',
 'Hub ve gerçek bölüm anchor; üç dil hero uzmanlık doğrudan/fallback düzeltmesi.',
 'Mevcut dizaltı URL korunarak title/description ve ilgili rehber bağlantıları.',
 'Genel sorgu hub üzerinden gerçek koroner/periferik sayfalara ayrılır.',
 'Mevcut rehber ile gerçek vasküler hizmetler; kapsamı doğrulanmamış yeni hizmet sayfası yayımlanmadı.']
for row,change in zip(keywords,changes):
 row['uygulanan_degisiklik']=change
 row['kabul']='Nihai statik hedef/canonical geçti; HTTP/GSC/GBP/SERP NOT_RUN'
 path=urlsplit(row['mevcut_canonical_url']).path
 file=PUBLIC/path.lstrip('/')/'index.html'
 assert file.is_file(),str(file)
 assert row['mevcut_canonical_url'] in file.read_text()
 row['kanit']='evidence/seo-release-final.json; evidence/static-after/static-summary.json'
with (OUT/'02-keyword-content-map.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(keywords[0]));w.writeheader();w.writerows(keywords)

initial=read('initial-worktree.json'); clinical=[]
for name in ['content/tr/blog/diyabetik-ayak/index.md','content/tr/blog/periferik-arter-hastaligi/index.md',
 'content/tr/hizmetler/dizalti-damar-tikanikligi/index.md','content/tr/hizmetler/periferik-damar/index.md']:
 old=subprocess.check_output(['git','show',initial['commit']+':'+name],cwd=ROOT,text=True)
 new=(ROOT/name).read_text()
 a=[x.strip() for x in old.splitlines() if '%' in x]; b=[x.strip() for x in new.splitlines() if '%' in x]
 clinical.append({'source':name,'before_percent_lines':len(a),'after_percent_lines':len(b),'unchanged':a==b})
(EV/'clinical-claims-preserved.json').write_text(json.dumps(clinical,ensure_ascii=False,indent=2))
assert all(x['unchanged'] for x in clinical)

summary='''# Kaynak değişiklikleri ve doğrulama — 24 Kasım 2026

Yerel uygulama tamamlandı; bütün başlangıç bulguları durum matrisine bağlandı.
Çalışmayan gerçek browser/production testleri ve klinik/dış veri bağımlılıkları
açık tutuldu. DNS, hesap, gerçek mesaj/randevu ve deploy yapılmadı; commit/push yok.

## Somut değişiklikler

- Menü alanı/breakpoint/nowrap ve mevcut başlık tercihi; gerçek düğmeler,
  ortak modal odak/inert/Escape, üç dil metinler, AR404, JS fallback.
- Mevcut URL'lerde hedef sayfa metadata ve rehber↔hizmet↔hekim bağlantıları.
  Sekiz sorgu CSV'de ayrı niyetle eşlenir; yeni benzer keyword sayfası yok.
- 45 kaynakta98 eski/bozuk link; EN home fragment;13 emekli home/sitemap
  kuralı +4 doğrudan /tr/page istisnası.12 home duplicate/alias route retire edilir;
  eski canonical içerikler korunur. Gerçek HTTP301 testi yapılmadı.
- Gerçek pagination self-canonical/title/OG; kanıtlanmış eşdeğerlik olmayan
  sayfa2+ hreflang omit; normal çevirilerin self/return bağlantıları korunur.
- Üç açık dil sitemap'i ve robots, tek sahiplik;53 kesin arşiv eşleşmesinde
  gerçek içerik bağlantıları;2 belirsiz manuel sayfaya tahmin uygulanmadı.
- Tek schema graph/breadcrumb, doğru amaç türleri, gerçek image; yanlış
  performer/enum/anatomi/status ve otomatik review/kurum/saat iddiaları kaldırıldı.
- 3B anatomik poster + kullanıcı isteği, tek frame zinciri, offscreen/hidden
  duruş, reduced-motion/Pause ve hata/Retry; eski shortcode konsolide edildi.
  Hero intrinsic boyut/srcset/sizes; gerçek iletişim href'i.
- Provider seçilene kadar iletişim formu render edilmez; telefon/WhatsApp
  bağlantıları vardır.8 sağlayıcı/URL senaryosu×3 dil Hugo fixture'ında geçti.
  Üç bağımsız teşekkür URL noindex/search/sitemap dışı; teslim iddiası üretmez.
- Güvenli build aracı boş/yeni hedef ister, kaynak public/resources'u temizlemez.
  Test edilen Hugo0.167.0 yerel/Netlify kaynak tanımında pinlendi; tema sürümü
  korunur. Theme destek aralığı/deprecation uyarıları devam eder.

## Önce / sonra — statik çıktı

| Ölçüm | Başlangıç | Nihai | Kanıt |
| --- | ---: | ---: | --- |
'''
metrics=[('HTML dosyası','html_total'),('Alias/404 dışı route','actual_non_alias_non404'),('Ayrı canonical','unique_canonicals'),
 ('Statik noindex','noindex_actual'),('Ham eksik link kullanımı','broken_link_instances'),('Eksik HTML asset','broken_asset_instances'),
 ('Eksik fragment','broken_fragment_instances'),('Canonical sorunu','canonical_issues'),('Hreflang sorunu','hreflang_issues'),('Statik orphan adayı','orphan_candidates')]
old_md=sum(n.startswith('content/') and n.endswith('.md') for n in initial['tracked_sha256'])
new_md=len(list((ROOT/'content').rglob('*.md')))
summary+='| Kaynak Markdown | '+str(old_md)+' | '+str(new_md)+' | source manifest |\n'
summary+='| Alias HTML | '+str(before['by_classification']['alias'])+' | '+str(after['by_classification']['alias'])+' | static-before/after |\n'
summary+='| Özel404 HTML | '+str(before['by_classification']['404'])+' | '+str(after['by_classification']['404'])+' | static-before/after |\n'
summary+='| Pagination HTML | '+str(before['by_classification']['pagination'])+' | '+str(after['by_classification']['pagination'])+' | static-before/after |\n'
summary+='\n'.join('| '+name+' | '+str(before[key])+' | '+str(after[key])+' | static-before/after |' for name,key in metrics)
summary+='''

Başlangıç98 ham linkin32'si eski /tr kuralıyla çözülebiliyordu;66'sı çözülemiyordu.
Nihai0 ölçümü ham taramada da0'dır. HTML sayısındaki azalma yeni içerik silinmesi
değildir:9 gereksiz home pagination +3 home/page/1 alias kaldırıldı,3 gerçek
yardımcı teşekkür sayfası eklendi.670 canonical'ın3'ü noindex yardımcı sayfadır;
667 statik indekslenebilir aday Google indeks sayısı değildir. Sitemap union652
normal canonical;15 gerçek pagination HTML linkleriyle keşfedilir, sitemap'e
ayrıca eklenmedi.652 eski canonical içerik ve üç özel404 canonical korunur.

## Gerçekten geçenler

'''
summary+=f'- Nihai minify production build exit0: `{PUBLIC.parent}`; Hugo0.167.0.\n'
summary+=f'- {schema["counts"]["html"]} HTML / {schema["counts"]["scripts"]} JSON-LD: yerel hedefli schema ihlali0. Resmî validator değildir.\n'
summary+=f'- {ui["html_tested"]} nonalias HTML UI kontratı: hata0; gerçek görünüm/klavye değildir.\n'
summary+=f'- {release["passed"]} release kabul kontrolü; eski canonical koruma,8 hedef,search/sitemap/form/redirect kuralları.\n'
summary+='''- 9 Node lifecycle/DOM-stub testi; gerçek WebGL/CPU/GPU değildir.
- 8 contact shortcode senaryosu,24 Hugo dil render'ı; HTTP/teslim değildir.
- Mevcut release hedefini reddetme exit2 ve eski manifest hash'inin korunması.
- 47 yüzde satırı başlangıç Git sürümüyle birebir aynı; klinik sayılar değiştirilmedi.

Komutlar/sonuçlar: evidence/final-test-commands.json, schema-after-final.json,
ui-contract-final.json, seo-release-final.json, contact-form-tests.json,
heart-viewer-node-tests.json ve build-existing-output-guard.json.

## Test edilmeyenler ve kalan işler

Native%200 ve genişlik matrisi (yeni1023/1024/1025 dahil), gerçek Tab/ekran
okuyucu/kontrast/RTL/JS-off; üretim ≥3desktop+3mobile cold ve sıcak ölçüm,
Lighthouse/CPU-GPU/modelA-B ve hata senaryoları; resmî schema/RRT tekrarı;
originHTTP/TLS/headers/301/404; GSC/GBP/CrUX/SERP ve gerçek mesaj teslimi NOT_RUN.
İzinli mevcut1314 HTTP gövdesi baseline ile byte-eş doğrulandı; ölçüm kurulumu
kernel reset nedeniyle çalışmadı, sonraki bağlantı timeout oldu. Yeni1315
socket.bind Operation not permitted: kısıt aşılmadı, kullanıcı server'ı durmadı.

İki belirsiz taxonomy ve kalan genel metadata tekrarları karar bekler; statik
orphan53 bir aday sayımıdır,53 indeks/ceza hatası değildir. PERF03/05 için
ölçülmemiş CPU darboğazı veya INP hükmü kurulmadı. Klinik kimlik/saat/istatistik
ve review olguları medical-review altında onay bekler. 6 hedef sayfanın lastmod'u
gerçek editoryal değişiklik tarihiyle güncellendi; tıbbi review tarihi değildir.

## Koruma ve geri dönüş

Tema alt modülü ve önceki audit kanıtları korunur. Değişiklikler henüz commit
edilmedi. `evidence/source-changes.patch` yalnız uygulama kaynaklarını içerir;
yeni dosyalar dahil tam liste manifesttedir. Otomatik rollback çalıştırılmadı.
Başka değişiklikler geldiyse ters patch uygulamadan önce güncel diff incelenmeli.
Üretim release'i değiştirilmedi; yayın/atomik geri dönüş kabulü06dosyasındadır.

Sonuç dizinindeki [00-progress.md](00-progress.md), [02-keyword-content-map.csv](02-keyword-content-map.csv),
[04-schema-validation.md](04-schema-validation.md), [05-performance-before-after.md](05-performance-before-after.md)
ve [06-launch-readiness.md](06-launch-readiness.md) birlikte okunmalıdır.
'''
(OUT/'01-changes-and-validation.md').write_text(summary)

launch=f'''# Yayın hazırlığı — 24 Kasım 2026

**Deploy yapılmadı; yayın kabulü tamamlanmış değildir.** Yerel kaynak ve çıktı
kabulü geçti; klinik veri/gerçek browser/origin kapıları aşağıda bekliyor.

## Somut release paketi

- Üretilen kök: `{PUBLIC}`.
- Build log ve SHA-256 manifest: evidence/final-build.log ve final-build-manifest.json.
- Kaynak farkı/yeni dosyalar: evidence/source-changes.patch ve final-preservation.json.
- Builder: `npm run build -- --output /tmp/dr-cil-yeni-bos-release`.
  Hedef yeni veya boş olmalıdır; eski release'e yazma reddedilir.
- Pin Hugo Extended0.167.0, tema7ce8be1/v2.93.0; tema bildirilen aralık üstü
  uyarısı vardır. Yerel derleme/çıktı testleri bu uyarıyı yok sayarak resmi
  tema uyumluluk veya tam tarayıcı garantisi vermez. Canlı Netlify ayarı değişmedi.

Üretim build'i geçici klasördedir; kalıcı release arşivi yerine geçmez.
Kod/rapor/manifest depoda; aynı komutla ayrı yeni build üretilebilir. Kamuya
sunulacak dosyalar yalnız public altıdır; cache/resources/manifest/raporları
web köküne kopyalamayın. Netlify'nin yeni yerel build tanımı artık --gc veya
tema/public silme komutu çalıştırmaz.

## Dış kapılar ve yapılacak tek somut adım

| Kapı | Şu anki kanıt | Tamamlama |
| --- | --- | --- |
| Browser/performans | Baseline1314hash eş; yeni test portu yasak, ölçüm bağlantısı timeout | Port izni ve çalışan tarayıcı olan ortamda bu release'i ayrı sun; 3+3cold/warm/native200 paketini çalıştır |
| DNS | Yeni DoH sorgularında site cevabı yok; kontrol başarılı; kayıt değişmedi | Yetkili zone+amaçlanan origin;authoritative/iki resolver ile A/AAAA/CNAME/NS |
| TLS ve yönlenme | Kaynak `_redirects` kuralları; gerçek yanıt yok | Apex/www/HTTP→HTTPS/sertifika ve IPv6 varsa ölç |
| HTTP404/301 | Dil şablonları ve explicit rules yerel kabulden geçti | Gerçek sunucuda doğru dilde404; tek301/query/UTF-8; SPA home200 yok |
| Form | Varsayılan disabled, gerçek telefon/WhatsApp;8statik senaryo geçti | Gerçek backend/teslim adresi seç;yetkili staging sentetik teslim+error/spam+teşekkür |
| Header/cache | Netlify kaynak politikası korunur; yeni sunucu bilinmiyor | Seçilen sunucuya açık aktarım;HTML/JSON/XML revalidation, MIME/ETag/Brotli/gzip/TLS |
| Google/schema | Tüm script yerel parse/kurallar0; resmî test yeni değil | Temsilci TR/EN/ARproduction koduyla Validator+RRT;GSCURLInspection ayrı |
| Klinik gerçeklik | 8kimlik onayı,12klinik taslak,47% satırı korunur | Kayıt sahibi/hekim;doğru yıl/saat/sayı/kaynak/review |
| GSC/GBP/CrUX | Yetkili araç/veri bulunmadı; hesap değişmedi | Performancequery/page/device/country;indexing/sitemap/canonical/security/manualaction;GBPbilgileri;CWVdönemi |
| İndeks politikası | 53kesin arşiv dolduruldu,2unknown;eski canonical'lar korunur | Gerçek ihtiyaç/URLverisiyle kalan taxonomy/metadata kararı;otomatiknoindex/silme yok |

Tek ortam adımı için örnek **yerel önizleme** komutu (bu ortamda bind
reddedildi; kullanıcı sunucusunu durdurmadan izinli bir boş port gerekir):

```sh
python3 -m http.server 1315 --bind 127.0.0.1 --directory {PUBLIC}
```

Bu Python önizlemesi Netlify redirect/header/form veya dil bazlı404 kurallarını
uygulamaz; yalnız UI/performans önizlemesidir, üretim hosting seçimi değildir.
Sunucu türü bilinmediği için çalışmış Nginx/Caddy/Apache ayarı icat edilmedi.

## Yayın ve geri dönüş sırası

1. Yetkili platform/hedef ve gerçek kayıtlar belirlenir; bekleyen klinik bilgi
   kararları kaynaklara aktarılıp yeni ayrı build/test paketi alınır.
2. Eski çalışan release, DNS/TTL ve platform kural snapshot'ları korunur.
3. Staging'de bütün kritik kabul ve form teslim yetkisi tamamlanır. Telefon/
   WhatsApp linkine tıklama mesaj/gerçek randevu veya teslim sayılmaz.
4. Yayın yetkisi ayrı verildiğinde doğrulanmış public release atomik aktive
   edilir; DNS/hesaplarda izinsiz işlem yapılmaz. --gc/canlı klasör temizliği yok.
5. Health/HTTP/telemetry kabulü başarısızsa önceki doğrulanmış release'e atomik
   geri dönüş; eski sistem teslim teyidi olmadan kapatılmaz. Bu tatbikat yapılmadı.

GSC baseline: 8konu kümesi+brand/non-brand, sayfa/cihaz/ülke; eşlenebilir dönem
ve kesinti boşlukları. Organik sonuç, harita görünürlüğü ve gerçek iletişim
ayrı ölçülür. Hasta adı/iletişim/sağlık metni analytics event'e aktarılmaz.
Sıralama/CTR/traffic artışı veya ceza nedeni bu veriler olmadan ilan edilmez.
'''
(OUT/'06-launch-readiness.md').write_text(launch)

schema_note=f'''\n## Nihai birleşik release doğrulaması\n\nRoot'un `{PUBLIC}` çıktısı: **{schema['counts']['html']} HTML / {schema['counts']['scripts']} script**, hedefli yerel hata **0**. Önceki ara smoke685script kaydı farklı render snapshot'ıdır; nihai sayım673'tür. Resmî Validator/RRT, klinik gerçeklik ve gerçek image HTTP kabulü yeni çalıştırılmadı. Kanıt: `evidence/schema-after-final.json` ve `final-build-manifest.json`.\n'''
p=OUT/'04-schema-validation.md';s=p.read_text();s+=schema_note if '## Nihai birleşik release doğrulaması' not in s else '';p.write_text(s)
p=OUT/'05-performance-before-after.md';s=p.read_text();s+='''\n## Root nihai paket notu\n\nYeni ayrı minify release exit0; nihai varlık karşılaştırması performance-before-after-assets.json içindedir. Runtime süreleri null'dır. CUA1314fetch101605bayt SHA5443e2…9b5a8 frozen baseline ile eş; bu bir hız koşusu değildir. Ölçüm kurulum çağrısı kernel reset nedeniyle çalışmadı, ardından bağlantı timeout oldu. Yeni üretim server1315 bind Operation not permitted; kısıt aşılmadı. Yeni CPU/network/viewport ölçüm profili uygulanmadı. Üretim3+3cold/warm,Lighthouse,trace,A-B,GPU ve gerçek native200 sonuçları NOT_RUN kalır. Kullanıcı isteğinden önce import/model başlamaması kaynak/Node-startup testidir; gerçek after network waterfall sonucu değildir.\n''' if '## Root nihai paket notu' not in s else '';p.write_text(s)
print(json.dumps({'reports_written':True,'findings':len(audit_rows),'keywords':len(keywords),'percent_lines_preserved':sum(x['after_percent_lines'] for x in clinical),'statuses':dict(collections.Counter(status(r['ID']) for r in audit_rows))},ensure_ascii=False))
