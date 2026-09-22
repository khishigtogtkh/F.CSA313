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

## Орчны мэдээлэл

### Node.js

```bash
node --version
```

### npm

```bash
npm --version
```

### k6

```bash
k6 version
```

`k6 version` командын бодит гаралтыг энд оруулна.

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
* [ ] Quality scenario бичих
* [ ] SLO тодорхойлох
* [ ] k6 threshold хэрэгжүүлэх
* [ ] PASS test хийх
* [ ] Chaos test хийх
* [ ] Intentional FAIL test хийх
