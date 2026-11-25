# Лаборатори №10. Өгөгдлийн урсгалын тест

Нэр: С.Хишигтогтох  
Оюутны код: B232270806

## Зорилго

Энэ лабораторид `gcd` болон `bonus` функцийн хувьсагч бүрийн утга хаана оноогдож, хаана ашиглагдаж байгааг эх кодын мөрөөр судлав. `bonus` функцэд эхлээд оноолт бүрийг дор хаяж нэг хэрэглээнд хүргэх all-defs багц, дараа нь боломжтой DU хос бүрийг хамрах all-DU-pairs багц ашиглав. Тестийн хамралт бодит алдааг илрүүлэхэд хэр хүрэлцэхийг гурван мутациар шалгав.

## Орчин

`results/` дэх анхны туршилтуудыг доорх Java болон Maven хувилбараар ажиллуулсан.

```text
openjdk version "17.0.21.0.3" 2026-10-24
OpenJDK Runtime Environment (build 17.0.21.0.3+1-1-24.04.1-Ubuntu)
OpenJDK 64-Bit Server VM (build 17.0.21.0.3+1-1-24.04.1-Ubuntu, mixed mode, sharing)
Apache Maven 3.9.10 (5f519b97e944483d878815739f519b2eade0a91d)
Maven home: /mnt/c/Program Files/apache-maven-3.9.10
Java version: 17.0.21.0.3, vendor: Ubuntu, runtime: /usr/lib/jvm/java-17-openjdk-amd64
Default locale: en, platform encoding: UTF-8
OS name: "linux", version: "6.18.58.1-microsoft-standard-wsl2", arch: "amd64", family: "unix"
```

## Ажиллуулах

Төслийн хавтсанд `mvn clean verify` ажиллуулахад JUnit тестүүд ажиллаж, JaCoCo тайлан `target/site/jacoco/` дотор үүснэ. Төсөл Java 17, JUnit Jupiter 5.10.2, JaCoCo 0.8.12 болон Maven Compiler Plugin 3.13.0 ашигладаг. Хүснэгт, CFG, тестийн тайлбар дахь мөрийн дугаарууд `d409a06` starter commit дахь `DataFlowTargets.java`-тай таарна.

## A — gcd

13-р мөрөнд `x`, `y` параметрүүд анхны утгаа авна. `tmp`-ийг 14-р мөрөнд зарлаж, 16-р мөрөнд `x % y`-ийн үр дүнг анх онооно. 15-р мөр `y`-г давталтын нөхцөлд шалгадаг тул p-use болно. 16–18-р мөрөнд утгуудыг тооцоолох, оноохдоо хэрэглэж, 20-р мөрөнд `x`-ийг буцаадаг тул эдгээр хэрэглээ нь c-use юм.

| Variable | Def | Use | Kind | Def-clear path | Test ID | Covered |
|---|---|---|---|---|---|---|
| x | 13 | 16 | c | 13→15T→16 | gcdTwoIterations_13_15_16_17_18_20 | Yes |
| x | 13 | 20 | c | 13→15F→20 | gcdZeroY_13to20 | Yes |
| x | 17 | 16 | c | 17→18→15T→16 | gcdTwoIterations_13_15_16_17_18_20 | Yes |
| x | 17 | 20 | c | 17→18→15F→20 | gcdTwoIterations_13_15_16_17_18_20 | Yes |
| y | 13 | 15 | p-T/F | 13→15 | gcdTwoIterations_13_15_16_17_18_20; gcdZeroY_13to20 | Yes |
| y | 13 | 16 | c | 13→15T→16 | gcdTwoIterations_13_15_16_17_18_20 | Yes |
| y | 13 | 17 | c | 13→15T→16→17 | gcdTwoIterations_13_15_16_17_18_20 | Yes |
| y | 18 | 15 | p-T/F | 18→15 | gcdTwoIterations_13_15_16_17_18_20 | Yes |
| y | 18 | 16 | c | 18→15T→16 | gcdTwoIterations_13_15_16_17_18_20 | Yes |
| y | 18 | 17 | c | 18→15T→16→17 | gcdTwoIterations_13_15_16_17_18_20 | Yes |
| tmp | 16 | 18 | c | 16→17→18 | gcdTwoIterations_13_15_16_17_18_20 | Yes |

