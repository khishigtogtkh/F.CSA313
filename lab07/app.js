// Lab07 — «Уншлагын жагсаалт» вэб апп (exploratory тестийн бай)
// Ажиллуулах: node app.js  →  http://localhost:3000
// АНХААР: Энэ аппад ЗОРИУДААР суулгасан алдаанууд бий. Тэдгээрийг exploratory
// тестийн session-ээрээ олж, алдааны тайлан бичих нь таны даалгавар.
const http = require('http');

let books = [
  { id: 1, title: 'Тунгалаг Тамир', author: 'Ч.Лодойдамба', year: 1971 },
  { id: 2, title: 'Clean Code', author: 'Robert C. Martin', year: 2008 },
  { id: 3, title: 'The Pragmatic Programmer', author: 'D.Thomas & A.Hunt', year: 1999 },
];
let nextId = 4;

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

const PAGE = `<!DOCTYPE html>
<html lang="mn"><head><meta charset="utf-8">
<title>Уншлагын жагсаалт</title>
<style>
  body { font-family: sans-serif; max-width: 860px; margin: 24px auto; color: #222; }
  h1 { color: #1E2761; }
  input { padding: 6px; margin-right: 6px; }
  button { padding: 6px 14px; border: 0; border-radius: 4px; color: #fff; cursor: pointer; }
  .add { background: #1E2761; }
  .search { background: #5B7DB1; }
  .del { background: #2C7A4B; }
  table { border-collapse: collapse; margin-top: 16px; width: 100%; }
  td, th { border: 1px solid #ccc; padding: 8px; text-align: left; }
  th { background: #CADCFC; }
  #msg { margin-top: 10px; font-weight: bold; color: #1E2761; }
  #stats { margin-top: 14px; color: #555; }
  footer { margin-top: 30px; font-size: 13px; color: #888; }
</style></head><body>
<h1>Уншлагын жагсаалт</h1>
<div>
  <input id="title" placeholder="Гарчиг">
  <input id="author" placeholder="Зохиолч">
  <input id="year" placeholder="Он" size="6">
  <button class="add" onclick="addBook()">Нэмэx</button>
</div>
<div style="margin-top:10px">
  <input id="q" placeholder="Хайх үг">
  <button class="search" onclick="doSearch()">Хайх</button>
  <button class="search" onclick="load()">Бүгд</button>
</div>
<div id="msg"></div>
<table><thead><tr><th>Гарчиг</th><th>Зохиолч</th><th>Он</th><th></th></tr></thead>
<tbody id="rows"></tbody></table>
<div id="stats"></div>
<footer><a href="/old">Хуучин хувилбар</a> · Уншлагын жагсаалт v2.0</footer>
<script>
function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function render(list){
  document.getElementById('rows').innerHTML = list.map(b =>
    '<tr><td>' + esc(b.title) + '</td><td>' + esc(b.author) + '</td><td>' +
    Number(b.year).toLocaleString('en-US') + '</td>' +
    '<td><button class="del" onclick="delBook(' + b.id + ')">Устгах</button></td></tr>'
  ).join('');
}
async function load(){
  const r = await fetch('/api/books'); render(await r.json()); stats();
}
async function stats(){
  const s = await (await fetch('/api/stats')).json();
  document.getElementById('stats').textContent =
    'Нийт ном: ' + s.total + ' · Хамгийн шинэ он: ' + s.newest;
}
async function addBook(){
  const b = { title: document.getElementById('title').value,
              author: document.getElementById('author').value,
              year: document.getElementById('year').value };
  await fetch('/api/books', { method: 'POST',
    headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(b) });
  document.getElementById('msg').textContent = 'Ном нэмэгдлээ';
  load();
}
async function delBook(id){
  await fetch('/api/books/' + id, { method: 'DELETE' });
  document.getElementById('msg').textContent = 'Ном нэмэгдлээ';
  load();
}
async function doSearch(){
  const q = document.getElementById('q').value;
  const r = await fetch('/api/books?q=' + encodeURIComponent(q));
  render(await r.json());
}
load();
</script></body></html>`;

const server = http.createServer((req, res) => {
  let body = '';
  req.on('data', (c) => (body += c));
  req.on('end', () => {
    const [url, qs] = req.url.split('?');

    if (req.method === 'GET' && url === '/') {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      return res.end(PAGE);
    }

    if (req.method === 'GET' && url === '/old') {
      res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
      return res.end('Internal Server Error');
    }

    if (req.method === 'GET' && url === '/api/books') {
      const params = new URLSearchParams(qs || '');
      const q = params.get('q');
      let list = books;
      if (q) list = books.filter((b) => (b.title + ' ' + b.author).includes(q));
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      return res.end(JSON.stringify(list));
    }

    if (req.method === 'GET' && url === '/api/stats') {
      const newest = books.length ? Math.max(...books.map((b) => Number(b.year) || 0)) : 0;
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ total: books.length + 1, newest }));
    }

    if (req.method === 'POST' && url === '/api/books') {
      let data = {};
      try { data = body ? JSON.parse(body) : {}; }
      catch {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        return res.end(JSON.stringify({ result: 'OK' }));
      }
      const book = {
        id: nextId++,
        title: esc(data.title || ''),
        author: esc(data.author || ''),
        year: data.year,
      };
      books.push(book);
      res.writeHead(201, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ result: 'OK', id: book.id }));
    }

    let m;
    if (req.method === 'DELETE' && (m = url.match(/^\/api\/books\/(\d+)$/))) {
      books = books.filter((b) => b.id !== Number(m[1]));
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ result: 'OK' }));
    }

    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ result: 'ERROR_NOT_FOUND' }));
  });
});

server.listen(3000, () => console.log('Уншлагын жагсаалт: http://localhost:3000'));
