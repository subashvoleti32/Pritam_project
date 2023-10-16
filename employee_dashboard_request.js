// Sample data for demonstration
const requestsData = [
    {id: 1, status: "Open"},
    {id: 2, status: "Open"},
    // Add more request objects as needed
];

// Function to display requests in the dashboard
function displayRequests() {
    const requestsList = document.getElementById("requestsList");
    requestsList.innerHTML = "";

    for (const request of requestsData) {
        const requestDiv = document.createElement("div");
        requestDiv.classList.add("request-item");
        requestDiv.innerHTML = `
            <p>Request ID: ${request.id}</p>
            <p>Status: ${request.status}</p>
            <button onclick="openChat(${request.id})">Chat</button>
            <button onclick="closeRequest(${request.id})">Close Request</button>
        `;
        requestsList.appendChild(requestDiv);
    }

    document.getElementById("numRequests").textContent = requestsData.length;
}

// Function to open chat for a request
function openChat(requestId) {
    // Add code to open a chat window for the specified request
}

// Function to close a request
function closeRequest(requestId) {
    // Add code to close the specified request
}
// Function to logout and redirect to the login page
function logout() {
    // Assuming your login page is named employee_login.html
    window.location.href = "employee_login.html";
}

// Display requests on page load
window.onload = displayRequests;
