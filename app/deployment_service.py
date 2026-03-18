import os

def deploy_container(version, environment):

    try:
        container_name = f"automated-app-{environment}"
        image_name = "automated-deployment-platform:latest"

        #Assign ports based on environment
        port_map = {
            "dev": "5002",
            "staging": "5003",
            "prod": "5004"
        }

        port = port_map.get(environment, "5002")

        print(f"Deploying {container_name} on port {port}")

        #STEP 1: Stop existing container (if running)
        os.system(f"docker stop {container_name} || true")

        #STEP 2: Remove existing container
        os.system(f"docker rm {container_name} || true")

        #STEP 3: Remove unused images (cleanup)
        os.system("docker image prune -f")

        #STEP 4: Run new container
        run_command = f"docker run -d -p {port}:5000 --name {container_name} {image_name}"

        result = os.system(run_command)

        #If docker run fails
        if result != 0:
            print("Docker run failed")
            return False

        print("Deployment successful")
        return True

    except Exception as e:
        print(f"Deployment error: {str(e)}")
        return False