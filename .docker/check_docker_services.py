import subprocess
import os
import stat

def check_docker_services():
    # Ensure we're in the correct working directory (where docker-compose.yml is)
    os.chdir(os.getenv("WORKSPACE_FOLDER", os.getcwd()))

    # Target the .docker directory in the workspace folder
    docker_dir = os.path.join(os.getcwd(), ".docker")
    
    try:
        # Run docker-compose ps and capture output
        result = subprocess.run(
            ["docker-compose", "ps"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout
        up_count = sum(1 for line in output.splitlines() if "Up" in line)

        if up_count > 0:
            print(f"Found {up_count} running services.")
            subprocess.run(["docker-compose", "down"], check=True)
            print("Stopped running services.")
        else:
            print("No running services found. Starting docker-compose...")

        print("Docker Compose started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running docker-compose: {e}")
        exit(1)

if __name__ == "__main__":
    check_docker_services()