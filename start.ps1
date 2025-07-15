function update_project_directories {

    # "version: ""3""" | Out-File ./docker-compose.override.yml
    "services:" | Out-File ./docker-compose.override.yml
    "  wordpress:" | Out-File -Append  ./docker-compose.override.yml
    "    volumes:" | Out-File -Append  ./docker-compose.override.yml

    Set-Location ./src/plugins;
    foreach($file in Get-ChildItem) {
        "      - `${PROJECT_SRC_PLUGINS_DIR}/${file}:`${WP_PLUGINS_DIR}/${file}" | Out-File -Append  ../../docker-compose.override.yml;
    }

    
    Set-Location ../themes
    foreach($file in Get-ChildItem) {
        "      - `${PROJECT_SRC_THEMES_DIR}/${file}:`${WP_THEMES_DIR}/${file}" | Out-File -Append  ../../docker-compose.override.yml;
    }
    
    Set-Location ../..
}

function start_compose {
    # Making sure compose is down before we start
    try {
        docker-compose down
        docker-compose up  
    }
    catch {
    }
    finally { 
        docker-compose down
    }
}


update_project_directories

start_compose