const socket = new WebSocket('ws://localhost:8765');

socket.onopen = () => {
    document.getElementById('server-status').textContent = "Connected";
    console.log('WebSocket connection established.');
    updateStatus();
};

socket.onmessage = (event) => {
    const data = event.data;
    if (data.startsWith("Active Connections")) {
        const [connections, uptime] = data.split(", ");
        document.getElementById('active-connections').textContent = connections.split(": ")[1];
        document.getElementById('uptime').textContent = uptime.split(": ")[1];
    } else if (data === "Server shutting down...") {
        alert("Server is shutting down...");
        window.close();
    }
};

socket.onclose = () => {
    console.log('WebSocket connection closed.');
    document.getElementById('server-status').textContent = "Disconnected";
};

document.getElementById('stop-server').addEventListener('click', () => {
    socket.send('stop');
});

function updateStatus() {
    setInterval(() => {
        socket.send('status');
    }, 1000);
}