async function loadData() {

    // STATUS
    const status = await fetch('/api/status');
    const statusData = await status.json();

    document.getElementById("env").innerText =
        "Environment: " + statusData.environment;

    document.getElementById("version").innerText =
        "Version: " + statusData.version;

    // SYSTEM
    const system = await fetch('/api/system');
    const systemData = await system.json();

    document.getElementById("cpu").innerText =
        "CPU Usage: " + systemData.cpu + "%";

    document.getElementById("memory").innerText =
        "Memory Usage: " + systemData.memory + "%";

    // BUILD HISTORY
    const builds = await fetch('/api/build-history');
    const buildData = await builds.json();

    const buildList = document.getElementById("build-history");
    buildList.innerHTML = "";

    buildData.slice(-5).reverse().forEach(b => {
        const li = document.createElement("li");
        li.innerText = `Build #${b.id} - ${b.status}`;
        buildList.appendChild(li);
    });

    // DEPLOYMENTS
    const deployments = await fetch('/api/deployments');
    const deployData = await deployments.json();

    const deployList = document.getElementById("deployment-history");
    deployList.innerHTML = "";

    deployData.slice(-5).reverse().forEach(d => {
        const li = document.createElement("li");
        li.innerText = `${d.environment} - ${d.version} - ${d.status}`;
        deployList.appendChild(li);
    });

    // LOGS
    const logs = await fetch('/api/logs');
    const logData = await logs.json();

    const logList = document.getElementById("logs");
    logList.innerHTML = "";

    logData.logs.forEach(l => {
        const li = document.createElement("li");
        li.innerText = l;
        logList.appendChild(li);
    });
}

loadData();
setInterval(loadData, 5000);