Хүснэгтийн 11 хосоос `y`-ийн хоёр p-use-ийг T/F салаагаар нь тооцоход 13 шаардлага гарна. `gcd(7, 0)` давталтад орохгүйгээр 13-р мөрийн `x`-ийг 20-р мөрөнд буцаана. Иймээс сонгосон тестүүдээс зөвхөн энэ оролт `x 13→20` хосыг хамарна. `gcd(12, 8)` дээр `(12, 8) → (8, 4) → (4, 0)` гэсэн хоёр давталт явагдана. Хоёр дахь давталтаар `x 17→16`, `y 18→16`, `y 18→17` хосууд хамрагдана. `gcd(0, 5)` нь эхний параметр тэг байх тохиолдлыг шалгана.

## B — bonus

### B1 — Удирдлагын урсгалын граф

![bonus CFG](cfg-bonus.png)

CFG-ийн дээд хэсэгт E1–E26 дугаартай ирмэгүүдийг харуулсан. Доод хэсэгт ирмэг бүрийг дайрдаг тестийн аргын нэр, нөхцөлтэй ирмэг бүрийн T/F үр дүнг тэмдэглэсэн. 33-р мөрөнд exception шидэж, 56-р мөрөнд оноог буцааж дуусна. 38c болон 38d нь 38-р мөрийн давталтын нөхцөл ба `a`-д утга оноох үйлдэл. 32a болон 32b нь 32-р мөрийн short-circuit нөхцөлийн хоёр шалгалт.

### B2 — Def/use

| Мөр | Def | c-use | p-use |
|---|---|---|---|
|31|attendance, threshold|—|—|
|32a / 32b|—|—|attendance / threshold|
|35|present|—|—|
|36|streak|—|—|
|37|best|—|—|
|38c / 38d|a (38d)|—|attendance (38c)|
|39|—|—|a|
|40|present|present|—|
|41|streak|streak|—|
|42|—|—|streak, best|
|43|best|streak|—|
|46|streak|—|—|
|49|score|—|—|
|50|—|—|present, threshold|
|51|score|—|—|
|53|—|—|best|
|54|score|score|—|
|56|—|score|—|

33-р мөрөнд `IllegalArgumentException` шидсэнээр гүйцэтгэл дуусна. Хүснэгтэд эх кодод ил тод байгаа долоон хувьсагчийн def, c-use, p-use-ийг бүртгэсэн. Нэмэх үйлдэлтэй мөрөнд, жишээлбэл 40-р мөрөнд, `present`-ийн өмнөх утгыг ашигласны дараа шинэ утга оноодог.

### B3 — DU хүснэгт

Нөхцөлийн үнэн, худал салааг тусад нь тоолоход 33 шаардлага гарсан. Def-clear замд анхны оноолтоос хэрэглээ хүртэл тухайн хувьсагчийн утга дахин оноогдохгүй. Жишээ нь `present 40→40` хосын эхний 40-р мөр `present`-д шинэ утга онооно. Дараагийн ирсэн өдрийн 40-р мөр энэ утгыг эхэлж уншаад дараа нь шинэчилдэг. `streak 41→41` хос мөн ийм дарааллаар хамрагдана.

