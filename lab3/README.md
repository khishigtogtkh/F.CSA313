# Laboratory 03 — Quality Scenario → SLO → k6 Threshold

**Хичээл:** F.CSA313 — Программ хангамжийн чанарын баталгаа ба тест
**Оюутны нэр:** [С.Хишигтогтох]
**Оюутны код:** [B232270806]

## Зорилго

Энэхүү лабораторийн ажлын зорилго нь локал API дээр чанарын сценарио тодорхойлж, тэдгээрийг хэмжигдэхүйц SLO болгон хувирган, Grafana k6 ашиглан threshold-оор автоматаар шалгах юм.

## Ашигласан технологи

* Node.js
* Express.js
* Grafana k6
* Ubuntu / WSL2
* Git / GitHub

## Орчны мэдээлэл``

### k6

```bash
k6 version
```
k6 v2.2.0

## Project бүтэц

```text
lab3/
├── server.js
├── slo-test.js
├── slo-test-fail.js
├── package.json
├── package-lock.json
├── README.md
├── .gitignore
└── results/
```

## Local API

Лабораторийн тестэд ашиглах Express API нь дараах 3 endpoint-той.

| Method | Endpoint    | Зориулалт                                         |
| ------ | ----------- | ------------------------------------------------- |
| POST   | `/cart/add` | Сагсанд бараа нэмэх хурдан endpoint               |
| GET    | `/report`   | 200–400 ms сааталтай тайлангийн endpoint          |
| POST   | `/pay`      | Ойролцоогоор 5% алдаа үүсгэдэг төлбөрийн endpoint |

Серверийг ажиллуулах:

```bash
node server.js
```

Амжилттай ажилласан үед:

```text
API: http://localhost:3000
```

## Endpoint шалгах

### Cart

```bash
curl -X POST http://localhost:3000/cart/add
```

Хүлээгдэж буй хариу:

```json
{"ok":true,"items":1}
```

### Report

```bash
curl http://localhost:3000/report
```

Хүлээгдэж буй хариу:

```json
{"rows":20000}
```

### Payment

```bash
curl -X POST http://localhost:3000/pay
```

Ихэнх хүсэлт:

```json
{"paid":true}
```

Зарим хүсэлт зориудаар HTTP 500 алдаа буцаана.

## Одоогийн төлөв

* [x] Node.js project үүсгэсэн
* [x] Express суулгасан
* [x] Local API үүсгэсэн
* [x] `results/` хавтас үүсгэсэн
* [x] k6 test файлуудын бүтэц үүсгэсэн
* [x] Quality scenario бичих
* [x] SLO тодорхойлох
* [x] k6 threshold хэрэгжүүлэх
* [x] PASS test хийх
* [x] Chaos test хийх
* [x] Intentional FAIL test хийх

## 1. Чанарын сценарио

### 1.1 Performance Scenario — Cart

| Хэсэг | Тайлбар |
|---|---|
| Тойм | Хэрэглэгч барааг сагсанд нэмэх үед систем хурдан хариу өгөх ёстой. |
| Системийн төлөв | Express API сервер хэвийн ажиллаж байна. |
| Орчны төлөв | Localhost орчинд 20 виртуал хэрэглэгч 1 минутын турш тогтмол ачаалал өгнө. |
| Гадаад өдөөлт | Хэрэглэгч `/cart/add` endpoint руу POST хүсэлт илгээнэ. |
| Шаардлагатай хариу | Сервер хүсэлтийг амжилттай боловсруулж HTTP 200 хариу буцаана. |
| Хэмжүүр | `/cart/add` хүсэлтийн хариу хугацааны p95 нь 50 ms-ээс бага байна. |

### 1.2 Reliability Scenario — Payment

| Хэсэг | Тайлбар |
|---|---|
| Тойм | Хэрэглэгч төлбөр хийх үед систем хэт олон алдаа гаргахгүй байх ёстой. |
| Системийн төлөв | Express API болон `/pay` endpoint хэвийн ажиллаж байна. |
| Орчны төлөв | Localhost орчинд 20 виртуал хэрэглэгч 1 минутын турш тогтмол ачаалал өгнө. |
| Гадаад өдөөлт | Хэрэглэгч `/pay` endpoint руу POST төлбөрийн хүсэлт илгээнэ. |
| Шаардлагатай хариу | Төлбөрийн хүсэлтүүдийн ихэнхийг сервер амжилттай боловсруулж HTTP 200 хариу буцаана. |
| Хэмжүүр | `/pay` endpoint-ийн error rate нь 8%-аас бага байна. |

