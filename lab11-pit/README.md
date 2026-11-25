# Лаборатори №11. PIT mutation testing

Овог нэр — С.Хишигтогтох

Оюутны код — B232270806

## Орчин

Гаралтыг `lab11-pit` төслийн хавтсаас авсан.

### `java -version`

```text
[0.015s][warning][perf,memops] Cannot use file /tmp/hsperfdata_hishigtogtokh/9 because it is locked by another process (errno = 11)
openjdk version "17.0.21.1" 2026-11-17
OpenJDK Runtime Environment (build 17.0.21.1+2-1-24.04.1-Ubuntu)
OpenJDK 64-Bit Server VM (build 17.0.21.1+2-1-24.04.1-Ubuntu, mixed mode, sharing)
```

### `mvn -version`

```text
Apache Maven 3.9.10 (5f519b97e944483d878815739f519b2eade0a91d)
Maven home: /mnt/c/Program Files/apache-maven-3.9.10
Java version: 17.0.21.1, vendor: Ubuntu, runtime: /usr/lib/jvm/java-17-openjdk-amd64
Default locale: en, platform encoding: UTF-8
OS name: "linux", version: "6.18.58.1-microsoft-standard-wsl2", arch: "amd64", family: "unix"
```

## Эхний хэмжилт

JaCoCo 25/25 мөр (100%), 38/41 салаа хамарсныг харуулсан. PIT нийт 63 мутантаас 17-г (27%) илрүүлж, 46 нь амьд үлдсэн.

Мөрийн хамралт нь тест тухайн кодыг ажиллуулсныг хэмждэг. Starter тестүүд дүн хоосон утга биш эсэх, голч болон тэтгэлэг зөвшөөрсөн мужид багтах эсэхийг л шалгасан учраас буруу боловч тэр шалгалтад нийцсэн үр дүнг илрүүлээгүй. Mutation coverage энэ сул талыг харуулсан.

![JaCoCo-ийн эхний хэмжилт](results/jacoco-start.png)

[Maven verify гаралт](results/mvn-verify-start.txt) · [JaCoCo CSV](results/jacoco-start.csv) · [PIT-ийн эхний гаралт](results/pit-start.txt)

## A. Starter дээр амьд үлдсэн мутантууд

PIT-ийн тайланд `letterGrade`-д 19, `gpa`-д 4, `scholarship`-д 23 буюу нийт **46** мутант `SURVIVED` төлөвтэй гарсан. Хүснэгтэд PIT-ийн тайлбарыг ашиглаж, нэг мөрөнд ижил тайлбартай мутаци байгаа үед нөлөөлсөн нөхцөлийг нь бичив.

