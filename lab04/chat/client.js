import { createInterface } from 'node:readline';
import { pathToFileURL } from 'node:url';
import { io } from 'socket.io-client';

export function connectClient(clientId, onMessage, onConnect) {
  if (!Number.isSafeInteger(clientId) || clientId < 1) {
    throw new Error('Expected a positive integer client ID');
  }

  const options = { auth: { clientId }, timeout: 1500, autoConnect: false };
  const standby = io('http://127.0.0.1:8002', options);
  const primary = clientId % 2 === 0
    ? io('http://127.0.0.1:8001', { ...options, reconnection: false })
    : standby;
  let socket = primary;

  standby.on('connect', () => onConnect('B'));
  standby.on('message', onMessage);

  if (primary !== standby) {
    const failover = () => {
      if (socket !== primary) return;
      socket = standby;
      primary.disconnect();
      standby.connect();
    };
    primary.on('connect_error', failover);
    primary.on('disconnect', failover);
    primary.on('connect', () => onConnect('A'));
    primary.on('message', onMessage);
  }

  primary.connect();
  return {
    send(text) {
      if (!socket.connected) return false;
      socket.emit('message', text);
      return true;
    },
    close() {
      const active = socket;
      socket = standby;
      active.disconnect();
    },
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const id = Number(process.argv[2]);
  if (!Number.isSafeInteger(id) || id < 1) {
    console.error('Usage: node client.js <positive integer ID>');
    process.exit(1);
  }
  const client = connectClient(
    id,
    ({ clientId, serverId, text }) => console.log(`[${serverId}/${clientId}] ${text}`),
    (server) => console.log(`Client ${id} connected to ${server}. Type a message.`),
  );
  const input = createInterface({ input: process.stdin, output: process.stdout });
  input.on('line', (line) => {
    if (line.trim() && !client.send(line)) console.log('Waiting for a connection. Send again once connected.');
  });
  input.on('close', () => client.close());
}
