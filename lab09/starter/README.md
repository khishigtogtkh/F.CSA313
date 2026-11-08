# Лаборатори 09 — JaCoCo

Нэр: С.Хишигтогтох  
Оюутны код: B232270806

## Орчин

```text
openjdk version "17.0.20.1" 2026-08-18
OpenJDK Runtime Environment (build 17.0.20.1+1-1-24.04-Ubuntu)
OpenJDK 64-Bit Server VM (build 17.0.20.1+1-1-24.04-Ubuntu, mixed mode, sharing)
Apache Maven 3.9.10 (5f519b97e944483d878815739f519b2eade0a91d)
Maven home: /mnt/c/Program Files/apache-maven-3.9.10
Java version: 17.0.20.1, vendor: Ubuntu, runtime: /usr/lib/jvm/java-17-openjdk-amd64
Default locale: en, platform encoding: UTF-8
OS name: "linux", version: "6.18.54.1-microsoft-standard-wsl2", arch: "amd64", family: "unix"
```

## Ажиллуулах

Репогийн root-оос `mvn -f lab09/starter/pom.xml verify`, эсвэл энэ хавтаснаас `mvn verify`.
HTML: `target/site/jacoco/index.html`. Java 17+, Maven, анхны dependency таталтад интернэт шаардлагатай.

## A — Happy path

5 тест. Line 60.00%, Branch 48.78%.
Хувь = covered / (missed + covered) × 100; хоёр орны нарийвчлалаар дугуйруулав.
[Лог](results/mvn-verify-A.txt), [CSV](results/jacoco-A.csv).
Хэвийн оролтын тестүүд A/B дүн, голч болон 100/70 хувийн тэтгэлгийн замыг дайрсан.
Оноо, голч, кредитийн шалгалтын exception мөрүүд хүрээгүй; эдгээрийн шалгах нөхцөлүүд дутуу салаатай.
Үлдсэн үсгэн дүн, switch case/default болон зөрчил, 50/0 хувийн тэтгэлгийн замуудыг B хэсэгт нөхнө.

## AI ашиглалт

Codex-ийг төлөвлөгөө, тест, хэмжилт, тайлбарын тусламжид ашигласан. Үр дүн нь бодит Maven ажиллуулалтын гаралт.

## B — CFG ба бүрэн хамралт

20 тест ажилласан: [лог](results/mvn-verify-B.txt), [CSV](results/jacoco-B.csv).
Line 25/25 = 100%, Branch 41/41 = 100%; LINE_MISSED=0, BRANCH_MISSED=0.
Гурван хүчингүй scholarship оролт тусдаа assertThrows тесттэй; AND нөхцөлүүдийн кредит хүрэхгүй зам, gpa switch-ийн F default хамрагдсан.

![CFG лавлах](cfg.png)

**CFG төлөв:** энэ зураг AI-аар кодоос үүсгэсэн лавлах бөгөөд зааврын «гараар зурсан» шаардлага одоогоор хангагдаагүй.
Оюутан draw.io эсвэл цаасан дээр гараар дахин зурж энэ зургийг солих шаардлагатай.
[Ирмэг–тестийн бүрэн жагсаалт](cfg-edges.json) дахь E1–E25 нэршил, true/false чиглэлийг ашиглан Лекц 9-ийн хэв маягтай тулгана.

## C — Давталтын зааг

22 тест ногоон: [лог](results/mvn-verify-C.txt), [CSV](results/jacoco-C.csv).
0 ангилал: `gpaRejectsNullScores`, `gpaRejectsEmptyScores` тус бүр assertThrows ашиглана.
1 ангилал: `gpaHandlesSingleScore` нь [95] → 4.0.
2+ ангилал: `gpaHandlesMultipleScores` нь [95,85,75,65] → 2.5.
Хамралт 100% байсан ч энэ нь давталтын бүх уртад тооцоо зөв гэдгийг батлахгүй.
Эдгээр тест хоосон оролтын гэрээ, нэг элементийн тооцоо, олон элементийн хуримтлал ба хуваалтыг тус тус шалгадаг учраас хэрэгтэй.

## D — Зааг утгын алдаа

[Унасан лог](results/mvn-test-D-fail.txt): 29 тестээс 1 унасан.

```text
ScholarshipCalculatorTest.letterGradeReturnsDAt60:31 expected: <D> but was: <F>
```

Тусдаа [засварын commit: 155cff1](https://github.com/khishigtogtkh/F.CSA313/commit/155cff1) нь `score > 60` нөхцөлийг `score >= 60` болгосон.
[Эцсийн лог](results/mvn-verify-final.txt): Tests run: 29, Failures: 0, Errors: 0, Skipped: 0; BUILD SUCCESS.
[Эцсийн CSV](results/jacoco-final.csv): Line 25/25 = 100%, Branch 41/41 = 100%; LINE_MISSED=0, BRANCH_MISSED=0.

### Гол дүгнэлт

B хэсгийн тестүүд бүх салааг дайрсан боловч яг 60 онооны хүлээгдэх үр дүнг шалгаагүй.
`score > 60` ба `score >= 60` нь ижил салааны бүтэцтэй тул branch хамралт дангаараа энэ ялгааг харуулахгүй.
Зааг утгын тест спецификацийн 60 оноо D байх дүрэмтэй үр дүнг харьцуулж алдааг илрүүлсэн.
JaCoCo нь тест ажиллахад кодын ямар мөр, салаа гүйцэтгэгдсэнийг хэмждэг.
Хамралт нь бүх оролтод тооцоо зөв, эсвэл спецификаци бүрэн биелснийг батлахгүй.
Иймээс бүтцийн хамралтыг зааг утгын болон хүлээгдэх үр дүнг шалгах тестүүдтэй хослуулах хэрэгтэй.

## Нотолгоо ба илгээлтийн төлөв

A → B → C → D-fail → D-fix нь тусдаа бодит commit-уудтай.
[Тестгүй starter-ийн тусгаарласан давтан шалгалт](results/mvn-verify-starter.txt) нь A үеийн commit-ийн pom/source-ийг тестгүй түр хавтаст хуулж дараа нь ажиллуулсан; анхны run гэж мэдүүлээгүй.
CFG нь AI-аар үүсгэсэн лавлах хэвээр; гараар дахин зурах шаардлага үлдсэн.
Teams-ийн Lab09 due date болон Turn in төлөвийг энэ орчноос баталгаажуулаагүй.
AI нь CFG лавлах зураг, ирмэгийн жагсаалт, README болон Git ажлын тусламжид мөн ашиглагдсан.
Нэмэлт coverage gate, Lab09 CI, AI харьцуулалт хийгээгүй. Одоо байгаа GitHub Actions нь Lab08-ыг шалгадаг.

### Цэвэр clone ба GitHub байршуулалт

Локал репогийн `056c626` commit-ийг шинэ хавтсанд `git clone --no-local` хийж, `mvn verify` ажиллуулахад 29 тест ногоон, final CSV яг ижил гарсан: [лог](results/mvn-verify-local-clone.txt).
Энэ нь GitHub remote-оос хийсэн шалгалт биш.
GitHub main руу push хийх оролдлого `could not read Username for 'https://github.com'` алдаагаар зогссон тул шинэ commit-ууд локалд байна.
Нэвтрэлтийг тохируулсны дараа push, remote clone шалгалт, гараар зурсан CFG, Teams Turn in-г дуусгах шаардлагатай.