| Кодын мөр | PIT-ийн тайлбар ба нөлөөлсөн хэсэг | Тоо | Ангилал | Үндэслэл ба авах арга хэмжээ |
| --- | --- | ---: | --- | --- |
| 20 | `changed conditional boundary`, доод ба дээд хязгаар | 2 | Тест дутуу | Заагийн мутаци хүчинтэй 0 эсвэл 100 дээр exception үүсгэх тул B2-д 0 → F, 100 → A гэж шалгана. |
| 23 | `changed conditional boundary`, 90 | 1 | Тест дутуу | 90 оноо A-аас B болж өөрчлөгдөх тул B2-д 90 → A гэж шалгана. |
| 23 | `removed conditional - replaced comparison check with true` / `false` | 2 | Тест дутуу | A салааг албадвал 85 дээр A, алгасвал 95 дээр B буцах тул B1-д 85 → B, 95 → A гэж шалгана. |
| 23 | `replaced return value with ""`, A | 1 | Тест дутуу | 95 дээр хоосон мөр буцахад starter-ийн `assertNotNull` амжилттай өнгөрөх тул B1-д 95 → A гэж шалгана. |
| 24 | `changed conditional boundary`, 80 | 1 | Тест дутуу | 80 оноо B-ээс C болж өөрчлөгдөх тул B2-д 80 → B гэж шалгана. |
| 24 | `removed conditional - replaced comparison check with true` / `false` | 2 | Тест дутуу | B салааг албадвал 75 дээр B, алгасвал 85 дээр C буцах тул B1-д 75 → C, 85 → B гэж шалгана. |
| 24 | `replaced return value with ""`, B | 1 | Тест дутуу | 85 дээр хоосон мөр буцахад `assertNotNull` амжилттай өнгөрөх тул B1-д 85 → B гэж шалгана. |
| 25 | `changed conditional boundary`, 70 | 1 | Тест дутуу | 70 оноо C-ээс D болж өөрчлөгдөх тул B2-д 70 → C гэж шалгана. |
| 25 | `removed conditional - replaced comparison check with true` / `false` | 2 | Тест дутуу | C салааг албадвал 65 дээр C, алгасвал 75 дээр D буцах тул B1-д 65 → D, 75 → C гэж шалгана. |
| 25 | `replaced return value with ""`, C | 1 | Тест дутуу | 75 дээр хоосон мөр буцахад `assertNotNull` амжилттай өнгөрөх тул B1-д 75 → C гэж шалгана. |
| 26 | `changed conditional boundary`, 60 | 1 | Тест дутуу | 60 оноо D-ээс F болж өөрчлөгдөх тул B2-д 60 → D гэж шалгана. |
| 26 | `removed conditional - replaced comparison check with true` / `false` | 2 | Тест дутуу | D салааг албадвал 30 дээр D, алгасвал 65 дээр F буцах тул B1-д 30 → F, 65 → D гэж шалгана. |
| 26 | `replaced return value with ""`, D | 1 | Тест дутуу | 65 дээр хоосон мөр буцахад `assertNotNull` амжилттай өнгөрөх тул B1-д 65 → D гэж шалгана. |
| 27 | `replaced return value with ""`, F | 1 | Тест дутуу | 30 дээр хоосон мөр буцахад `assertNotNull` амжилттай өнгөрөх тул B1-д 30 → F гэж шалгана. |
| 36 | `Changed switch default to be first case` | 1 | Тест дутуу | F дүнгийн default салаа эхний салааны 4 оноог нэмэх тул B1-д `gpa([40]) → 0.0` гэж шалгана. |
| 38 | `Replaced double addition with subtraction`, B | 1 | Тест дутуу | B-ийн 3 оноог хасвал [95, 85]-ын голч 0.5 болох тул B1-д 3.5 гэж шалгана. |
| 40 | `Replaced double addition with subtraction`, D | 1 | Тест дутуу | D-ийн 1 оноог хасвал [75, 65]-ын голч 0.5 болох тул B1-д 1.5 гэж шалгана. |
| 44 | `replaced double return with 0.0d` | 1 | Тест дутуу | Эерэг голч 0.0 болж өөрчлөгдөх тул B1-д [95, 85] → 3.5 гэж шалгана. |
| 48 | `changed conditional boundary`, голч ба кредитийн доод хязгаар | 2 | Тест дутуу | Голч эсвэл кредит яг 0 байхад exception үүсэх тул B2-д (0, 12, false) → 0, (3.0, 0, false) → 50 гэж шалгана. |
| 48 | `removed conditional - replaced comparison check with true`, сөрөг голчийн шалгалт | 1 | Тест дутуу | Сөрөг голч зөвшөөрөгдөж 0 буцах тул B2-д (−0.01, 12, false) дээр exception шалгана. |
| 51 | `removed conditional - replaced equality check with true` / `false` | 2 | Тест дутуу | Зөрчлийн нөхцөлийг албадвал зөрчилгүй оюутанд 0, алгасвал зөрчилтэй оюутанд 100 буцах тул B1-д (3.9, 16, false) → 100, (4, 20, true) → 0 гэж шалгана. |
| 52 | `changed conditional boundary`, 3.8 ба 15 кредит | 2 | Тест дутуу | Голч эсвэл кредитийг яг заагаар нь өгөхөд 100-аас 70 болж буурах тул B2-д (3.8, 16, false) ба (3.9, 15, false) дээр 100 шалгана. |
| 52 | `removed conditional - replaced comparison check with true` / `false`, голч | 2 | Тест дутуу | Голчийн шалгалтыг алгасвал (3.79, 15, false) дээр 100, салааг хаавал (3.9, 16, false) дээр 70 буцах тул B2 ба B1-д харгалзан 70, 100 шалгана. |
| 52 | `removed conditional - replaced comparison check with true` / `false`, кредит | 2 | Тест дутуу | Кредитийн шалгалтыг алгасвал (3.8, 14, false) дээр 100, салааг хаавал (3.9, 16, false) дээр 70 буцах тул B2 ба B1-д харгалзан 70, 100 шалгана. |
| 52 | `replaced int return with 0`, 100% | 1 | Тест дутуу | 100 авах ёстой оюутанд 0 буцах тул B1-д (3.9, 16, false) → 100 гэж шалгана. |
| 53 | `changed conditional boundary`, 3.4 ба 12 кредит | 2 | Тест дутуу | Голч эсвэл кредитийг яг заагаар нь өгөхөд 70-аас 50 болж буурах тул B2-д (3.4, 13, false) ба (3.5, 12, false) дээр 70 шалгана. |
| 53 | `removed conditional - replaced comparison check with true` / `false`, голч | 2 | Тест дутуу | Голчийн шалгалтыг алгасвал (3.39, 12, false) дээр 70, салааг хаавал (3.5, 13, false) дээр 50 буцах тул B2 ба B1-д харгалзан 50, 70 шалгана. |
| 53 | `removed conditional - replaced comparison check with true` / `false`, кредит | 2 | Тест дутуу | Кредитийн шалгалтыг алгасвал (3.4, 11, false) дээр 70, салааг хаавал (3.5, 13, false) дээр 50 буцах тул B2 ба B1-д харгалзан 50, 70 шалгана. |
| 53 | `replaced int return with 0`, 70% | 1 | Тест дутуу | 70 авах ёстой оюутанд 0 буцах тул B1-д (3.5, 13, false) → 70 гэж шалгана. |
| 54 | `changed conditional boundary`, 3.0 | 1 | Тест дутуу | Яг 3.0 голчтой оюутанд 0 буцах тул B2-д (3.0, 0, false) → 50 гэж шалгана. |
| 54 | `removed conditional - replaced comparison check with true` / `false` | 2 | Тест дутуу | 50%-ийн салааг албадвал (2.0, 1, false) дээр 50, алгасвал (3.1, 5, false) дээр 0 буцах тул B1-д харгалзан 0, 50 шалгана. |
| 54 | `replaced int return with 0`, 50% | 1 | Тест дутуу | 50 авах ёстой оюутанд 0 буцах тул B1-д (3.1, 5, false) → 50 гэж шалгана. |

## B. Тест сайжруулсны дараах хэмжилт

| Үе | Үүссэн | Илрүүлсэн | Амьд | Mutation Coverage | PIT гаралт |
| --- | ---: | ---: | ---: | ---: | --- |
| Эхлэл | 63 | 17 | 46 | 27% | [pit-start.txt](results/pit-start.txt) |
| B1. Яг утгын assertion | 63 | 45 | 18 | 71% | [pit-B1.txt](results/pit-B1.txt) |

B1-д starter-ийн оролтуудыг ашиглаж, дүн, голч, тэтгэлгийн буцах утгыг `assertEquals`-оор шалгав. Үүний дараа 28 нэмэлт мутант илэрсэн бөгөөд үлдсэн 18 нь зааг өөрчилсөн 13, нөхцөлийг тогтмол болгосон 5 мутант байв.
