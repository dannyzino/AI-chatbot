function sendMessage() {
    const messageInput = document.getElementById("message-input");
    const messagesContainer = document.getElementById("messages");

    const userMessage = document.createElement("div");
    userMessage.classList.add("user-message");
    userMessage.textContent = messageInput.value;
    messagesContainer.appendChild(userMessage);

    // Send the message to your Python script using AJAX
    fetch('/process_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: messageInput.value
        })
    })
    .then(response => response.json())
    .then(data => {
        const botMessage = document.createElement("div");
        botMessage.classList.add("bot-message");
        botMessage.textContent = data.response;
        messagesContainer.appendChild(botMessage);
    })
    .catch(error => {
        console.error('Error sending message:', error);
    });

    messageInput.value = "";
}