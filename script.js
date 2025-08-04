async function convertToBullets() {
  const inputText = document.getElementById('summaryInput').value;
  const outputList = document.getElementById('bulletOutput');
  outputList.innerHTML = '';

  if (inputText.trim() === '') {
    alert("Please enter some text to convert.");
    return;
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/format', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: inputText })
    });

    const result = await response.json();

    if (result.bullets) {
      result.bullets.forEach(sentence => {
        const li = document.createElement('li');
        li.textContent = sentence;
        outputList.appendChild(li);
      });
    } else {
      alert("Error formatting text.");
    }
  } catch (error) {
    console.error('Error:', error);
    alert("Failed to connect to the backend.");
  }
}
