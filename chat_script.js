// chat_script.js

function openChat() {
    // Load the chat window
    window.location.href = "chat_window.html";
}

function closeChat() {
    // Close the chat window
    window.location.href = "customer_dashboard.html";
}

function employeecloseChat() {
    // Close the chat window
    window.location.href = "employee_dashboard.html";
}

function sendMessage() {
    // Add code to send the message
    const messageInput = document.getElementById("messageInput");
    const chatMessages = document.getElementById("chatMessages");
    const message = messageInput.value;

    if (message.trim() !== "") {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message");
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        messageInput.value = "";
    }
}