| Variable | Def | Use | Kind | Def-clear witness | Test IDs | Covered |
|---|---|---|---|---|---|---|
| a | 38d | 39 | p-F | 38d → 39 | BD1_allDefs_score49to54, BD2_allDefs_score51to56, BB_negativeMeansAbsent, BM2_separatedRuns_doNotEarnStreakBonus, BB_allAbsent | Yes |
| a | 38d | 39 | p-T | 38d → 39 | BD1_allDefs_score49to54, BD2_allDefs_score51to56, BD5_duWitness, BB_longerThanFive, BB_negativeMeansAbsent, BM2_separatedRuns_doNotEarnStreakBonus | Yes |
| attendance | 31 | 32a | p-F | 31 → 32a | BD1_allDefs_score49to54, BD2_allDefs_score51to56, BD3_duWitness, BD4_duWitness, BD5_duWitness, BD7_duWitness, BB_longerThanFive, BB_negativeMeansAbsent, BM2_separatedRuns_doNotEarnStreakBonus, BB_allAbsent | Yes |
| attendance | 31 | 32a | p-T | 31 → 32a | BD6_duWitness, BX_nullAndNegative | Yes |
| attendance | 31 | 38c | p-F | 31 → 32a → 32b → 35 → 36 → 37 → 38c | BD3_duWitness, BD4_duWitness, BB_allAbsent, BD2_allDefs_score51to56, BB_negativeMeansAbsent, BD5_duWitness, BB_longerThanFive, BD1_allDefs_score49to54, BM2_separatedRuns_doNotEarnStreakBonus | Yes |
| attendance | 31 | 38c | p-T | 31 → 32a → 32b → 35 → 36 → 37 → 38c | BD1_allDefs_score49to54, BD2_allDefs_score51to56, BD5_duWitness, BB_longerThanFive, BB_negativeMeansAbsent, BM2_separatedRuns_doNotEarnStreakBonus, BB_allAbsent | Yes |
| best | 37 | 42 | p-T | 37 → 38c → 38d → 39 → 40 → 41 → 42 | BD1_allDefs_score49to54, BD5_duWitness, BB_longerThanFive, BM2_separatedRuns_doNotEarnStreakBonus, BD2_allDefs_score51to56, BB_negativeMeansAbsent | Yes |
| best | 37 | 53 | p-F | 37 → 38c → 49 → 50 → 53 | BD3_duWitness, BD4_duWitness, BB_allAbsent | Yes |
| best | 43 | 42 | p-F | 43 → 38c → 38d → 39 → 46 → 38c → 38d → 39 → 40 → 41 → 42 | BD1_allDefs_score49to54, BM2_separatedRuns_doNotEarnStreakBonus | Yes |
| best | 43 | 42 | p-T | 43 → 38c → 38d → 39 → 40 → 41 → 42 | BD1_allDefs_score49to54, BD5_duWitness, BB_longerThanFive, BM2_separatedRuns_doNotEarnStreakBonus | Yes |
| best | 43 | 53 | p-F | 43 → 38c → 49 → 50 → 53 | BM2_separatedRuns_doNotEarnStreakBonus, BD2_allDefs_score51to56, BB_negativeMeansAbsent | Yes |
| best | 43 | 53 | p-T | 43 → 38c → 49 → 50 → 51 → 53 | BD5_duWitness, BB_longerThanFive, BD1_allDefs_score49to54 | Yes |
| present | 35 | 40 | c | 35 → 36 → 37 → 38c → 38d → 39 → 40 | BD1_allDefs_score49to54, BD5_duWitness, BB_longerThanFive, BM2_separatedRuns_doNotEarnStreakBonus, BD2_allDefs_score51to56, BB_negativeMeansAbsent | Yes |
| present | 35 | 50 | p-F | 35 → 36 → 37 → 38c → 49 → 50 | BD3_duWitness, BB_allAbsent | Yes |
| present | 35 | 50 | p-T | 35 → 36 → 37 → 38c → 49 → 50 | BD4_duWitness | Yes |
| present | 40 | 40 | c | 40 → 41 → 42 → 38c → 38d → 39 → 40 | BM2_separatedRuns_doNotEarnStreakBonus, BD1_allDefs_score49to54, BD5_duWitness, BB_longerThanFive | Yes |
| present | 40 | 50 | p-F | 40 → 41 → 42 → 38c → 49 → 50 | BD1_allDefs_score49to54, BM2_separatedRuns_doNotEarnStreakBonus | Yes |
| present | 40 | 50 | p-T | 40 → 41 → 42 → 43 → 38c → 49 → 50 | BD2_allDefs_score51to56, BD5_duWitness, BB_longerThanFive, BB_negativeMeansAbsent | Yes |
| score | 49 | 54 | c | 49 → 50 → 53 → 54 | BD1_allDefs_score49to54 | Yes |
| score | 49 | 56 | c | 49 → 50 → 53 → 56 | BD3_duWitness, BM2_separatedRuns_doNotEarnStreakBonus, BB_allAbsent | Yes |
| score | 51 | 54 | c | 51 → 53 → 54 | BD5_duWitness, BB_longerThanFive | Yes |
| score | 51 | 56 | c | 51 → 53 → 56 | BD2_allDefs_score51to56, BD4_duWitness, BB_negativeMeansAbsent | Yes |
| score | 54 | 56 | c | 54 → 56 | BD1_allDefs_score49to54, BD5_duWitness, BB_longerThanFive | Yes |
| streak | 36 | 41 | c | 36 → 37 → 38c → 38d → 39 → 40 → 41 | BD1_allDefs_score49to54, BD5_duWitness, BB_longerThanFive, BM2_separatedRuns_doNotEarnStreakBonus | Yes |
| streak | 41 | 41 | c | 41 → 42 → 38c → 38d → 39 → 40 → 41 | BM2_separatedRuns_doNotEarnStreakBonus, BD1_allDefs_score49to54, BD5_duWitness, BB_longerThanFive | Yes |
| streak | 41 | 42 | p-F | 41 → 42 | BD1_allDefs_score49to54, BM2_separatedRuns_doNotEarnStreakBonus | Yes |
| streak | 41 | 42 | p-T | 41 → 42 | BD1_allDefs_score49to54, BD2_allDefs_score51to56, BD5_duWitness, BB_longerThanFive, BB_negativeMeansAbsent, BM2_separatedRuns_doNotEarnStreakBonus | Yes |
| streak | 41 | 43 | c | 41 → 42 → 43 | BD1_allDefs_score49to54, BD2_allDefs_score51to56, BD5_duWitness, BB_longerThanFive, BB_negativeMeansAbsent, BM2_separatedRuns_doNotEarnStreakBonus | Yes |
| streak | 46 | 41 | c | 46 → 38c → 38d → 39 → 40 → 41 | BD1_allDefs_score49to54, BD2_allDefs_score51to56, BB_negativeMeansAbsent, BM2_separatedRuns_doNotEarnStreakBonus | Yes |
| threshold | 31 | 32b | p-F | 31 → 32a → 32b | BD1_allDefs_score49to54, BD2_allDefs_score51to56, BD3_duWitness, BD4_duWitness, BD5_duWitness, BB_longerThanFive, BB_negativeMeansAbsent, BM2_separatedRuns_doNotEarnStreakBonus, BB_allAbsent | Yes |
| threshold | 31 | 32b | p-T | 31 → 32a → 32b | BD7_duWitness | Yes |
| threshold | 31 | 50 | p-F | 31 → 32a → 32b → 35 → 36 → 37 → 38c → 49 → 50 | BD3_duWitness, BB_allAbsent, BD1_allDefs_score49to54, BM2_separatedRuns_doNotEarnStreakBonus | Yes |
| threshold | 31 | 50 | p-T | 31 → 32a → 32b → 35 → 36 → 37 → 38c → 49 → 50 | BD4_duWitness, BD2_allDefs_score51to56, BB_negativeMeansAbsent, BD5_duWitness, BB_longerThanFive | Yes |

