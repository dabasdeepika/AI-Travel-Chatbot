const chatBox = document.getElementById('chatbox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

// Generate unique session ID
const senderId = "user_" + Math.floor(Math.random() * 1000000);

// Send message
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', e => { if(e.key === 'Enter') sendMessage(); });

function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage('user', message);
  showTypingIndicator();

  fetch('http://localhost:5005/webhooks/rest/webhook', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sender: senderId, message })
  })
  .then(res => res.json())
  .then(data => {
    removeTypingIndicator();
    if (Array.isArray(data) && data.length > 0) {
      data.forEach(msg => { if(msg.text) appendMessage('bot', msg.text); });
    } else {
      appendMessage('bot', "🤖 I didn't understand that.");
    }
  })
  .catch(err => {
    removeTypingIndicator();
    console.error(err);
    appendMessage('bot', "⚠️ Error connecting to server.");
  });

  userInput.value = '';
}

// Append messages
function appendMessage(sender, text) {
  const msg = document.createElement('div');
  msg.className = sender === 'user' ? 'user-message' : 'bot-message';
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Typing indicator
function showTypingIndicator() {
  const typing = document.createElement('div');
  typing.id = 'typing-indicator';
  typing.className = 'bot-message';
  typing.textContent = "🤖 is typing...";
  chatBox.appendChild(typing);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTypingIndicator() {
  const typing = document.getElementById('typing-indicator');
  if (typing) typing.remove();
}

// Auto greeting
window.addEventListener('load', () => sendBotAutoMessage("hi"));

function sendBotAutoMessage(message) {
  showTypingIndicator();
  fetch('http://localhost:5005/webhooks/rest/webhook', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sender: senderId, message })
  })
  .then(res => res.json())
  .then(data => {
    removeTypingIndicator();
    if(Array.isArray(data)) data.forEach(msg => { if(msg.text) appendMessage('bot', msg.text); });
  })
  .catch(err => { removeTypingIndicator(); console.error(err); });
}
