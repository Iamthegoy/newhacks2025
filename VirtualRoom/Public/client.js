// Connect to server
const socket = io();
const scene = document.querySelector("a-scene");
const cameraRig = document.querySelector("#cameraRig");
const usernameDisplay = document.getElementById("username");

// Generate random color and nickname
const myColor = "#" + Math.floor(Math.random() * 16777215).toString(16);
const myName = "User_" + Math.floor(Math.random() * 1000);
usernameDisplay.innerText = `You are: ${myName}`;

const players = {}; // other players in the scene

// When we receive all current players
socket.on("currentPlayers", (serverPlayers) => {
  for (const id in serverPlayers) {
    if (id !== socket.id) addAvatar(id, serverPlayers[id]);
  }
});

// When a new player joins
socket.on("newPlayer", (data) => addAvatar(data.id, data));

// When another player moves
socket.on("playerMoved", (data) => updateAvatar(data.id, data));

// When a player leaves
socket.on("playerDisconnected", (id) => removeAvatar(id));

// Add a new avatar to the world
function addAvatar(id, pos) {
  console.log("Adding avatar for", id);
  const el = document.createElement("a-box");
  el.setAttribute("color", "#" + Math.floor(Math.random() * 16777215).toString(16));
  el.setAttribute("height", "1.6");
  el.setAttribute("width", "0.5");
  el.setAttribute("depth", "0.5");
  el.setAttribute("position", `${pos.x} ${pos.y} ${pos.z}`);
  el.setAttribute("id", id);

  // Floating username
  const nameTag = document.createElement("a-text");
  nameTag.setAttribute("value", id.slice(0, 5));
  nameTag.setAttribute("color", "black");
  nameTag.setAttribute("position", "0 1 0");
  nameTag.setAttribute("align", "center");
  el.appendChild(nameTag);

  scene.appendChild(el);
  players[id] = el;
}

// Update avatar position
function updateAvatar(id, pos) {
  console.log("Updating avatar for", id);
  console.log(pos);
  if (players[id]) {
    players[id].setAttribute("position", `${pos.x} ${pos.y} ${pos.z}`);
  }
}

// Remove avatar when disconnected
function removeAvatar(id) {
  if (players[id]) {
    players[id].remove();
    delete players[id];
  }
}

// Send your position every 100ms
setInterval(() => {
  const pos = cameraRig.querySelector("a-camera").object3D.position;
  console.log("My position:", pos);
  socket.emit("move", { x: pos.x, y: pos.y, z: pos.z });
}, 100);
