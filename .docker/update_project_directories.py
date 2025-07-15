import os
import subprocess

def update_project_directories():
    print("Starting update of project directories...")
    plugins_dir = "src/plugins"
    themes_dir = "src/themes"
    wp_content_dir = "/var/www/html/wp-content"
    volumes = ""
    path_mappings = ""

    # Process plugins
    print(f"Scanning plugins directory: {plugins_dir}")
    for dir in os.listdir(plugins_dir):
        if dir == "." or dir == "..":
            continue
        if os.path.isdir(os.path.join(plugins_dir, dir)):
            print(f"Found plugin directory: {dir}")
            volumes += f"      - ${{PROJECT_SRC_PLUGINS_DIR}}/{dir}:${{WP_PLUGINS_DIR}}/{dir}\n"
            path_mappings += f'                "{wp_content_dir}/plugins/{dir}":"${{workspaceFolder}}/{plugins_dir}/{dir}",\n'
    
    # Process themes
    print(f"Scanning themes directory: {themes_dir}")
    for dir in os.listdir(themes_dir):
        if dir == "." or dir == "..":
            continue
        if os.path.isdir(os.path.join(plugins_dir, dir)):
            print(f"Found theme directory: {dir}")
            volumes += f"      - ${{PROJECT_SRC_THEMES_DIR}}/{dir}:${{WP_THEMES_DIR}}/{dir}\n"
            path_mappings += f'                "{wp_content_dir}/themes/{dir}":"${{workspaceFolder}}/{themes_dir}/{dir}",\n'
    
    
    # Write docker-compose.override.yml
    with open("./docker-compose.override.yml", "w") as f:
        print("Writing docker-compose.override.yml...")
        f.write("services:\n  wordpress:\n    volumes:\n")
        f.write(volumes)
        print("docker-compose.override.yml written successfully.")
    
    # Write .vscode/launch.json
    with open("./.vscode/launch.json", "w") as f:
        print("Writing .vscode/launch.json...")
        f.write('''{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Listen for Xdebug",
            "type": "php",
            "request": "launch",
            "port": 9003,
            "log": true,
            "pathMappings": {
''')
        f.write(path_mappings)
        f.write('''                "/var/www/html/": "${workspaceFolder}/.docker/wp"
            }
        }
    ]
}
''')
        print(".vscode/launch.json written successfully.")


if __name__ == "__main__":
    print(os.getcwd())
    update_project_directories()