**Дахин оноолт ба биелэх боломжгүй замууд.** Тасалсан өдөр 46-р мөр `streak`-ийг тэглэж, 36, 41 эсвэл өмнөх давталтын 46-р мөрөнд оноосон утгыг дарна. Ийм замаар 41-р мөрөнд хүрэхэд хамгийн сүүлийн 46-р мөрийн утга хэрэглэгдэнэ. 36 эсвэл 46-р мөрийн `streak` 42, 43-р мөрөнд хүрэхээс өмнө 41-р мөрөнд заавал шинэчлэгдэнэ. Үүнтэй адил 51-р мөр ажиллавал 49-р мөрийн `score` дарагдаж, 54 эсвэл 56-р мөрөнд тэр утга хүрэхгүй.

`best 37→42F` биелэхгүй. Анхны ирсэн өдөр `streak` 1, `best` 0 тул 42-р мөрийн нөхцөл үнэн байна. `best 37→53T` мөн биелэхгүй. 43-р мөрөөр шинэчлэгдээгүй `best` анхны 0 утгатай, 5-ын босгыг давахгүй. `threshold` 50-р мөрөнд хүрэхийн тулд массив `null` биш, босго сөрөг биш байх шаардлагатай.

Хосуудыг тодорхойлохдоо CFG дээр оноолт бүрээс дараагийн дахин оноолт хүртэл хүрч болох хэрэглээг мөрдсөн. [`du_analysis.py`](analysis/du_analysis.py) нь хүснэгтийн замыг жишээ оролтоор давхар шалгахад ашигласан туслах скрипт юм. Скрипт 0–8 урттай хоёртын массив, `0`, `n`, `n+1` босго болон буруу оролтуудыг шалгадаг. Хүснэгтийн хамралтыг эх кодын урсгал болон JUnit тестийн оролттой тулгаж тайлбарлав.

### B4 — all-defs → all-DU-pairs

