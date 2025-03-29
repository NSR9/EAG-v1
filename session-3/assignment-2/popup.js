// document.getElementById("runAgent").addEventListener("click", async () => {
//     const query = document.getElementById("query").value;
  
//     const res = await fetch("http://127.0.0.1:5000/run", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json"
//       },
//       body: JSON.stringify({ query })
//     });
  
//     const data = await res.json();
//     document.getElementById("result").textContent = `Answer: ${data.result}\n\nLogs:\n${data.logs}`;
//   });

// 

// 2

// const runButton = document.getElementById("runAgent");
// const audio = document.getElementById("thaggedeLe");
// const typedSpan = document.getElementById("typed");
// const resultDiv = document.getElementById("result");

// typedSpan.textContent = "Waiting for Pushpa’s reply...";
// audio.volume = 1.0;

// runButton.addEventListener("click", async () => {
//   audio.currentTime = 0;
//   audio.play();

//   const query = document.getElementById("query").value.trim();
//   if (!query) return;

//   typedSpan.textContent = "";
//   resultDiv.style.opacity = 1;
//   resultDiv.style.fontStyle = "normal";

//   try {
//     const res = await fetch("http://127.0.0.1:5000/run", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json"
//       },
//       body: JSON.stringify({
//         query,
//         session_id: "pushpa-session" // static or dynamic ID
//       })
//     });

//     const data = await res.json();
//     const fullResponse = `Answer: ${data.result}\n\nLogs:\n${data.logs}`;

//     // ✨ Trigger browser TTS
//     const utterance = new SpeechSynthesisUtterance(data.result);
//     utterance.rate = 1; // 1 = normal speed
//     utterance.pitch = 1; // deeper for mass feel
//     utterance.lang = "en-IN"; // Indian English voice
//     speechSynthesis.speak(utterance);

//     // ✍️ Animate typing
//     let index = 0;
//     const interval = setInterval(() => {
//       if (index < fullResponse.length) {
//         typedSpan.textContent += fullResponse.charAt(index);
//         index++;
//       } else {
//         clearInterval(interval);
//       }
//     }, 30);
//   } catch (error) {
//     typedSpan.textContent = "Pushpa couldn't respond. Check if the backend is running.";
//     console.error("Error:", error);
//   }
// });

const runButton = document.getElementById("runAgent");
const queryInput = document.getElementById("query");
const chatBox = document.getElementById("chatBox");
const audio = document.getElementById("thaggedeLe");

const sessionId = "pushpa-session";

function appendMessage(text, sender) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

runButton.addEventListener("click", async () => {
  const query = queryInput.value.trim();
  if (!query) return;

  appendMessage(query, "user");
  queryInput.value = "";

  audio.currentTime = 0;
  audio.play();

  try {
    const res = await fetch("http://127.0.0.1:5000/run", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query, session_id: sessionId }),
    });

    const data = await res.json();

    const fullResponse = data.result;

    // Animate typing
    const botDiv = document.createElement("div");
    botDiv.className = "message bot";
    chatBox.appendChild(botDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    let i = 0;
    const interval = setInterval(() => {
      if (i < fullResponse.length) {
        botDiv.textContent += fullResponse.charAt(i);
        i++;
        chatBox.scrollTop = chatBox.scrollHeight;
      } else {
        clearInterval(interval);
      }
    }, 30);
  } catch (err) {
    appendMessage("Pushpa couldn't respond. Backend may be down.", "bot");
    console.error(err);
  }
});

