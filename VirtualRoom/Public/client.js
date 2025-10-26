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
function addAvatar_new(id, pos) {
  console.log("Adding avatar for", id);
  const el = document.createElement("a-entity");
  el.setAttribute("gltf-model", "#chara");
  el.setAttribute("position", `${pos.x} ${pos.y} ${pos.z}`);
  el.setAttribute("id", id);

  // Floating username
  const nameTag = document.createElement("a-text");
  nameTag.setAttribute("value", id.slice(0, 5));
  nameTag.setAttribute("color", "black");
  nameTag.setAttribute("position", "0 1 0");
  nameTag.setAttribute("rotation", "0 180 0");
  nameTag.setAttribute("align", "center");
  el.appendChild(nameTag);

  scene.appendChild(el);
  players[id] = el;
}
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
  nameTag.setAttribute("rotation", "0 180 0");
  nameTag.setAttribute("align", "center");
  el.appendChild(nameTag);

  scene.appendChild(el);
  players[id] = el;
}

// Update avatar position and rotation
function updateAvatar(id, data) {
  if (players[id]) {
    // Update position
    players[id].setAttribute("position", `${data.x} ${data.y} ${data.z}`);
    
    // Update rotation around Y axis
    if (data.rotationY !== undefined) {
      console.log("Updating rotation for", id, data.rotationY);
      players[id].setAttribute("rotation", `0 ${data.rotationY} 0`);
    }
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
  const rot = cameraRig.querySelector("a-camera").object3D.rotation;
  // console.log("My position:", pos);
  const rotationY = rot.y * (180 / Math.PI); // Convert to degrees
  socket.emit("move", { x: pos.x, y: pos.y, z: pos.z, rotationY: rotationY });
}, 50);



// Audio streaming

/*
// 2. Play others’ audio
socket.on('audio', data => {
  const context = new AudioContext();
  console.log("Playing received audio", data);
  const buffer = context.createBuffer(1, data.byteLength, 44100);
  const floatArray = buffer.getChannelData(0);
  for (let i = 0; i < data.length; i++) floatArray[i] = data[i] / 0x7fff;
  const src = context.createBufferSource();
  src.buffer = buffer;
  src.connect(context.destination);
  src.start();
});

// 1. Capture mic
navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
  const context = new AudioContext();
  const source = context.createMediaStreamSource(stream);
  const processor = context.createScriptProcessor(4096, 1, 1);

  source.connect(processor);
  processor.connect(context.destination);

  processor.onaudioprocess = e => {
    const input = e.inputBuffer.getChannelData(0);
    const buffer = new Int16Array(input.length);
    for (let i = 0; i < input.length; i++) buffer[i] = input[i] * 0x7fff;
    socket.emit('audio', buffer);
  };
});
*/


// Capture mic and stream audio chunks (latter first)

socket.on("audio", arrayBuffer => {
  const data = new Int16Array(arrayBuffer);
  const context = new AudioContext();
  const audioBuffer = context.createBuffer(1, data.length, 44100);
  const floatArray = audioBuffer.getChannelData(0);
  for (let i = 0; i < data.length; i++) floatArray[i] = data[i] / 0x7fff;

  const src = context.createBufferSource();
  src.buffer = audioBuffer;
  src.connect(context.destination);
  src.start();
});


navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
  const context = new AudioContext();
  const source = context.createMediaStreamSource(stream);
  const processor = context.createScriptProcessor(4096, 1, 1);

  source.connect(processor);
  processor.connect(context.destination);

  processor.onaudioprocess = e => {
    const input = e.inputBuffer.getChannelData(0);
    const buffer = new Int16Array(input.length);
    for (let i = 0; i < input.length; i++) buffer[i] = input[i] * 0x7fff;

    socket.emit("audio", buffer.buffer);
  };
});





