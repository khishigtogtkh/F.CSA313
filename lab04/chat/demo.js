import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { setTimeout } from 'node:timers/promises';
import { connectClient } from './client.js';

const servers = [];
const clients = [];
const serverLog = [];
const routes = new Map();
const deliveries = [];

function startServer(id) {
  const child = spawn(process.execPath, ['server.js', id], { stdio: ['ignore', 'pipe', 'inherit'] });
  servers.push(child);
  child.stdout.setEncoding('utf8').on('data', (chunk) => {
    serverLog.push(chunk);
    process.stdout.write(chunk);
  });
  return child;
}

async function waitFor(check, description) {
  const deadline = Date.now() + 7000;
  while (!check()) {
    assert(Date.now() < deadline, `Timed out: ${description}`);
    await setTimeout(20);
  }
}

function openClient(id) {
  const client = connectClient(id, (message) => {
    deliveries.push({ recipient: id, ...message });
  }, (server) => {
    routes.set(id, server);
    console.log(`Client ${id} -> Server ${server}`);
  });
  clients.push(client);
  return client;
}

async function verifyMessage(client, text, sender, origin, recipients) {
  assert(client.send(text));
  const matching = () => deliveries.filter((message) => message.text === text);
  await waitFor(() => matching().length >= recipients.length, text);
  await setTimeout(100);
  assert.deepEqual(matching().map(({ recipient }) => recipient).sort((a, b) => a - b), recipients);
  assert(matching().every(({ clientId, serverId }) => clientId === sender && serverId === origin));
  console.log(`PASS "${text}" from ${origin}/${sender} reached [${recipients.join(', ')}] once each`);
}

try {
  startServer('B');
  const serverA = startServer('A');
  await waitFor(() => serverLog.join('').includes('Server A linked to B'), 'server relay');
  const [one, two, three] = [1, 2, 3, 4].map(openClient);
  await waitFor(() => routes.size === 4, 'four clients connected');
  for (const [id, server] of [[1, 'B'], [2, 'A'], [3, 'B'], [4, 'A']]) {
    assert.equal(routes.get(id), server);
  }
  console.log('PASS balanced routing: A=[2, 4], B=[1, 3]');
  await verifyMessage(two, 'A to B', 2, 'A', [1, 2, 3, 4]);
  await verifyMessage(one, 'B to A', 1, 'B', [1, 2, 3, 4]);

  const stopped = once(serverA, 'exit');
  assert(serverA.kill());
  await stopped;
  console.log('Server A stopped');
  await waitFor(() => routes.get(2) === 'B' && routes.get(4) === 'B', 'A clients reconnected to B');
  await verifyMessage(three, 'B stays available', 3, 'B', [1, 2, 3, 4]);
  const six = openClient(6);
  await waitFor(() => routes.get(6) === 'B', 'new even client routed to B');
  await verifyMessage(six, 'New client after A stopped', 6, 'B', [1, 2, 3, 4, 6]);
} finally {
  for (const client of clients) client.close();
  for (const server of servers) server.kill();
}
