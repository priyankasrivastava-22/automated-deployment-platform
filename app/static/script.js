async function loadData() {

    // STATUS
    const statusRes = await fetch('/api/status');
    const status = await statusRes.json();

    document.getElementById("env").innerText =
        "Environment: " + status.environment;

    document.getElementById("version").innerText =
        "Version: " + status.version;

    // SYSTEM METRICS
    const systemRes = await fetch('/api/system');
    const system = await systemRes.json();

    document.getElementById("cpu").innerText =
        "CPU Usage: " + system.cpu + "%";

    document.getElementById("memory").innerText =
        "Memory Usage: " + system.memory + "%";

    // BUILD HISTORY
    const buildRes = await fetch('/api/build-history');
    const builds = await buildRes.json();

    const buildTable = document.getElementById("build-history");
    buildTable.innerHTML = "";

    builds.slice(-5).reverse().forEach(b => {
        buildTable.innerHTML += `
            <tr>
                <td>${b.id}</td>
                <td>${b.status}</td>
                <td>${b.timestamp || "-"}</td>
            </tr>
        `;
    });

    // DEPLOYMENTS
    const deployRes = await fetch('/api/deployments');
    const deployments = await deployRes.json();

    const deployTable = document.getElementById("deployment-history");
    deployTable.innerHTML = "";

    deployments.slice(-5).reverse().forEach(d => {
        deployTable.innerHTML += `
            <tr>
                <td>${d.id}</td>
                <td>${d.environment}</td>
                <td>${d.version}</td>
                <td>${d.status}</td>
                <td>${d.timestamp || "-"}</td>
            </tr>
        `;
    });

    // LOGS
    const logsRes = await fetch('/api/logs');
    const logs = await logsRes.json();

    const logDiv = document.getElementById("logs");
    logDiv.innerHTML = "";

    logs.logs.forEach(l => {
        logDiv.innerHTML += `<div>> ${l}</div>`;
    });
}

loadData();
setInterval(loadData, 5000);