### 1.3 Availability Scenario — Server Recovery

| Хэсэг | Тайлбар |
|---|---|
| Тойм | Сервер гэнэт зогссон үед систем богино хугацаанд дахин сэргэж хүсэлтүүдийг хүлээн авч эхлэх ёстой. |
| Системийн төлөв | Express API сервер эхэндээ хэвийн ажиллаж байна. |
| Орчны төлөв | k6 тест 2 минут ажиллах бөгөөд тестийн явцад серверийг 10 секунд зогсооно. |
| Гадаад өдөөлт | Express серверийн процесс гэнэт зогсоно (crash). |
| Шаардлагатай хариу | Сервер дахин асмагц API хүсэлтүүдийг хэвийн хүлээн авч эхэлнэ. |
| Хэмжүүр | Нийт хүсэлтийн availability 90%-иас багагүй байх ба сэргээх хугацаа 15 секундээс ихгүй байна. |


## 2. Service Level Objectives (SLO)

| Scenario | SLI | Threshold | Window / Condition |
|---|---|---|---|
| Performance | `/cart/add` response latency p95 | p95 < 50 ms | 20 VU, 1 минут |
| Reliability | `/pay` error rate | error rate < 8% | 20 VU, 1 минут |
| Availability | Successful request ratio | availability ≥ 90% | 2 минутын тест, 10 секундийн server downtime |
| Availability | Recovery time | ≤ 15 секунд | Server restart хийсний дараа |

## 3. Threshold сонгосон үндэслэл

### Performance

`/cart/add` endpoint нь нэмэлт сааталгүй энгийн JSON response буцаадаг тул localhost орчинд маш хурдан ажиллах ёстой. Иймээс p95 < 50 ms босгыг эхний SLO болгон сонгосон. Бодит k6 хэмжилтийн дараа энэ босго бодитой эсэхийг шалгана.

### Reliability

`/pay` endpoint нь серверийн кодоор ойролцоогоор 5% HTTP 500 алдаа зориудаар үүсгэдэг. Санамсаргүй хэлбэлзлийг тооцож error rate < 8% босгыг сонгосон.

### Availability

2 минутын туршилтын үеэр серверийг 10 секунд зориудаар зогсооно. Availability SLO-г 90% гэж сонгосон бөгөөд үүнээс error budget-ийг тооцно.

## 4. Availability Error Budget

Availability SLO = 90%

Туршилтын хугацаа:

2 минут = 120 секунд

Зөвшөөрөгдөх unavailable хугацаа:

120 × (1 - 0.90) = 12 секунд

Иймээс 2 минутын хугацаанд систем хамгийн ихдээ 12 секунд unavailable байх error budget-тэй.

## 5. Normal Load Test Result

k6 load test-ийг 20 виртуал хэрэглэгчтэйгээр 1 минутын турш ажиллуулав.

Туршилтын бодит үр дүн:

| Metric                  | SLO Threshold | Actual Result | Status |
| ----------------------- | ------------: | ------------: | ------ |
| `/cart/add` p95 latency |       < 50 ms |       3.48 ms | PASS   |
| `/report` p95 latency   |      < 450 ms |     389.77 ms | PASS   |
| `/pay` error rate       |          < 8% |         5.16% | PASS   |
| Checks success rate     |         > 90% |        98.27% | PASS   |

`/cart/add` endpoint-ийн p95 latency 3.48 ms гарсан тул 50 ms-ийн performance SLO-г хангаж байна.

`/report` endpoint нь зориудаар 200–400 ms сааталтай бөгөөд бодит p95 latency 389.77 ms гарсан. Энэ нь 450 ms-ийн threshold-оос бага тул performance SLO-г хангаж байна.

`/pay` endpoint-ийн 929 хүсэлтээс 48 хүсэлт амжилтгүй болсон бөгөөд error rate 5.16% гарсан. Сервер ойролцоогоор 5% алдаа зориудаар үүсгэдэг тул энэ үр дүн хүлээгдэж байсан бөгөөд 8%-ийн reliability threshold-оос бага байна.

Нийт checks success rate 98.27% гарсан бөгөөд 90%-ийн threshold-ийг хангаж байна.

Иймээс normal load test-ийн бүх threshold PASS болсон.

## 6. Chaos Experiment

Availability scenario-г бодитоор шалгахын тулд k6 тестийг 20 виртуал хэрэглэгчтэйгээр 2 минутын турш ажиллуулсан. Тест ажиллаж байх үед Express серверийг зориудаар зогсоож, ойролцоогоор 10 секундийн дараа дахин ажиллуулсан.

