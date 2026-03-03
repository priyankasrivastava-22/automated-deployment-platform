async function loadMetrics() {
    const response = await fetch('/api/system');
    const data = await response.json();

    document.getElementById("cpu").innerText = data.cpu + "%";
    document.getElementById("memory").innerText = data.memory + "%";
}

setInterval(loadMetrics, 5000);
loadMetrics();