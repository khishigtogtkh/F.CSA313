# BUG-06: Буруу JSON бүхий POST хүсэлт HTTP 400 биш HTTP 200 буцааж байна

Орчин: Уншлагын жагсаалт v2.0; хэрэгсэл: curl 8.5.0 (HTTP хүсэлт, браузер шаардахгүй); Node.js v22.23.2; үйлдлийн систем: Ubuntu 24.04.3 LTS / WSL2, Linux 6.18.54.1-microsoft-standard-WSL2; дахин шалгасан огноо: 2026-10-25 (UTC+08:00).
Урьдчилсан нөхцөл: `node app.js`-ийг зогсоож шинээр асаасан, анхны 3 номтой төлөв.

## Дахин гаргах алхам

1. `node app.js`-ийг шинээр асааж ажиллуул.
2. Өөр Terminal дээр доорх командыг ажиллуул. Оролтын бие нь яг `not-json` гэсэн 8 тэмдэгт.

   ```bash
   curl -sS -i -X POST http://localhost:3000/api/books \
     -H 'Content-Type: application/json' -d 'not-json' \
     > evidence/api-invalid-json.txt
   ```
3. `cat evidence/api-invalid-json.txt` ажиллуулж хадгалсан бүтэн хариуны HTTP статус мөр болон JSON биеийг шалга.

**Хүлээгдэж байсан:** Буруу JSON биетэй POST хүсэлтэд `HTTP/1.1 400 Bad Request` хариу ирнэ.

**Бодит үр дүн:** Шинэ хүсэлтийн хариу `HTTP/1.1 200 OK`, `{"result":"OK"}` байв. HTTP `Date`: `Sun, 25 Oct 2026 14:29:27 GMT` (Улаанбаатарын 22:29:27). Дараах GET хүсэлтээр анхны 3 ном хэвээр байсныг шалгасан; буруу JSON-ийг амжилттай гэж мэдээлж байна.

**Ноцтой байдал:** Major — Хүчингүй хүсэлтийг амжилттай гэж мэдээлснээр API хэрэглэгч төөрөгдөнө.

**Түүхий тэмдэглэл:** [session-events.jsonl](../evidence/session-events.jsonl) — тухайн шалгалтын цаг, оролт, DOM үр дүн.

**Хавсралт:** `evidence/api-invalid-json.txt`

**Олдсон аялал:** Saboteur (API)
