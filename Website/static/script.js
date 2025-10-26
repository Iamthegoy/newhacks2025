document.getElementById('searchBtn').addEventListener('click', async () => {
  const subject = document.getElementById('subject').value;
  const hobby = document.getElementById('hobby').value;
  const nationality = document.getElementById('nationality').value;
  const gender = document.getElementById('gender').value;
  const ageRange = document.getElementById('ageRange').value;

  try {
    const response = await fetch(`/search?subject=${subject}&hobby=${hobby}&nationality=${nationality}&gender=${gender}&ageRange=${ageRange}`);
    const users = await response.json();

    const resultDiv = document.getElementById('results');
    resultDiv.innerHTML = "";

    if (users.length === 0) {
      resultDiv.innerHTML = "<p>No matches found 😢</p>";
      return;
    }

    users.forEach(user => {
      const div = document.createElement("div");
      div.style.border = "1px solid #ccc";
      div.style.margin = "10px";
      div.style.padding = "10px";
      div.innerHTML = `
        <h3>${user.name} (${user.age}, ${user.gender}, ${user.nationality})</h3>
        <p><b>Subjects:</b> ${user.favorite_subjects.join(", ")}</p>
        <p><b>Hobbies:</b> ${user.hobbies.join(", ")}</p>
        <p>${user.bio}</p>
        <button onclick="window.location.href='/room/${user.name}'">Join Room</button>
      `;
      resultDiv.appendChild(div);
    });
  } catch (error) {
    console.error("Error fetching users:", error);
  }
});