### Туршилтын нөхцөл

* Virtual users: 20 VU
* Duration: 2 минут
* Server downtime: ойролцоогоор 10 секунд
* Availability SLO: ≥ 90%
* Time-based error budget: 12 секунд

### Chaos Test Result

| Metric                  | Threshold | Actual Result | Status |
| ----------------------- | --------: | ------------: | ------ |
| Availability / checks   |     > 90% |        85.68% | FAIL   |
| `/pay` error rate       |      < 8% |        18.05% | FAIL   |
| `/cart/add` p95 latency |   < 50 ms |       2.84 ms | PASS   |
| `/report` p95 latency   |  < 450 ms |     389.24 ms | PASS   |

Нийт 5715 хүсэлтээс 4897 хүсэлт амжилттай, 818 хүсэлт амжилтгүй болсон.

### Request-based Availability

Бодит availability-г амжилттай хүсэлтийг нийт хүсэлтэд харьцуулж тооцов.

```text
Availability = successful requests / total requests × 100
             = 4897 / 5715 × 100
             = 85.68%
```

Availability SLO нь 90% байсан боловч бодит request-based availability 85.68% гарсан тул availability threshold FAIL болсон.

Request-based error budget нь нийт хүсэлтийн 10% байна.

```text
5715 × 0.10 = 571.5
```

Иймээс ойролцоогоор 571 хүртэл failed request зөвшөөрөгдөх боломжтой байсан. Бодит туршилтаар 818 хүсэлт амжилтгүй болсон тул request-based error budget хэтэрсэн.

### Time-based болон Request-based Error Budget

Availability SLO 90%, туршилтын хугацаа 120 секунд тул time-based error budget:

```text
120 × (1 - 0.90)
= 12 секунд
```

Серверийг ойролцоогоор 10 секунд зогсоосон тул хугацаагаар тооцсон 12 секундийн error budget дотор багтаж байгаа мэт харагдана.

Гэсэн хэдий ч k6-ийн `checks` нь хугацааны хувийг биш, хүсэлтийн амжилтын хувийг хэмждэг. Сервер хэвийн ажиллах үед `/report` endpoint 200–400 ms сааталтай байдаг боловч сервер унтарсан үед хүсэлтүүд `connection refused` байдлаар маш хурдан амжилтгүй буцдаг. Иймээс downtime-ийн богино хугацаанд олон failed request үүсэж, request-based availability 85.68% хүртэл буурсан.

### Availability ба Reliability

Chaos туршилтаар `/pay` endpoint-ийн error rate 18.05% болж, 8%-ийн reliability threshold мөн FAIL болсон.

Энэ нь сервер унтарсан хугацаанд `/pay` хүсэлтүүдийн ердийн 5%-ийн application-level алдаанаас гадна сервертэй холбогдох боломжгүй болсон хүсэлтүүд мөн failure гэж тооцогдсонтой холбоотой.

Иймээс нэг server crash нь availability болон reliability гэсэн хоёр SLO-д зэрэг нөлөөлсөн.

Availability болон application reliability-г илүү зөв тусгаарлахын тулд server connectivity failure болон `/pay` endpoint-ийн application-level HTTP 500 алдааг тусдаа custom metric эсвэл тусдаа failure төрлөөр хэмжиж болно.

## 7. Intentional Threshold Failure

k6 threshold ажиллаж байгаа эсэхийг шалгахын тулд `/report` endpoint-ийн performance threshold-ийг зориудаар `p(95) < 100 ms` болгон өөрчилж `slo-test-fail.js` файлаар туршсан.

`/report` endpoint нь 200–400 ms зориудын сааталтай тул 100 ms-ийн threshold-ийг хангах боломжгүй.

Туршилтын бодит үр дүн:

* `/report` threshold: `p(95) < 100 ms`
* Actual `/report` p95: `389 ms`
* Result: `FAIL`
* k6 exit code: `99`

Бусад threshold-үүд:

* `/cart/add` p95: `2.94 ms` — PASS
* `/pay` error rate: `4.93%` — PASS
* Checks success rate: `98.35%` — PASS

Ингэснээр зөвхөн `/report`-ийн зориуд эвдсэн threshold FAIL болсон. k6 нь threshold зөрчигдөх үед non-zero exit code буцааж байгаа тул CI pipeline чанарын шаардлага хангаагүй build-ийг автоматаар зогсоох боломжтой.
