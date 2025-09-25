function toggleChatbot() {
  const popup = document.getElementById("chatbot-popup");
  popup.style.display = (popup.style.display === "flex") ? "none" : "flex";
  popup.style.flexDirection = "column";
}

function sendMessage() {
  const userInput = document.getElementById("user-input");
  const message = userInput.value.trim();
  if (!message) return;

  // Display user message
  const messages = document.getElementById("chat-messages");
  messages.innerHTML += `<div><b>You:</b> ${message}</div>`;

  // Call Flask backend
  fetch("/chatbot", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  })
  .then(res => res.json())
  .then(data => {
    messages.innerHTML += `<div><b>Bot:</b> ${data.reply}</div>`;
    messages.scrollTop = messages.scrollHeight;
  });

  userInput.value = "";
}
