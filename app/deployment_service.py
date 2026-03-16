import subprocess

def deploy_container(version, environment):
    container_name = f"automated-app-{environment}"

    image = f"automated-platform:{version}"

    try:
        subprocess.run(["docker", "pull", image])

        subprocess.run(["docker", "stop", container_name], stderr=subprocess.DEVNULL)
        subprocess.run(["docker", "rm", container_name], stderr=subprocess.DEVNULL)

        port = "5001" if environment == "dev" else "5002"

        subprocess.run([
            "docker",
            "run",
            "-d",
            "--name",
            container_name,
            "-p",
            f"{port}:5000",
            image
        ])

        return True

    except Exception as e:
        print(e)
        return False