`bonus`-ийн all-defs хамралтад хамгийн багадаа хоёр тест шаардлагатай. 50-р мөрийн нөхцөл үнэн үед 51-р мөр `score`-ийн анхны 0 утгыг ашиглахаас нь өмнө 5 болгож дардаг. Иймээс 49, 51-р мөрийн оноолтыг хоёуланг нь нэг гүйцэтгэлээр хэрэглээнд хүргэх боломжгүй. `BD1` 49-р мөрийн утгыг 54-р мөрөнд хүргэнэ. `BD2` 51-р мөрийн утгыг 56-р мөрөнд хүргэнэ. Үлдсэн оноолтууд мөн энэ хоёр тестэд хамрагдсан. `gcd`-ийн гурван тесттэй нийлээд эхний шатны [Maven гаралт](results/mvn-verify-alldefs.txt)-д 5 тест амжилттай ажилласан.

All-DU-pairs шатанд 10 `bonus`, 3 `gcd` тест ажилласан. `BD3` ба `BD4` нь хоосон массив дээр 1 болон 0 босго өгөхөд харгалзан 0, 5 оноо гарахыг шалгана. `BD5` нь таван өдөр дараалж ирсэн, босго 0 үед 8 оноо гарахыг шалгана. `BD6`, `BD7` нь `null` массив болон сөрөг босго дээр `IllegalArgumentException` хүлээнэ. Энэ таван тестийн `@DisplayName`-д DU хос бүрийг эх кодын мөрөөр нь тэмдэглэсэн. Үүнээс гадна урт цуваа, сөрөг ирцийн утга, бүгд тасалсан нөхцөлийг шалгасан. M2-ыг унагах тест, бүгд тасалсан тохиолдлыг нэмснээр эцсийн багц 15 тесттэй болсон.

All-defs-ийн багц, гаралтыг `d20e0bf` commit-д хадгалсан. All-DU-pairs-ийн тестүүд `91e08d4` commit-д нэмэгдсэн.

### B5 — JaCoCo

| Үе шат | Амжилттай тест | Хамарсан салаа | Хамарсан мөр |
|---|---:|---:|---:|
| All-defs ([CSV](results/jacoco-alldefs.csv)) | 5 | 14/16 | 22/24 |
| Эцсийн багц ([CSV](results/jacoco-final.csv)) | 15 | 16/16 | 23/24 |

All-defs багцын оролтууд зөв байсан учраас алдаа шидэх хоёр салаа хамрагдаагүй. Эцсийн багц бүх салааг хамарсан бөгөөд хамрагдаагүй ганц мөр нь 7-р мөрийн далд constructor юм.

`BD1`, `BD2`, `BD6`, `BD7` дөрвөн тест нийлээд бүх салааг дайрах боломжтой ч `score 49→56`, `score 51→54` хосууд дутна. `BD3` дээр нэмэлт оноо авах хоёр нөхцөл хоёулаа худал учир 49-р мөрийн 0 утга шууд 56-р мөрөнд хүрнэ. `BD5` дээр хоёр нөхцөл хоёулаа үнэн учир 51-р мөрийн 5 оноог 54-р мөрөнд ашиглаж 3-аар нэмнэ. Ижил салаануудыг дайрсан ч аль оноолтын утга хэрэглээнд хүрэх нь оролтоос хамаардаг.

## C — Fault seeding

Алдааны мөрийн дугааруудыг мутаци бүрийг ажиллуулсан үеийн `results/` логуудаас авсан.

| Mutation | Бодит үр дүн | Нотолгоо |
|---|---|---|
| M1 | [ERROR]   BonusTest.BB_longerThanFive:13 expected: <8> but was: <5>; [ERROR]   BonusTest.BD1_allDefs_score49to54:5 expected: <3> but was: <0>; [ERROR]   BonusTest.BD5_duWitness:9 expected: <8> but was: <5> | results/mvn-test-M1.txt |
| M2 | `BUILD SUCCESS`, 13 тест амжилттай | results/mvn-test-M2.txt |
| M3 | `BUILD SUCCESS`, 13 тест амжилттай | results/mvn-test-M3.txt |
| M2-kill | [ERROR]   BonusTest.BM2_separatedRuns_doNotEarnStreakBonus:15 expected: <0> but was: <3> | results/mvn-test-M2-kill.txt |

