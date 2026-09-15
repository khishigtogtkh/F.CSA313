# Лаборатори №2 — Гүйцэтгэлийн хэмжүүрийг k6-аар хэмжих

**Хичээл:** F.CSA313 — Программ хангамжийн чанарын баталгаа ба тест (2026)

## Зорилго

Энэхүү лабораторийн ажлын зорилго нь Grafana k6 ашиглан веб системийн гүйцэтгэлийг бодитоор хэмжиж, ачаалал нэмэгдэхэд latency, throughput болон error rate хэрхэн өөрчлөгдөхийг ажиглах явдал юм.

Туршилтыг зөвшөөрөгдсөн `https://test.k6.io` хаяг дээр хийсэн.

---

## Орчин

- OS: Ubuntu / WSL2
- Load testing tool: Grafana k6
- Target: `https://test.k6.io`
- k6 version: **энд `k6 version` командын өөрийн гаралтыг оруулна**

---

## 1. Үндсэн тест — Baseline

Эхний туршилтыг 5 VU, 30 секундийн тохиргоогоор ажиллуулсан.

```javascript
import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  vus: 5,
  duration: '30s',
};

export default function () {
  const res = http.get('https://test.k6.io');

  check(res, {
    'status 200 байна': (r) => r.status === 200,
  });

  sleep(1);
}
```

Baseline туршилтын гол үр дүн:

| Metric | Үр дүн |
|---|---:|
| Average latency | 213.76 ms |
| p90 latency | 406.18 ms |
| p95 latency | 565.67 ms |
| Error rate | 0.00% |

Энэ туршилтын `p95 = 565.67 ms` утгыг дараагийн SLO threshold тодорхойлох baseline болгон ашигласан.

---

## 2. 5 / 30 / 100 VU харьцуулалт

Ачааллын түвшин тус бүрийг 1 минутын хугацаанд тусад нь ажиллуулсан.

```bash
k6 run --vus 5 --duration 1m script.js | tee results/run-05vu.txt
k6 run --vus 30 --duration 1m script.js | tee results/run-30vu.txt
k6 run --vus 100 --duration 1m script.js | tee results/run-100vu.txt
```

### Хэмжилтийн үр дүн

| VU | p90 latency | p95 latency | Throughput (`http_reqs/s`) | Error rate |
|---:|---:|---:|---:|---:|
| 5 | 277.86 ms | 363.70 ms | 7.088537 req/s | 0.00% |
| 30 | 218.18 ms | 222.06 ms | 43.822178 req/s | 0.00% |
| 100 | 219.55 ms | 223.41 ms | 143.96188 req/s | 0.00% |

### Ажиглалт

5 VU-ээс 100 VU хүртэл ачаалал нэмэгдэхэд throughput мэдэгдэхүйц өссөн. Харин latency тогтмол өсөх хандлага ажиглагдаагүй. 5 VU үед p95 хамгийн өндөр буюу `363.70 ms` байсан бол 30 болон 100 VU үед ойролцоогоор `222–223 ms` байсан. Бүх туршилтад error rate `0.00%` гарсан.

---

## 3. Stages туршилт

Ачааллыг шатлан өсгөж, дараа нь бууруулахын тулд дараах stages тохиргоог ашигласан.

```javascript
export const options = {
  stages: [
    { duration: '30s', target: 5 },
    { duration: '1m', target: 30 },
    { duration: '30s', target: 100 },
    { duration: '30s', target: 0 },
  ],
};
```

Ажиллуулах команд:

```bash
k6 run stages.js | tee results/run-stages.txt
```

### Stages туршилтын summary

| Metric | Үр дүн |
|---|---:|
| Checks | 3544 |
| Checks succeeded | 100.00% |
| p90 latency | 220.69 ms |
| p95 latency | 225.60 ms |
| Error rate | 0.00% |
| HTTP requests | 7088 |
| Throughput | 44.959603 req/s |
| Maximum VU | 100 |

Stages туршилтын үед 100 хүртэл VU хүрсэн ч HTTP request failure гараагүй бөгөөд p95 latency `225.60 ms` байсан.

---

## 4. SLO болон Threshold

Baseline туршилтын p95 latency:

```text
565.67 ms
```

SLO-г baseline-ийн 1.5 дахин өсөлтөөр тооцсон:

```text
565.67 × 1.5 = 848.505 ms
```

Тиймээс SLO-г ойролцоогоор:

```text
p95 latency < 850 ms
error rate < 1%
```

гэж тодорхойлсон.

Threshold тохиргоо:

```javascript
export const options = {
  vus: 30,
  duration: '1m',

  thresholds: {
    http_req_duration: ['p(95)<850'],
    http_req_failed: ['rate<0.01'],
  },
};
```

---

## 5. Threshold PASS туршилт

