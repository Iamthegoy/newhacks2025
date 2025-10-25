document.getElementById('searchBtn').addEventListener('click', async () => {
  const subject = document.getElementById('subject').value;
  const hobby = document.getElementById('hobby').value;

  const query = new URLSearchParams({ subject, hobby });
  const response = await fetch(`/search?${query}`);
  const users = await response.json();

  const resultDiv = document.getElementById('results');
  if (users.length === 0) {
    resultDiv.innerHTML = "<p>No matches found 😢</p>";
    return;
  }

  resultDiv.innerHTML = users.map(u => `
    <div style="margin:10px; padding:10px; border:1px solid #ccc;">
      <h3>${u.name} (${u.major}, Year ${u.year})</h3>
      <p>${u.bio}</p>
      <p>Hobbies: ${u.hobbies.join(', ')}</p>
      <p>Subjects: ${u.favorite_subjects.join(', ')}</p>
    </div>
  `).join('');
});
