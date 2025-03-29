document.getElementById('startBtn').addEventListener('click', () => {
    const repoUrl = document.getElementById('repoUrl').value;
    chrome.runtime.sendMessage({ type: 'START_SETUP', repoUrl });
  });
  
  chrome.runtime.onMessage.addListener((msg) => {
    if (msg.type === 'LOG') {
      const output = document.getElementById('output');
      output.textContent += `\n${msg.text}`;
    }
  });
  