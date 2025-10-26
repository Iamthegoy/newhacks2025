// server.js
import express from "express";
import http from "http";
import { Server } from "socket.io";
import path from "path";
import { fileURLToPath } from "url";

// Setup __dirname (needed in ES module format)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Create Express app
const app = express();
const server = http.createServer(app);
const io = new Server(server);

// Serve static files from /public
app.use(express.static(path.join(__dirname, "public")));

// Keep track of all connected players
const players = {};

// Socket.io connection event
io.on("connection", (socket) => {
  console.log("🟢 Player connected:", socket.id);

  // Add player to list with default position
  players[socket.id] = { x: 0, y: 1.6, z: 0 };

  // Send existing players to the new client
  socket.emit("currentPlayers", players);

  // Tell everyone else a new player joined
  socket.broadcast.emit("newPlayer", { id: socket.id, ...players[socket.id] });

  // When player moves
  socket.on("move", (data) => {
    // console.log("Player moved:", socket.id, data);
    players[socket.id] = data;
    socket.broadcast.emit("playerMoved", { id: socket.id, ...data });
  });


  // Audio data relay
  socket.on("audio", data => {
    socket.broadcast.emit("audio", data);
  });

  // When player disconnects
  socket.on("disconnect", () => {
    console.log("🔴 Player disconnected:", socket.id);
    delete players[socket.id];
    io.emit("playerDisconnected", socket.id);
  });
});

// Start local server
const PORT = 3000;
server.listen(PORT, () => console.log(`✅ Server running at http://localhost:${PORT}`));
