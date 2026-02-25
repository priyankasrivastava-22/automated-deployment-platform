async function loadData() {

    const status = await fetch('/api/status');
    const statusData = await status.json();

    document.getElementById("env").innerText =
        "Environment: " + statusData.environment;

    document.getElementById("version").innerText =
        "Version: " + statusData.version;

    const system = await fetch('/api/system');
    const systemData = await system.json();

    document.getElementById("cpu").innerText =
        "CPU Usage: " + systemData.cpu + "%";

    document.getElementById("memory").innerText =
        "Memory Usage: " + systemData.memory + "%";
}

loadData();
setInterval(loadData, 5000);