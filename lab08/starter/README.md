# Лаборатори 08 Mockito mock объектууд

**Оюутны нэр:** С.Хишигтогтох

**Оюутны код:** B232270806

**Хичээл:** F.CSA313 — Программ хангамжийн чанарын баталгаа ба тест

**Шалгасан огноо:** 2026-11-03, Asia/Ulaanbaatar (UTC+08:00)

## Орчин

`java -version` болон `mvn -version` командын бодит гаралт ([эх файл](results/environment.txt)):

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

Java release 17, JUnit Jupiter 5.10.2, Mockito Jupiter 5.11.0, Maven Compiler 3.13.0, Surefire 3.2.5 ашигласан. Сан, SMTP сервер ажиллуулах шаардлагагүй: `StudentRepository`, `EmailSender` хоёрыг mock-оор орлуулсан бөгөөд `Student`, жагсаалтууд, тестлэж буй service нь бодит объектууд.

## Ажиллуулах

Локал төслөөс WSL2 Ubuntu орчинд:

```bash
cd /home/hishigtogtokh/F.CSA313/lab08/starter
mvn test
```

GitHub-ийн main салбарыг өөр хавтаст татах:

```bash
git clone --branch main https://github.com/khishigtogtkh/F.CSA313.git
cd F.CSA313/lab08/starter
mvn test
```

Maven төсөл репогийн үндсэн хавтаст биш, `lab08/starter` дотор байдаг. Репогийн үндсэн хавтсаас мөн `mvn -B -f lab08/starter/pom.xml test` гэж ажиллуулж болно. Эхний удаа Maven Central-аас dependency татах интернэт хэрэгтэй.

```text
F.CSA313/
├── .github/workflows/test.yml
└── lab08/
    ├── .gitignore
    ├── IMPLEMENTATION_PLAN.md
    └── starter/
        ├── pom.xml
        ├── README.md
        ├── src/main/java/mn/edu/must/sqat/        # анхны дөрвөн Java файл
        ├── src/test/java/mn/edu/must/sqat/
        │   ├── CourseRegistrationServiceTest.java
        │   └── CourseRegistrationServiceAiComparison.java
        ├── scripts/run-mutations.sh
        ├── ai-comparison/prompt.md
        └── results/
            ├── environment.txt
            ├── mvn-test.txt
            ├── mvn-test-clean-clone.txt
            ├── mvn-test-mutant-1.txt
            ├── mvn-test-mutant-2.txt
            ├── mvn-test-mutant-3.txt
            └── ai-comparison/
                ├── mvn-test.txt
                ├── mvn-test-mutant-1.txt
                ├── mvn-test-mutant-2.txt
                └── mvn-test-mutant-3.txt
```

`target/`, IDE/build туслах файлууд, зааврын DOCX, `__MACOSX/`, `Zone.Identifier` нь Git-д ороогүй. Локал зааврын DOCX-ийг устгаагүй.

## Хэсэг A найман тест

Үндсэн [тестийн класс](src/test/java/mn/edu/must/sqat/CourseRegistrationServiceTest.java) нь `MockitoExtension`, хоёр `@Mock`, `@BeforeEach` constructor injection ашиглана. Нэр бүр `register_нөхцөл_үрДүн` хэв маягтай; matcher ашигласан дуудалтад бүх аргумент matcher байна.

| ID | Шалгасан зан төлөв | Гол хэрэгсэл |
|---|---|---|
| A1 | Идэвхтэй, prerequisite хангагдсан оюутан `OK`; зөв аргументтай хадгалалт ба и-мэйл нэг удаа | `when/thenReturn`, `verify` |
| A2 | Оюутан байхгүй → `ERROR_NO_STUDENT`; хадгалалт, и-мэйл байхгүй | `never()` |
| A3 | Идэвхгүй → `ERROR_INACTIVE_STUDENT`; хадгалалтгүй, и-мэйлтэй огт харьцаагүй | `verifyNoInteractions` |
| A4 | Хоёр prerequisite-ийн нэг нь дутуу → `ERROR_PREREQUISITES`; хадгалалт, и-мэйл байхгүй | `when`, `never()` |
| A5 | И-мэйл `RuntimeException` шидсэн ч `OK`; хадгалалт болон илгээх оролдлого хийгдсэн | `doThrow` |
| A6 | `(null, validCourseId)`, `(validStudentId, null)` тус бүр exception; хамаарлуудтай харьцаагүй | Хоёр `assertThrows` |
| A7 | Илгээгдсэн и-мэйлийн body дотор courseId байгаа | `ArgumentCaptor<String>` |
| A8 | `missing`, `inactive`, `missingCourse` гэсэн гурван мөр зөв алдааны код буцааж, хадгалалт/и-мэйл хийхгүй | `@ParameterizedTest`, `@CsvSource` |

