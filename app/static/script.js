function triggerBuild() {
    fetch("/trigger-build", {
        method: "POST"
    })
    .then(res => res.json())
    .then(data => {
        alert(data.status);
    });
}

function viewLogs(buildId) {

    if (buildId === "latest") {
        buildId = 102;  // later we will auto fetch latest
    }

    fetch("/logs/" + buildId)
    .then(res => res.text())
    .then(data => {
        document.getElementById("dashboard-section").style.display = "none";
        document.getElementById("deployments-section").style.display = "block";
        document.getElementById("log-output").innerText = data;
    });
}