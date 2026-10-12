#!/usr/bin/env python3
"""F.CSA313 lab6 helper. Two phases: a -> commit; b -> commit. No git mutations.

Run from ~/F.CSA313/lab6:
 python3 lab6_finish.py a --name 'Your name' --code 'Your code'
 python3 lab6_finish.py b
"""
import argparse
import csv
import json
import os
import subprocess
import sys
from pathlib import Path

LAB = Path.cwd().resolve()
REPO = LAB.parent

A_TEMPLATE = r'''

**Оюутны нэр:** {name}  
**Оюутны код:** {code}  
**Хичээл:** F.CSA313 — Программ хангамжийн чанарын баталгаа ба тест (2026)

## A. Category-Partition — POST /transfer

API хүсэлт: `POST /transfer` — `{{"from": ID, "to": ID, "amount": NUM, "currency": CODE}}`.  
Амжилттай үед `HTTP 201 {{"result":"OK"}}`, алдаа гарвал тодорхойлолтын дагуу `HTTP 200 {{"result":"ERROR_..."}}` буцаана.

### A1. Сонголт ба төлөөлөх утгууд

| Параметр | Сонголт | Төлөөлөх утга | Утга |
|---|---|---|---|
| From | Valid | 101 | Оршин байгаа, идэвхтэй данс |
| From | Frozen | 103 | Царцаагдсан данс |
| From | Missing | 9999 | Байхгүй данс |
| To | Valid | 202 | Өөр хүчинтэй данс |
| To | Missing | 9998 | Байхгүй данс |
| To | SameAsFrom | `to = from` | Ижил данс |
| Amount | Normal | 10000 MNT | Эерэг, үлдэгдэл ба лимитэд багтсан |
| Amount | ExactLimit | 50000 MNT | Өдрийн үлдсэн лимиттэй яг тэнцүү |
| Amount | Zero | 0 | Тэг утга |
| Amount | OverBalance | 100001 MNT | Үлдэгдлээс их |
| Amount | OverLimit | 50001 MNT | Өдрийн үлдсэн лимитээс их |
| Currency | Same | MNT | Дансны үндсэн валют |
| Currency | Different | USD | Ханшийн хөрвүүлэлт шаардлагатай |

**Далд орчны нөхцөл:** From дансны төлөв, дансны үлдэгдэл, өдрийн лимитийн нийт хэмжээ/зарцуулалт/үлдсэн хэмжээ, валютын ханш. Жишээ setup: `from.balance=100000 MNT`, `remainingDailyLimit=50000 MNT`, `rate(USD/MNT)=3500` (зөвхөн тестийн таамаг ханш). `OverBalance` үед зөвхөн үлдэгдлийн алдааг тусгаарлахын тулд лимитийг `200000 MNT` болгоно. `Different` валютын үед amount нь USD-ээр өгөгдөх бөгөөд хөрвүүлсэн MNT дүнгээр үлдэгдэл болон лимитийг шалгана. Эдгээр орчны төлөвийг тусдаа PICT параметр болгохгүй, Amount сонголтын утга болон бодит кейсийн setup-д тодорхойлно.

### A2. `[ERROR]`, `[SINGLE]`, `[IF/property]` хязгаарлалт

| Сонголт | Тэмдэглэгээ | Үндэслэл |
|---|---|---|
| From.Valid | property | Шилжүүлэг хийхийн тулд илгээгч данс идэвхтэй байна |
| From.Frozen | `[ERROR]` | Царцаагдсан данснаас шилжүүлэхгүй |
| From.Missing | `[ERROR]` | Илгээгч данс байхгүй |
| To.Valid | property | Хүлээн авагч хүчинтэй бөгөөд өөр данс |
| To.Missing | `[ERROR]` | Хүлээн авагч байхгүй |
| To.SameAsFrom | `[ERROR]`, `[IF]` | Ижил данс руу шилжүүлэхгүй; `From` оршин байх шаардлагатай |
| Amount.Normal | property | Дүн эерэг, хөрвүүлсэн дүн үлдэгдэл, лимитэд багтана |
| Amount.ExactLimit | `[SINGLE]`, property | Хүчинтэй заагийн утгыг гараар нэг тусгай кейсээр шалгана |
| Amount.Zero | `[ERROR]` | `amount <= 0` |
| Amount.OverBalance | `[ERROR]` | Хөрвүүлсний дараа үлдэгдэл хүрэхгүй |
| Amount.OverLimit | `[ERROR]` | Хөрвүүлсний дараа өдрийн лимит хэтэрнэ |
| Currency.Same | property | Хөрвүүлэлт шаардлагагүй |
| Currency.Different | property | Бэлдсэн ханшаар хөрвүүлэлт хийнэ |

**IF хязгаарлалт (тест сонголтын шийдвэр):**

```text
IF [From] = "Missing" THEN [Amount] = "Normal";
IF [To] = "Missing" THEN [Amount] = "Normal";
IF [To] = "SameAsFrom" THEN [From] <> "Missing";
```

Эхний хоёр IF нь банкны API-ийн заавал дагах бизнесийн дүрэм биш; олон алдааг тусгаарлан тест сонгох зорилготой хязгаарлалт бөгөөд зарим бодит олон алдаатай хүсэлтийг хамралтаас хасна. Гурав дахь нь `SameAsFrom` утгыг оршин байгаа илгээгчийн данстай холбосон семантикийн шийдвэр юм.

**`N → M` тооцоо:**

- Бүрэн олонлог: `3 × 3 × 5 × 2 = 90`.
- IF хязгаарлалтын дараа: `(2×2×5×2) + (2×1×1×2) + (1×2×1×2) = 48`.
- Нэг мөрд хамгийн ихдээ нэг `[ERROR]` байхаар сонгоход: `22` боломжит комбинаци үлдэнэ.
- Тэдгээр 22-ын `ExactLimit` бүхий 6 хувилбараас `[SINGLE]` дүрмээр нэгийг төлөөлүүлж сонговол: `22 − 6 + 1 = 17`.

**Иймээс гараар тест сонгох тооцоо: `90 → 48 → 22 → 17`.** 17 нь бүх 17 тестийг заавал хийх гэсэн үг биш, хязгаарлалтын дараах боломжит сонголтын орон зайн тоо юм. PICT-ийн pairwise гаралтын мөрийн тоо үүнтэй адил байх албагүй; PICT `ExactLimit`-ийг автоматаар `[SINGLE]` болгохгүй. A3 хүснэгтийн зориуд оруулсан давхар алдааны тусгай кейсүүд нэг алдааг тусгаарлах ердийн `[ERROR]` дүрмийн **нэмэлт** сорил юм.

**Олон алдааны oracle тогтоох таамагласан давуу эрэмбэ:**

`ERROR_NO_FROM → ERROR_FROZEN → ERROR_NO_TO → ERROR_SAME_ACCOUNT → ERROR_BAD_AMOUNT → ERROR_INSUFFICIENT → ERROR_LIMIT`.

Банкны тодорхойлолт олон алдаа зэрэг илэрвэл ямар хариу буцаахыг заагаагүй тул эхлээд From данс, дараа нь To данс, эцэст нь дүн, үлдэгдэл, лимитийг шалгана гэж **тест дизайны таамаг** тогтоов; үүнийг бодит хэрэгжүүлэлт баталгаажаагүй.

### A3. Спецификацийн хүснэгт

| № | From | To | Amount | Currency | Хүлээгдэх статус, result |
|---:|---|---|---|---|---|
| 1 | Valid | Valid | Normal | Same | `201 OK` |
| 2 | Valid | Valid | Normal | Different | `201 OK` |
| 3 | Valid | Valid | ExactLimit | Same | `201 OK` — SINGLE |
| 4 | Missing | Valid | Normal | Same | `200 ERROR_NO_FROM` |
| 5 | Frozen | Valid | Normal | Same | `200 ERROR_FROZEN` |
| 6 | Valid | Missing | Normal | Same | `200 ERROR_NO_TO` |
| 7 | Valid | SameAsFrom | Normal | Same | `200 ERROR_SAME_ACCOUNT` |
| 8 | Valid | Valid | Zero | Same | `200 ERROR_BAD_AMOUNT` |
| 9 | Valid | Valid | OverBalance | Same | `200 ERROR_INSUFFICIENT` |
| 10 | Valid | Valid | OverLimit | Same | `200 ERROR_LIMIT` |
| 11 | Frozen | Missing | Normal | Same | `200 ERROR_FROZEN` — давхар алдаа, давуу эрэмбэ |
| 12 | Frozen | SameAsFrom | Normal | Different | `200 ERROR_FROZEN` — давхар алдаа, давуу эрэмбэ |

**Тайлбар:** 2-р мөрийн `Normal/Different` бодит утгыг 10 USD = 35000 MNT гэж авна; 12-р мөрийн 10 USD дүн болон 100000 MNT үлдэгдэл, 50000 MNT лимит нь хэвийн боловч Frozen ба SameAsFrom алдаанууд давхар оролцоно. `OverBalance`-д үлдсэн лимитийг 200000 MNT болгож алдааг тусгаарлана. `OverLimit`-д үлдэгдэл 100000 MNT, лимит 50000 MNT байна.
'''

