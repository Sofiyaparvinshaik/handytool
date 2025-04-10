import subprocess

def update_log4j_in_docker(container_name, log4j_file_path, class_name, new_log_level):
    # Logger tag structure
    logger_tag = f"""
<Logger name="{class_name}" level="{new_log_level}" additivity="false">
    <AppenderRef ref="asyncD"/>
    <AppenderRef ref="asyncE" level="ERROR"/>
</Logger>
"""

    # Command to enter Docker container
    docker_enter_command = f"docker exec -it {container_name} /bin/bash -c '"

    # Step 1: Append the new logger tag to the end of the <Loggers> section
    append_logger_command = f"sed -i '/<Loggers>/a \\\n{logger_tag.strip()}' {log4j_file_path}"

    # Step 2: Update the log level for a specific class if it already exists
    update_log_level_command = f"sed -i '/<Logger name=\"{class_name}\"/s/level=\"[^\"]*\"/level=\"{new_log_level}\"/' {log4j_file_path}"

    try:
        # Step 3: Execute the Docker commands
        # 1. Append new logger tag to the log4j.xml file
        subprocess.run(f"{docker_enter_command}{append_logger_command}'", shell=True, check=True)

        # 2. Update the log level if the logger tag already exists
        subprocess.run(f"{docker_enter_command}{update_log_level_command}'", shell=True, check=True)

        print(f"Log4j configuration updated for class: {class_name} with log level: {new_log_level}")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while updating log4j configuration: {e}")
    

if __name__ == "__main__":
    # Define your parameters
    container_name = "object-main"  # Replace with your Docker container name
    log4j_file_path = "/opt/storageos/conf/blobsvc-log4j2.xml"  # Path to your log4j.xml file inside the container
    class_name = "com.emc.storageos.data.object.impl"  # Class for which you want to add the logger
    new_log_level = "DEBUG"  # New log level (can be DEBUG, INFO, ERROR, etc.)

    # Update the log4j configuration in the Docker container
    update_log4j_in_docker(container_name, log4j_file_path, class_name, new_log_level)