M1-д `streak`-ийг нэмэх мөрийг устгахад таван өдрийн урамшууллыг шалгасан гурван тест унасан. M2 эхний 13 тестийг давсан. Тэдгээр оролтод `best` шинэчлэгдэх үед `present` болон `streak` ижил утгатай байв. Тасралтын дараах богино цуваа өмнөх дээд амжилтыг даваагүй тул 43-р мөр дахин ажиллаагүй.

M2-д зориулж `[1, 1, 1, 0, 1, 1, 1, 1]` оролтыг `threshold = 8`-тай шалгасан. Нийт 7 өдөр ирсэн, хамгийн урт цуваа 4 тул зөв оноо 0. Мутацитай хувилбар сүүлийн шинэчлэлтээр `best = 7` болгож, буруу 3 оноо өгсөн. 15 тесттэй багцад `BM2_separatedRuns_doNotEarnStreakBonus` ганцаараа унасан нь логт хадгалагдсан.

M3-т нэмсэн `total`-ийг дараа нь хаана ч ашигладаггүй. Буцах оноо хэвээр байсан тул 13 тест амжилттай ажилласан. Ашиглагдаагүй хувьсагчийг шалгахын тулд Eclipse JDT ECJ 3.40.0-ийг `-17 -proc:none -warn:+unusedLocal` тохиргоотой ажиллуулахад [дараах анхааруулга](results/m3-static-analysis.txt) гарсан.

```text
The value of the local variable total is not used
```

Мутаци бүрийн дараа `DataFlowTargets.java`-г сэргээсэн. Эцсийн файлыг starter commit `d409a06`-тай тулгахад зөрүү гараагүй. Сэргээсэн хувилбарын [Maven гаралт](results/mvn-verify-final.txt)-д 15 тест амжилттай ажилласан.

## DU хүснэгтийн давтан шалгалт

Codex эхний хүснэгтийг [baseline-du.md](analysis/baseline-du.md)-д, давтан шалгалтыг [ai-review.md](analysis/ai-review.md)-д тэмдэглэсэн. Хоёр хүснэгтийн 33 шаардлага таарсан. `best 37→42F` болон `best 37→53T` яагаад биелэхгүйг `best`-ийн анхны утга болон эхний шинэчлэлтээр тайлбарласан. `streak`-ийн 36, 46-р мөрийн утга 42, 43-р мөрөнд хүрэхээс өмнө 41-р мөрөнд дахин оноогддог. 38-р мөрд `attendance`-ийг шалгах болон `a`-д утга оноох үйлдлийг тусад нь бүртгэсэн.

## Дүгнэлт

Салааны хамралтаар нөхцөл бүрийн аль салаа ажилласныг харж болно. DU хүснэгт тэр салаагаар дамжсан хувьсагчийн утга аль мөрөөс ирснийг нэмж харуулдаг. Хамгийн их нягтлах шаардлагатай хэсэг нь давталтын дараагийн алхамд `streak`, `best`-ийн аль оноолт хүчинтэй хэвээр байгааг мөрдөх байв. All-defs багц оноолт бүрийг дор хаяж нэг удаа хэрэглээнд хүргэсэн ч бүх DU хосыг хамраагүй. M1-д `streak` шинэчлэгдэхгүй болоход гурван тест унасан. M2-ын хувьд бүх DU хос хамрагдсан байсан ч нийт ирц, хамгийн урт цуваа ялгаатай оролт нэмсний дараа алдаа илэрсэн. M3-ын ашиглагдаагүй хувьсагчийг ECJ илрүүлсэн бөгөөд JUnit-ээр шалгасан буцах утгууд хэвээр байв.

## AI ба баталгаажуулалтын хүрээ

Энэ тайланг бэлтгэхдээ Codex ашигласан. DU хүснэгтийн эхний хувилбар, тестийн оролт сонгох, CFG дүрслэх болон тайлбаруудыг найруулахад тусалсан. Мутацийн туршилтуудыг Codex ажиллуулж, гаралтыг [`results/`](results/) хавтаст хадгалсан.

Засварын дараа Codex шинэ локал хуулбар дээр `mvn clean verify` ажиллуулж, 15 тест амжилттай болсныг шалгасан. Шинээр үүссэн JaCoCo CSV нь хадгалсан `jacoco-final.csv`-тэй таарсан. Мөн `BD3`–`BD7`-ийн `@DisplayName` дахь мөрийн дугаар болон T/F салааг DU хүснэгттэй тулгасан.
