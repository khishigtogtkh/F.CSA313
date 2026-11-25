import { createServer } from 'node:http';
import { Server } from 'socket.io';
import { io as connectSocket } from 'socket.io-client';

const serverId = process.argv[2];
if (serverId !== 'A' && serverId !== 'B') {
  console.error('Usage: node server.js A|B');
  process.exit(1);
}

const port = serverId === 'A' ? 8001 : 8002;
const http = createServer();
http.on('error', (error) => {
  console.error(error.message);
  process.exitCode = 1;
  peer?.disconnect();
});
const io = new Server(http);
const clients = new Map();

function logClients() {
  console.log(`Server ${serverId} clients: [${[...clients.values()].join(', ')}]`);
}

function receiveFromPeer(message) {
  io.emit('message', message);
}

const peerNamespace = io.of('/peer');
const peer = serverId === 'A' ? connectSocket('http://127.0.0.1:8002/peer') : null;
if (peer) {
  peer.on('connect', () => console.log('Server A linked to B'));
  peer.on('relay', receiveFromPeer);
} else {
  peerNamespace.on('connection', (socket) => {
    socket.on('relay', receiveFromPeer);
  });
}

io.use((socket, next) => {
  const { clientId } = socket.handshake.auth;
  if (!Number.isSafeInteger(clientId) || clientId < 1) {
    return next(new Error('Expected a positive integer client ID'));
  }
  socket.data.clientId = clientId;
  next();
});

io.on('connection', (socket) => {
  const { clientId } = socket.data;
  clients.set(socket.id, clientId);
  logClients();

  socket.on('message', (text) => {
    if (typeof text !== 'string' || !text.trim()) return;
    const message = { clientId, serverId, text: text.trim() };
    io.emit('message', message);
    if (peer) {
      if (peer.connected) peer.emit('relay', message);
    } else {
      peerNamespace.emit('relay', message);
    }
  });

  socket.on('disconnect', () => {
    clients.delete(socket.id);
    logClients();
  });
});

http.listen(port, '127.0.0.1', () => {
  console.log(`Server ${serverId} listening on ${port}`);
});
