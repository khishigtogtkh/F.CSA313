# Lab08 хэрэгжүүлэлтийн төлөв ба шалгах жагсаалт

2026-11-03-нд DOCX заавар болон баталсан төлөвлөгөөний дагуу локал хэрэгжүүлэлт хийв. Оюутан: С.Хишигтогтох, B232270806. Хэрэглэгчийн дараагийн хүсэлтээр Lab08-ийн commit-уудыг main руу fast-forward нэгтгэж, origin/main руу нийтэлсэн. GitHub репо public болох нь батлагдсан; Teams Assignment-ийн due date болон Turn in нь тусдаа үлдсэн.

## Дууссан үе шатууд

- [x] Java 17, Maven 3.9.10 болон тестгүй starter-ийн BUILD SUCCESS-ийг шалгасан.
- [x] `codex/lab08-mockito` салбар, лабораторийн ignore, compiler plugin 3.13.0 болон starter commit.
- [x] A1–A8: 7 энгийн тест + 3 параметрийн мөр; 10/0/0/0, BUILD SUCCESS.
- [x] Гурван мутантыг нэг нэгээр нь ажиллуулсан; failures 2, 2, 1; errors бүгд 0; гурвуулаа BUILD FAILURE.
- [x] Мутаци бүрийн дараа service-ийг сэргээсэн; src/main starter commit e3c9921-ээс өөрчлөгдөөгүй.
- [x] Өөр AI хувилбар: 12/0/0/0; гурван мутантын failures 1, 3, 1; errors бүгд 0.
- [x] Prompt, AI оролцооны тайлбар, бүх бодит гаралт болон README дүгнэлтүүд.
- [x] Репогийн үндсэн .github/workflows/test.yml болон бодит badge URL локалд бэлтгэсэн.
- [x] Үе шат тус бүрийн бодит локал commit-ууд.
- [x] Локал репогоос тусдаа цэвэр clone хийсэн: 10/0/0/0, BUILD SUCCESS; бүх шаардлагатай файл ирсэн, target эхэнд байгаагүй.

## Шалгах гол нотолгоо

Үндсэн README: starter/README.md. Ногоон гаралт: starter/results/mvn-test.txt. Үндсэн мутацууд: starter/results/mvn-test-mutant-1.txt, mvn-test-mutant-2.txt, mvn-test-mutant-3.txt. AI гаралтууд: starter/results/ai-comparison/. Java/Maven орчин: starter/results/environment.txt. Мутацийг давтах: starter дотроос `bash scripts/run-mutations.sh main` эсвэл `bash scripts/run-mutations.sh ai`.

Цэвэр clone-ийн нотолгоо: starter/results/mvn-test-clean-clone.txt; шалгасан commit `2aea6faa16b1215cb04463d03a833af2e110bcc4`.

## GitHub нийтлэлт ба үлдсэн илгээлт

- [x] Public GitHub репогийн main салбарт push хийсэн.
- [x] Үүлэн CI completed/success; run 41646754658. Нотолгоо: starter/results/github-actions.json.
- [x] GitHub main-аас цэвэр clone: 10/0/0/0, BUILD SUCCESS. Нотолгоо: starter/results/mvn-test-github-clone.txt.
- [ ] Assignment-ийн due date-ээс өмнө GitHub линк хавсаргаж Turn in дарах, илгээгдсэн төлөвийг батлах.

Teams Turn in батлагдаагүй тул лабораторийг бүрэн илгээсэн гэж тэмдэглэхгүй. Өөрчлөлт зөвхөн lab08 болон уг лабораторийн CI workflow-д хамаарна.