SLO threshold-ийг бодит ачаалал дээр шалгасан.

### Үр дүн

| Metric | Үр дүн |
|---|---:|
| p90 latency | 222.19 ms |
| p95 latency | 229.07 ms |
| Error rate | 0.00% |
| Throughput | 44.532581 req/s |
| Maximum VU | 30 |

`p95 = 229.07 ms` нь `850 ms`-ээс бага, мөн error rate `0.00%` байсан тул SLO **PASS** болсон.

```text
p95 229.07 ms < 850 ms  → PASS
error rate 0.00% < 1%   → PASS
```

---

## 6. Threshold FAIL туршилт

Quality gate хэрхэн FAIL болдгийг шалгахын тулд p95 threshold-ийг санаатайгаар хэт хатуу болгож:

```javascript
thresholds: {
  http_req_duration: ['p(95)<50'],
  http_req_failed: ['rate<0.01'],
}
```

гэж тохируулсан.

### Үр дүн

| Metric | Үр дүн |
|---|---:|
| Average latency | 230 ms |
| p90 latency | 251.28 ms |
| p95 latency | 304.79 ms |
| Error rate | 0.00% |
| Throughput | 37.859003 req/s |
| Maximum VU | 30 |

Бодит p95 latency `304.79 ms` байсан тул:

```text
304.79 ms > 50 ms → FAIL
```

гэж гарсан.

k6 дараах threshold error-ийг үзүүлсэн:

```text
ERRO[0062] thresholds on metrics 'http_req_duration' have been crossed
```

Энэ нь CI/CD pipeline дахь performance quality gate ажиллах зарчмыг харуулж байна.

---

## 7. Дүгнэлт

Энэ лабораторийн ажлаар k6 ашиглан веб системийн latency, throughput болон error rate хэмжүүрүүдийг бодитоор хэмжсэн.  
5 VU үед p95 latency `363.70 ms` байсан бол 30 болон 100 VU үед тус тус `222.06 ms`, `223.41 ms` гарсан тул энэ удаагийн туршилтаар ачаалал өсөхөд latency тогтмол өссөнгүй.  
Харин throughput 5 VU үед `7.09 req/s` орчмоос 100 VU үед `143.96 req/s` хүртэл өссөн нь олон зэрэгцээ хүсэлтийг систем боловсруулж чадсаныг харуулсан.  
5, 30, 100 VU-ийн бүх туршилтад error rate `0.00%` байсан тул хүсэлтүүд амжилттай боловсруулагдсан.  
Stages туршилтаар ачааллыг 5-аас 30, дараа нь 100 VU хүртэл өсгөхөд p95 latency `225.60 ms`, error rate `0.00%` байсан.  
Baseline p95 `565.67 ms` дээр үндэслэн 1.5 коэффициент ашиглаж `p95 < 850 ms` гэсэн SLO тодорхойлсон.  
PASS туршилтаар p95 `229.07 ms` гарсан тул тодорхойлсон SLO амжилттай хангагдсан.  
Харин `p95 < 50 ms` гэсэн санаатай хатуу threshold ашиглахад бодит p95 `304.79 ms` байсан учир тест FAIL болж, k6 threshold quality gate зөв ажиллаж байгааг харуулсан.  
Ингэснээр latency, throughput, error rate, SLO болон threshold нь системийн гүйцэтгэлийг хэмжих, хянахад хэрхэн ашиглагддагийг практик туршилтаар баталгаажуулсан.

---

## 8. Үр дүнгийн файлууд

```text
results/
├── run-05vu.txt
├── run-30vu.txt
├── run-100vu.txt
├── run-stages.txt
├── threshold-pass.txt
└── threshold-fail.txt
```

README доторх хэмжилтийн утгууд нь дээрх k6-ийн бүтэн текст гаралтуудтай таарч байх ёстой.

---

## 9. Screenshot нотолгоо

Репозиторийн `screenshots/` хавтсанд дараах screenshot-уудыг хадгална:

```text
screenshots/
├── baseline.png
├── run-05vu.png
├── run-30vu.png
├── run-100vu.png
├── stages.png
├── threshold-pass.png
└── threshold-fail.png
```

---

## 10. Репозиторийн бүтэц

```text
lab2/
├── script.js
├── stages.js
├── threshold-pass.js
├── threshold-fail.js
├── README.md
├── results/
│   ├── run-05vu.txt
│   ├── run-30vu.txt
│   ├── run-100vu.txt
│   ├── run-stages.txt
│   ├── threshold-pass.txt
│   └── threshold-fail.txt
└── screenshots/
    ├── baseline.png
    ├── run-05vu.png
    ├── run-30vu.png
    ├── run-100vu.png
    ├── stages.png
    ├── threshold-pass.png
    └── threshold-fail.png
```