**Тестийн тоо: 10 = 7 энгийн тест + A8-ийн 3 мөр.** Эцсийн [бодит гаралт](results/mvn-test.txt):

```text
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

A8-д `courseExists`-ийн нийтлэг stub нь `missing`, `inactive` мөрүүдийн эрт буцах замд ашиглагддаггүй тул зөвхөн тэр stub-д `lenient()` хэрэглэсэн. Бусад stub болон тестүүдийн strict горимыг хадгалсан; бүх классад lenient strictness тавиагүй.

Гаралтыг хадгалсан команд:

```bash
mkdir -p results
set -o pipefail
mvn -B --no-transfer-progress test 2>&1 | tee results/mvn-test.txt
```

## Хэсэг B гурван мутаци

[Давтагдах скрипт](scripts/run-mutations.sh) нэг удаад нэг эвдрэл оруулж, `clean test` ажиллуулаад эх кодыг сэргээнэ. `pipefail` болон `PIPESTATUS` нь Maven/tee-ийн алдааг шалгана; `EXIT`, `INT`, `TERM` trap нь команд амжилтгүй болсон үед ч эх файлыг сэргээнэ. Эх хувилбарын суурь тестийг эхэнд, сэргээсэн хувилбарын тестийг төгсгөлд ажиллуулдаг.

```bash
bash scripts/run-mutations.sh main
```

Доорх нь төлөвлөсөн бус, бодитоор гарсан үр дүн. Бүх мутантад 10 тест ажиллаж, `Errors: 0`, `Skipped: 0`, `BUILD FAILURE` гарсан.

| Мутант ба эвдрэл | Бодитоор унасан тестүүд | Failures / Errors | Алдааны төрөл | Нотолгоо |
|---|---|---|---|---|
| 1 — идэвхгүй оюутны шалгалтыг хассан | A3 `register_inactiveStudent_returnsInactiveWithoutSavingOrEmail`; A8 `register_invalidState_returnsExpectedError(String, boolean, String)[2]` буюу inactive мөр | 2 / 0 | `AssertionFailedError`: хүлээсэн `ERROR_INACTIVE_STUDENT`-ийн оронд тус тус `ERROR_NO_COURSE`, `OK` | [мутант 1](results/mvn-test-mutant-1.txt) |
| 2 — `saveRegistration` дуудалтыг хассан | A1 `register_activeStudent_returnsOkAndSavesAndSendsEmail`; A5 `register_emailFailure_returnsOkAndKeepsRegistration` | 2 / 0 | Mockito `WantedButNotInvoked`: хадгалалт дуудагдаагүй | [мутант 2](results/mvn-test-mutant-2.txt) |
| 3 — `courseId == null` хамгаалалтыг хассан | A6 `register_eitherIdNull_throwsWithoutDependencyInteractions` | 1 / 0 | `AssertionFailedError`: courseId-null оролтод `IllegalArgumentException` шидээгүй | [мутант 3](results/mvn-test-mutant-3.txt) |

Гурван эвдрэл бүгд баригдсан тул зөвхөн буцах утга бус хадгалалтын side effect, тусдаа null хамгаалалт ч шалгагдаж байна. A6-г анхнаас нь хоёр аргументын null-ийг тус тус шалгадаг бичсэн учраас мутант 3-ын дараа нөхөж засварлах шаардлага гараагүй. Энэ гүйлтэд `UnnecessaryStubbingException` гараагүй; таван уналт бүгд assertion эсвэл verification failure байсан. Гурван мутантын дараа `src/main` нь starter commit `e3c9921`-тэй diff-гүй, эцсийн үндсэн тест 10/10 ногоон.

## Нэмэлт AI харьцуулалт

Хоёр suite-ийг нэг Codex туслахын оролцоотой бэлтгэсэн; оюутан дангаараа бичсэн тест эсвэл хараат бус AI session гэж тайлагнахгүй. [Prompt болон service-ийн оролт](ai-comparison/prompt.md), [өөр хувилбарын эх код](src/test/java/mn/edu/must/sqat/CourseRegistrationServiceAiComparison.java), бодит гаралтуудыг хадгалсан.

```bash
mvn -B --no-transfer-progress -Dtest=CourseRegistrationServiceAiComparison test
bash scripts/run-mutations.sh ai
```

`CourseRegistrationServiceAiComparison` нэр нь Surefire-ийн анхдагч `Test*`, `*Test`, `*Tests`, `*TestCase` загварт таарахгүй тул ердийн `mvn test`-д ажиллахгүй. Тусдаа сонгож ажиллуулахад **12 тест**, үндсэн suite-д **10 тест** байна.

| Гүйлт | Үндсэн suite | Өөр AI хувилбар | AI нотолгоо |
|---|---|---|---|
| Эх код | 10 / 0 / 0 / 0, `BUILD SUCCESS` | 12 / 0 / 0 / 0, `BUILD SUCCESS` | [суурь](results/ai-comparison/mvn-test.txt) |
| Мутант 1 | 2 failure, 0 error | 1 failure, 0 error: `register_inactiveStudent_rejectsWithoutSavingOrEmail` | [мутант 1](results/ai-comparison/mvn-test-mutant-1.txt) |
| Мутант 2 | 2 failure, 0 error | 3 failure, 0 error: `register_eligibleStudent_savesAndSendsCourseNotification`, `register_noPrerequisites_acceptsStudentWithNoCompletedCourses`, `register_smtpFailure_returnsOkAfterSaving` | [мутант 2](results/ai-comparison/mvn-test-mutant-2.txt) |
| Мутант 3 | 1 failure, 0 error | 1 failure, 0 error: `register_nullCourseId_throwsBeforeUsingDependencies` | [мутант 3](results/ai-comparison/mvn-test-mutant-3.txt) |

AI-ийн гурван мутантын файл тус бүр `BUILD FAILURE`; алдааны төрлүүд нь үндсэн suite-тэй адил mutant 1/3-д `AssertionFailedError`, mutant 2-д `WantedButNotInvoked`.

### AI харьцуулалтын дүгнэлт

Үндсэн A1–A8 suite 10 гүйцэтгэлтэй, харьцуулалтын AI хувилбар 12 тусдаа энгийн тесттэй бөгөөд хоёр хувилбар хоёулаа гурван мутантыг барьсан. Өөр хувилбар нь хоёул null байх, prerequisite-гүй хичээл, repository-ийн жагсаалтыг өөрчлөхгүй байх, repository-ийн exception-ийг дамжуулах тохиолдлуудыг нэмж шалгасан. Үндсэн хувилбарын A1 нь immutable prerequisite жагсаалт ашигладаг тул түүнийг шууд өөрчлөх эвдрэлийг мөн илрүүлэх боломжтой боловч тусдаа state assertion агуулаагүй. Өөр хувилбар нь и-мэйлийн body-г `argThat`-аар шалгасан ч лабораторийн шаардсан `ArgumentCaptor`, параметржүүлсэн A8-ийг ашиглаагүй тул үндсэн suite-ийг шууд орлохгүй. Хадгалалтыг `verify`-аар, үр дүнг `assertEquals`-ээр, null хамгаалалтыг `assertThrows`-оор шалгасан тул шалгалтгүйгээр зөвхөн дуудагддаг сул тест байхгүй. Харин жагсаалтын өөрчлөлтийн тест дангаараа хадгалалтын эвдрэлийг барихгүй тул нэг тестээр бүх side effect-ийг баталсан гэж үзэхгүй. Энэ харьцуулалт нэг AI туслахтай нэг чатанд хийгдсэн учраас хараат бус загваруудын чанарын хэмжилт биш бөгөөд зөвхөн хадгалсан хоёр тестийн хувилбарын бодит үр дүнг харуулна.

## Нэмэлт CI

[![Lab08 Mockito tests](https://github.com/khishigtogtkh/F.CSA313/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/khishigtogtkh/F.CSA313/actions/workflows/test.yml?query=branch%3Amain)

[Workflow](../../.github/workflows/test.yml) нь push, pull request, workflow_dispatch үйл явдлаар Ubuntu, Temurin Java 17 орчинд үндсэн 10 тестийг ажиллуулна. Maven cache нь лабораторийн POM-оор түлхүүрлэгдэнэ; workflow зөвхөн `contents: read` эрхтэй.

**CI төлөв:** workflow main салбарт бэлэн; энэ нийтлэлтийн Actions үүлэн гүйлт болон ногоон badge хараахан батлагдаагүй. Дээрх badge нь бодит workflow-ийн хаяг бөгөөд хиймэл ногоон зураг биш. AI-ийн улаан мутацийн гүйлтийг CI-ийн ногоон үндсэн тесттэй хольж ажиллуулахгүй.

## Нэгтгэсэн дүгнэлт

Mockito mock нь хамаарлын хариуг тохируулж, дуудалтыг шалгах хэрэгсэл бол гараар бичсэн fake нь тухайн интерфейсийн хялбар боловч ажилладаг хэрэгжүүлэлт юм. Энэ лабораторид сан болон и-мэйл илгээгчийг mock болгосноор сүлжээ, өгөгдлийн сангийн төлөвөөс үл хамаарах нэгжийн тест бичсэн. `Student` record, энгийн утга, жагсаалтууд болон тестлэж буй `CourseRegistrationService`-ийг mock хийхгүй, бодит объект ашигласан. Буцах кодыг assertion-оор, хадгалалт болон и-мэйлийн зайлшгүй side effect-ийг `verify`-аар баталсан. Хэт олон дотоод дуудалт, дарааллыг `verify`-аар түгжвэл ижил зан төлөвтэй refactor хийхэд тест хэрэггүйгээр унах эрсдэлтэй. Гурван мутацийн бодит уналт нь идэвхтэй байдлын дүрэм, хадгалалт, courseId-null хамгаалалтыг тестүүд шалгаж байгааг харуулсан. Мутаци бүрийн дараа эх кодыг сэргээж эцсийн 10 тестийг дахин ногоон ажиллуулсан ч гурван мутант барьсан нь бүх боломжит согоггүйг батлахгүй.

## Локал цэвэр clone-ийн шалгалт

[Бодит гаралт](results/mvn-test-clean-clone.txt)-д локал репогоос `--no-local` сонголттой тусдаа `/tmp` хавтаст clone хийсэн commit, байрлал, файлын бүрдэл болон `mvn test`-ийн гаралт байна. Шалгасан commit: `2aea6faa16b1215cb04463d03a833af2e110bcc4`; build хийхээс өмнө `target` байхгүй, зааврын DOCX/IDE/build файлууд бүртгэгдээгүй, бүх тест ба найман үндсэн/AI нотолгооны файл ирсэн. Цэвэр clone дээр энгийн `mvn test` нь `Tests run: 10, Failures: 0, Errors: 0, Skipped: 0`, `BUILD SUCCESS` болсон. Энэ нь локал clone-ийн баталгаа бөгөөд GitHub-ээс clone хийсэн шалгалтыг орлохгүй.

## Git түүх ба илгээлт

Starter, A1–A8, үндсэн мутаци, AI харьцуулалт, README/CI гэсэн үе шатуудыг дуусах бүрд тусдаа локал commit хийсэн. `git log --oneline -- lab08 .github/workflows/test.yml` командаар бодит дарааллыг харж болно. Эвдэрсэн service хувилбаруудыг commit хийгээгүй.

GitHub репо public, default branch нь main болохыг GitHub API-аар баталсан. Lab08-ийн үе шатны commit-уудыг main руу fast-forward нэгтгэсэн; нийтлэлт болон үүлэн CI-г дараагийн шалгалтаар батална. Assignment-ийн due date-ийг шалгаагүй, Teams илгээлт хийгээгүй.

Илгээхэд үлдсэн алхмууд:

1. GitHub репо public байгааг шалгаад `git push origin main` ажиллуулах.
2. Actions-ийн ногоон гүйлт болон badge-ийг шалгах.
3. GitHub-ээс өөр цэвэр хавтаст clone хийж `lab08/starter` дотроос `mvn test` ажиллуулах.
4. Teams Assignment-д public репогийн холбоос хавсаргаж, `lab08/starter` байршлыг тодруулан due date-ээс өмнө **Turn in** дарах.
5. Teams дээр илгээгдсэн төлөвийг шалгах; архив, screenshot нь шаардсан текстэн нотолгоо болон Turn in-ийг орлохгүй.
