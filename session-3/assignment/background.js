chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
    if (message.type === 'START_SETUP') {
      const repoUrl = message.repoUrl;
  
      log(`Received repo URL: ${repoUrl}`);
  
      const response1 = await callLLM(`Given this repo URL: ${repoUrl}, Look at the repo contents and define the steps to set it up`);
      log(`LLM: ${response1}`);
  
      const response2 = await callLLM(`Analyze this repo structure and suggest setup steps.`);
  
      log(`LLM: ${response2}`);
    }
  });
  
  function log(text) {
    chrome.runtime.sendMessage({ type: 'LOG', text });
  }
  
  async function callLLM(prompt) {
    const res = await fetch('http://127.0.0.1:5000/agent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });
    const data = await res.json();
    return data.result;
  }
  