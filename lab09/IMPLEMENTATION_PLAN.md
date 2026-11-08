# Лаборатори №9 — хэрэгжүүлэх төлөвлөгөө ба бодит төлөв

Эх сурвалж: Lab09 - Код хамралт JaCoCo (2026).docx, starter код, багшийн Лаб08/09 сануулга.
Хэрэглэгчийн сонголт: одоогийн F.CSA313 репо, зөвхөн үндсэн шаардлага; нэмэлт coverage gate/CI/AI харьцуулалтгүй.

## Бүтэц ба бэлтгэл

Maven төсөл lab09/starter дотор. Root-оос `mvn -f lab09/starter/pom.xml verify` ажиллуулна.
Java release 17, compiler 3.13.0, JUnit 5.10.2, Surefire 3.2.5, JaCoCo 0.8.12.
Lab09-ийн .gitignore нь target, IDE/OS, DOCX, __MACOSX, Zone.Identifier файлуудыг хасна.
Бусад лаборатори, Lab08 CI-г өөрчлөхгүй. Нэр/код: С.Хишигтогтох / B232270806.

## A → B → C → D

- [x] A: 5 happy-path тест; letterGrade 95/85, gpa [95,85], scholarship 100/70. Production засваргүй.
- [x] A: бодит лог/CSV, Line 60%, Branch 48.78%; README ажиглалт 2–3 өгүүлбэр.
- [x] B: нийт 20 тест; C/D/F, хүчингүй оноо, null/empty, switch default, scholarship-ийн гурван OR exception, AND кредит false зам, зөрчил ба 0 тэтгэлэг.
- [x] B: Line 25/25, Branch 41/41; хоёр MISSED=0. CSV ба Maven тоонууд таарсан.
- [x] CFG лавлах: short-circuit шийдвэрүүд, E1–E25 ирмэг, бодит тестийн нэрүүд; JSON mapping.
- [ ] Оюутан CFG-г Лекц9-ийн хэв маягаар гараар зурж cfg.png-г солих. AI-аар үүсгэсэн лавлах нь энэ шаардлагыг хангахгүй.
- [x] C: null/empty assertThrows дахин ашиглаж, [95]→4.0 болон [95,85,75,65]→2.5 нэмсэн. Нийт 22 тест ногоон; README 2 өгүүлбэр тайлбар.
- [x] D: 60,59.99,69.99,0,100,89.99,90 заагийн 7 тест нэмсэн. Нийт 29-өөс letterGradeReturnsDAt60 унасан; expected D / actual F лог хадгалсан.
- [x] D: унасан тестийн тусдаа commit, дараа нь >60 → >=60 засварын тусдаа commit.
- [x] Final: 29 тест ногоон; Line/Branch 100%; гол дүгнэлт 6 өгүүлбэр, засварын commit холбоос.

## README ба нотолгоо

- [x] Бодит нэр/код, java -version болон mvn -version бүтэн гаралт, ажиллуулах команд.
- [x] A/B/final тус бүрийн mvn-verify лог ба jacoco CSV, D-fail лог — заавал шаардах 7 файл UTF-8.
- [x] README-ийн хувь, тоо, тестийн нэр, assertion, commit холбоосыг бодит файлтай тулгасан.
- [x] AI ашигласан хүрээ болон CFG-ийн дутуу шаардлагыг ил тод тэмдэглэсэн.
- [x] A, B, C, D-fail, D-fix тусдаа бодит commit; утгатай message, огноо өөрчлөөгүй.
- [x] Тестгүй starter-ийн тусгаарласан давтан шалгалт: тайлан үүсэхгүй гэсэн хэвийн гаралт. Энэ нь A-ийн дараа хийсэн шалгалт гэдгийг README тайлбарласан.

## Илгээлтийн хаалга

- [x] GitHub default branch нь main гэдгийг remote-оос шалгасан.
- [x] Локал цэвэр clone-оос mvn verify; тайлан ба тестийн тоо final нотолгоотой таарсан.
- [ ] GitHub push: HTTPS credential байхгүй тул оролдлого амжилтгүй; локал commit-ууд remote-д хараахан ороогүй.
- [ ] Push-ийн дараа public remote-оос шинэ clone татаж mvn verify дахин ажиллуулах, results ба default branch-ийн бүрэн ажлыг шалгах.
- [ ] Teams Lab09-ийн due date-ийг шалгах; Lab08-ын хугацааг ашиглахгүй.
- [ ] Архив биш репогийн root URL-ийг Teams Assignment-д хавсаргаж хугацаанд нь Turn in дарах, илгээсэн төлөвийг шалгах.

Бүрэн тэнцэхэд гараар зурсан CFG, GitHub байршуулалт/remote clone болон Teams илгээлтийн нотолгоо үлдсэн.