MODELS = {
    'browser.model': '''Content: Allow, Restrict, Block\nCookies: Allow, Restrict, Block\nPopups: Yes, No\nAddons: Yes, No\nAttacks: Yes, No\nForgeries: Yes, No\n''',
    'transfer-nc.model': '''From: Valid, Frozen, Missing\nTo: Valid, Missing, SameAsFrom\nAmount: Normal, ExactLimit, Zero, OverBalance, OverLimit\nCurrency: Same, Different\n''',
    'transfer.model': '''From: Valid, Frozen, Missing\nTo: Valid, Missing, SameAsFrom\nAmount: Normal, ExactLimit, Zero, OverBalance, OverLimit\nCurrency: Same, Different\n\nIF [From] = "Missing" THEN [Amount] = "Normal";\nIF [To] = "Missing" THEN [Amount] = "Normal";\nIF [To] = "SameAsFrom" THEN [From] <> "Missing";\n''',
    'transfer-neg.model': '''From: Valid, ~Frozen, ~Missing\nTo: Valid, ~Missing, ~SameAsFrom\nAmount: Normal, ExactLimit, ~Zero, ~OverBalance, ~OverLimit\nCurrency: Same, Different\n\nIF [From] = "Missing" THEN [Amount] = "Normal";\nIF [To] = "Missing" THEN [Amount] = "Normal";\nIF [To] = "SameAsFrom" THEN [From] <> "Missing";\n'''
}

