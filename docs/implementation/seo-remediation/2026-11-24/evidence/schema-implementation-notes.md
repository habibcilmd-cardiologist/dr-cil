# Schema uygulama notları

Kapsam: SCH-01–10 / B06,B12. 7 schema/breadcrumb/data kaynağı ve
scripts/validate_schema_output.py uygulandı. Tema altmodülü değişmedi.
Klinik metin, DNS/hesap/form gönderimi ve deploy yapılmadı.

Tam değişiklik/kabul raporu: ../04-schema-validation.md.

Ara smoke build exit0; whole-output schema checker exit0. Nihai birleşik
root build ayrıca aynı checker'dan geçmeli. Clinic/gerçek saatler/review ve
ayrıntılı klinik harita dış veri bekler; teknik düzelme tam klinik kabul değildir.

Resmî validator testleri NOT_RUN. `python -m py_compile` ilk denemesi hostun
varsayılan pycache yazım izninde başarısız oldu; kaynak metni Python compile()
ile bellekte ayrıştırıldı ve gerçek CLI baseline/after çalıştırıldı. İzin
kısıtını aşacak işlem yapılmadı. Baseline çıktısı scriptin policy kodunun
adı okunaklılaştırılmadan önce kaydedildi; `PERSON_OFFICE_CONFLATED` etiketi
bir Schema.org geçersizlik hükmü değildir, ayrık kişi/ofis kabul politikasıdır.
