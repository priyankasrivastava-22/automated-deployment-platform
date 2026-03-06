// Fetch system status
async function loadStatus() {
    try {
        const response = await fetch("/api/status");
        const data = await response.json();

        document.querySelector(".latest-build b").innerText =
            `Version ${data.version} - ${data.status}`;

        // Update CPU, Memory, Response randomly (simulate live data)
        document.getElementById("cpu").innerText =
            Math.floor(Math.random() * 80) + "%";

        document.getElementById("memory").innerText =
            Math.floor(Math.random() * 90) + "%";

        document.getElementById("response").innerText =
            Math.floor(Math.random() * 200) + "ms";

    } catch (error) {
        console.error("Error loading status:", error);
    }
}


//Fetch logs
async function loadLogs() {
    try {
        const response = await fetch("/api/logs");
        const data = await response.json();

        const logContainer = document.querySelector(".logs");
        logContainer.innerHTML = "<h4>Logs & Alerts</h4>";

        if (data.logs) {
            data.logs.forEach(log => {
                const p = document.createElement("p");
                p.innerText = log;

                if (log.toLowerCase().includes("error"))
                    p.classList.add("error");
                else if (log.toLowerCase().includes("warning"))
                    p.classList.add("warning");
                else
                    p.classList.add("info");

                logContainer.appendChild(p);
            });
        }

    } catch (error) {
        console.error("Error loading logs:", error);
    }
}


// Fetch build history
async function loadBuildHistory() {
    try {
        const response = await fetch("/api/build-history");
        const builds = await response.json();

        const historyList = document.querySelector(".history");
        historyList.innerHTML = "";

        builds.forEach(build => {
            const li = document.createElement("li");
            li.innerText = `#${build.id} ${build.status}`;

            if (build.status === "Successful")
                li.classList.add("success");
            else
                li.classList.add("failed");

            historyList.appendChild(li);
        });

    } catch (error) {
        console.error("Error loading build history:", error);
    }
}

async function triggerBuild() {
    try {
        const response = await fetch("/trigger-build", {
            method: "POST"
        });

        if (response.ok) {
            alert("Build Triggered Successfully!");
            loadBuildHistory();
        } else {
            alert("Failed to trigger build");
        }

    } catch (error) {
        console.error("Error triggering build:", error);
    }
}


// Auto refresh every 5 seconds
setInterval(() => {
    loadStatus();
    loadLogs();
}, 5000);


// Load immediately on page open
window.onload = function () {
    loadStatus();
    loadLogs();
};