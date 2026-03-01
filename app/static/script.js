function triggerBuild() {
    fetch("/trigger-build", {
        method: "POST"
    })
    .then(res => res.json())
    .then(data => {
        alert(data.status);
    });
}

function showSection(sectionId) {

    document.getElementById("dashboard-section").classList.add("hidden");
    document.getElementById("deployments-section").classList.add("hidden");
    document.getElementById("settings-section").classList.add("hidden");

    document.getElementById(sectionId).classList.remove("hidden");
}

function showDashboard() {
    showSection("dashboard-section");
}

function showDeployments() {
    showSection("deployments-section");
}

function showSettings() {
    showSection("settings-section");
}

function viewLogs(buildId) {

    if (buildId === "latest") {
        buildId = 102;  // later dynamic
    }

    fetch("/logs/" + buildId)
    .then(res => res.text())
    .then(data => {

        showSection("deployments-section");   // cleaner navigation

        document.getElementById("log-output").innerText = data;
    });
}