BAD = {'From': {'Frozen','Missing'}, 'To': {'Missing','SameAsFrom'}, 'Amount': {'Zero','OverBalance','OverLimit'}}

def v(row,key):
    return row[key].lstrip('~')

def count_errors(row):
    return sum(v(row,k) in values for k,values in BAD.items())

def read_rows(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        rows=list(csv.DictReader(f,delimiter='\t'))
    if not rows: raise RuntimeError(f'PICT файлын мөр хоосон: {path}')
    expected={'From','To','Amount','Currency'}
    if expected.issubset(rows[0].keys()) is False and path.name.startswith('transfer'):
        raise RuntimeError(f'PICT model толгой буруу: {path}: {list(rows[0])}')
    return rows

def stats(rows):
    counts=[count_errors(r) for r in rows]
    return len(rows),counts.count(0),max(counts,default=0)

def find_row(rows, pred, path):
    for i,row in enumerate(rows,2):
        if pred(row): return i,row
    raise RuntimeError(f'Тохирох PICT мөр олдсонгүй: {path}')

def testcase(title, source, line, row):
    fromval=v(row,'From'); toval=v(row,'To'); av=v(row,'Amount'); currency=v(row,'Currency')
    cur='MNT' if currency=='Same' else 'USD'
    vals={'Normal': 10000, 'ExactLimit':50000, 'Zero':0, 'OverBalance':100001, 'OverLimit':50001} if cur=='MNT' else {'Normal':10, 'ExactLimit':10, 'Zero':0, 'OverBalance':40, 'OverLimit':15}
    amount=vals[av]
    in_mnt=amount*(1 if cur=='MNT' else 3500)
    bal=100000
    limit=200000 if av=='OverBalance' else in_mnt if av=='ExactLimit' else 50000
    fromid={'Valid':101, 'Frozen':103, 'Missing':9999}[fromval]
    toid=fromid if toval=='SameAsFrom' else 9998 if toval=='Missing' else 202
    errors={'Missing':'ERROR_NO_FROM','Frozen':'ERROR_FROZEN'}
    if fromval in errors: result=errors[fromval]
    elif toval=='Missing': result='ERROR_NO_TO'
    elif toval=='SameAsFrom': result='ERROR_SAME_ACCOUNT'
    elif av=='Zero': result='ERROR_BAD_AMOUNT'
    elif av=='OverBalance': result='ERROR_INSUFFICIENT'
    elif av=='OverLimit': result='ERROR_LIMIT'
    else: result='OK'
    http=201 if result=='OK' else 200
    body={'from':fromid,'to':toid,'amount':amount,'currency':cur}
    pict=' / '.join(f'{k}={row[k]}' for k in ('From','To','Amount','Currency'))
    setup=(f'`from={fromid}` ({"байхгүй" if fromval=="Missing" else "царцаагдсан" if fromval=="Frozen" else "идэвхтэй"}), '
           f'`to={toid}` ({"байхгүй" if toval=="Missing" else "ижил данс" if toval=="SameAsFrom" else "идэвхтэй"}), '
           f'`balance={bal} MNT`, `remainingDailyLimit={limit} MNT`, `1 USD=3500 MNT` (жишээ ханш). '
           f'Хөрвүүлсний дараах amount: `{in_mnt} MNT`.')
    return (f'#### {title}\n\n**PICT эх сурвалж:** `results/{source}.txt` файлын {line}-р мөр — `{pict}`.\n\n'
            f'**Setup:** {setup}\n\n**Оролт:**\n\n```json\n{json.dumps(body,indent=2,ensure_ascii=False)}\n```\n\n'
            f'**Oracle:** `HTTP {http}`, `{{"result":"{result}"}}`. '
            + ('Давхар алдааны үед README-ийн давуу эрэмбээр эхний алдааг сонгосон.' if count_errors(row)>1 else 'Бодит гүйлгээг ажиллуулаагүй: энэ нь спецификацид суурилсан хүлээлт.') + '\n\n')

def part_a(name,code):
    if not (LAB/'results'/'pict-build.txt').exists():
        raise RuntimeError('Эхлээд results/pict-build.txt бэлд.')
    path=LAB/'README.md'
    if path.exists():
        raise RuntimeError('README.md файл аль хэдийн байна. Өмнөх ажлаа устгахгүй. Эхлээд одоогийн README-г шалгаад шаардлагатай бол нэрийг нь сольж хадгал.')
    path.write_text(A_TEMPLATE.format(name=name,code=code),encoding='utf-8')
    print('A1, A2, A3 бэлэн:',path)

def part_b():
    if not (LAB/'README.md').exists(): raise RuntimeError('Эхлээд A хэсгийг үүсгэ.')
    readme=(LAB/'README.md').read_text(encoding='utf-8')
    if '\n## B. PICT' in readme: raise RuntimeError('B тайлан README дотор аль хэдийн байна. Давхар оруулахгүй.')
    for name,content in MODELS.items():
        path=LAB/name
        if path.exists() and path.read_text(encoding='utf-8')!=content:
            raise RuntimeError(f'{name} файл өмнө нь байгаа бөгөөд өөр агуулгатай. Өөрчлөлтөө гараар шалга.')
    for name,content in MODELS.items(): (LAB/name).write_text(content,encoding='utf-8')
    specs=[('browser-2way','browser.model',[]),('browser-3way','browser.model',['/o:3']),('transfer-nc','transfer-nc.model',[]),('transfer','transfer.model',[]),('transfer-neg','transfer-neg.model',[])]
    (LAB/'results').mkdir(exist_ok=True)
    for name,model,opts in specs:
        proc=subprocess.run(['pict',model,*opts],cwd=LAB,capture_output=True,text=True)
        if proc.returncode!=0 or not proc.stdout.strip():
            raise RuntimeError(f'{model} PICT алдаа: '+(proc.stderr or proc.stdout))
        if proc.stderr.strip():
            raise RuntimeError(f'{model} PICT stderr: '+proc.stderr)
        (LAB/'results'/f'{name}.txt').write_text(proc.stdout,encoding='utf-8')
    rows={k:read_rows(LAB/'results'/f'{k}.txt') for k in ['transfer-nc','transfer','transfer-neg']}
    browser_count={k: len(read_rows(LAB/'results'/f'{k}.txt')) for k in ['browser-2way','browser-3way']}
    s={k:stats(r) for k,r in rows.items()}
    assert s['transfer-neg'][2] <= 1, 'transfer-neg загварт нэгээс олон алдаатай мөр байна.'
    case1=find_row(rows['transfer-neg'],lambda r:count_errors(r)==0 and v(r,'From')=='Valid' and v(r,'To')=='Valid','transfer-neg')
    case2=find_row(rows['transfer-neg'],lambda r:v(r,'From')=='Missing' and count_errors(r)==1,'transfer-neg')
    case3=find_row(rows['transfer-neg'],lambda r:v(r,'Amount')=='OverLimit' and count_errors(r)==1,'transfer-neg')
    case4=find_row(rows['transfer'],lambda r:v(r,'From')=='Frozen' and v(r,'To')=='Missing','transfer')
    comp='олон' if browser_count['browser-2way']>9 else 'цөөн' if browser_count['browser-2way']<9 else 'ижил'
    b=(f'\n## B. PICT — pairwise covering array\n\n'
       f'### B1. Browser: 2-way ба 3-way\n\n'
       f'| Тест сонгох арга | Мөрийн тоо |\n|---|---:|\n'
       f'| Бүрэн олонлог (`3×3×2×2×2×2`) | 144 |\n'
       f'| Лекц дээрх гараар 2-way | 9 |\n'
       f'| PICT browser 2-way (`results/browser-2way.txt`) | {browser_count["browser-2way"]} |\n'
       f'| PICT browser 3-way (`results/browser-3way.txt`) | {browser_count["browser-3way"]} |\n\n'
       f'PICT 2-way нь лекцийн 9 мөртэй харьцуулахад **{comp}** ({browser_count["browser-2way"]} мөр) гарсан. '
       f'PICT-ийн greedy алгоритм нь тухайн алхамд олон шинэ хос хамруулах сонголт хийдэг тул хамгийн цөөн мөрийг заавал олохгүй. '
       f'3-way нь гурван параметрийн хослолыг хамрах шаардлагаас шалтгаалан илүү өргөн хамралт шаардах бөгөөд '
       f'энэ модельд {browser_count["browser-3way"]} мөр гарсан нь бүрэн олонлог 144 мөртэй харьцуулахад {144-browser_count["browser-3way"]} мөрөөр цөөн байна.\n\n'
       '### B2. Transfer: IF болон `~` сөрөг утгын харьцуулалт\n\n'
       '| Үзүүлэлт | transfer-nc | transfer | transfer-neg |\n|---|---:|---:|---:|\n'
       f'| Нийт мөр | {s["transfer-nc"][0]} | {s["transfer"][0]} | {s["transfer-neg"][0]} |\n'
       f'| Happy path (`ERROR` байхгүй) | {s["transfer-nc"][1]} | {s["transfer"][1]} | {s["transfer-neg"][1]} |\n'
       f'| Нэг мөрийн хамгийн их ERROR | {s["transfer-nc"][2]} | {s["transfer"][2]} | {s["transfer-neg"][2]} |\n'
       '| IF хязгаарлалт | Үгүй | Тийм | Тийм |\n'
       '| `~` negative тэмдэглэгээ | Үгүй | Үгүй | Тийм |\n\n'
       'Хязгаарлалтгүй болон IF-тэй загварт алдааны утгууд энгийн утгатай адил хосолж болох тул нэг мөр олон ERROR агуулж, '
       'эхний алдаа бусдыг нуух (`error masking`) эрсдэл үүснэ. `~` тэмдэгтэй ERROR утгуудыг PICT нэг мөрөнд хамгийн ихдээ '
       'нэг сөрөг утга байхаар сонгодог тул алдааны семантикийг тусгаарлана. Гэвч `~` нь сонголтуудын IF хамаарлыг орлохгүй, '
       'тиймээс A2-ын IF хязгаарлалт `transfer-neg.model` дотор хэвээр шаардлагатай. '
       'PICT нь `[SINGLE]`-ийг тусгайлан хэрэгжүүлээгүй учраас ExactLimit нь хэд хэдэн тестэд байж болно.\n\n'
       '### B2.1. PICT гаралтаас боловсруулсан бодит тест кейсүүд\n\n')
    b+=testcase('Тест 1 — Happy path','transfer-neg',*case1)
    b+=testcase('Тест 2 — Илгээгчийн данс байхгүй (`~Missing`)','transfer-neg',*case2)
    b+=testcase('Тест 3 — Өдрийн лимит хэтэрсэн (`~OverLimit`)','transfer-neg',*case3)
    b+=testcase('Тест 4 — Давхар алдаа (Frozen + Missing)','transfer',*case4)
    b+=('### B3. Хоёр аргын харьцуулалт ба дүгнэлт (9 өгүүлбэр)\n\n'
        'Category-Partition нь банкны шилжүүлгийн шаардлагыг шинжлэн сонголт, төлөөлөх утга, хязгаарлалтыг тодорхойлоход тусалсан. '
        'Энэ арга нь алдааны нөхцөл бүрийн хүлээгдэх хариуг ил тод заадаг давуу талтай. '
        'Гараар спецификаци гаргах явцад олон алдааны давуу эрэмбийг тогтоох нь хамгийн их бодол шаардсан хэсэг байсан. '
        'PICT нь параметрүүдийн pairwise хамралтыг автоматаар бий болгож, олон комбинацыг системтэйгээр сонгодог. '
        'Гэхдээ greedy алгоритм нь хамгийн цөөн мөрийн тоог баталгаажуулдаггүй. '
        'Алдааг энгийн утгаар загварчлахад error masking үүсэж болох нь модель хоорондын харьцуулалтаар харагдлаа. '
        'Negative утгыг `~` тэмдэглэхэд нэг мөрөнд хамгийн ихдээ нэг ERROR сонгогдох бөгөөд oracle илүү тодорхой болно. '
        'Гэсэн ч `~` тэмдэглэгээ нь IF нөхцөлийг орлохгүй, харин Category-Partition-ийн `[SINGLE]` дүрмийг PICT автоматаар хэрэгжүүлдэггүй. '
        'Иймээс алдааны семантикийг Category-Partition аргаар тодорхойлж, параметрүүдийн хосын хамралтыг PICT-ээр үүсгэх нь бие биеэ нөхөх арга юм.\n')
    (LAB/'README.md').write_text(readme+b,encoding='utf-8')
    print('B хэсэг бэлэн; PICT бодит мөрийг README-д автоматаар оруулав.')
    for name,n in browser_count.items():print(name,n)
    for name,vals in s.items():print(name,'total/happy/max-errors',*vals)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('stage',choices=['a','b'])
    p.add_argument('--name',default='[ОВОГ НЭРЭЭ БИЧ]')
    p.add_argument('--code',default='[ОЮУТНЫ КОДОО БИЧ]')
    args=p.parse_args()
    if LAB.name != 'lab6': print('САНУУЛГА: ~/F.CSA313/lab6 дотороос ажиллуул.',file=sys.stderr);sys.exit(2)
    if args.stage == 'a' and (not args.name.strip() or not args.code.strip() or args.name.startswith('[') or args.code.startswith('[')):
        p.error('A үе шатанд заавал --name болон --code бодит утгаар өгнө.')
    try:
        if args.stage=='a':part_a(args.name,args.code)
        else:part_b()
    except (RuntimeError,FileNotFoundError) as e:
        print('АЛДАА:',e,file=sys.stderr)
        sys.exit(1)
