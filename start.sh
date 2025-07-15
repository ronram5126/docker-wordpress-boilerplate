#!/bin/bash

update_project_directories() {
    # echo "version: \"3\"" > ./docker-compose.override.yml
    echo "services:" > ./docker-compose.override.yml
    echo "  wordpress:" >> ./docker-compose.override.yml
    echo "    volumes:" >> ./docker-compose.override.yml

    cd src/plugins
    for dir in $(find . -type d -not -path '*/\.*' -not -path '.' -not -path '..'); do
        echo "      - \${PROJECT_SRC_PLUGINS_DIR}/${dir#./}:\${WP_PLUGINS_DIR}/${dir#./}" >> ../../docker-compose.override.yml;
    done

    cd ../themes
    for dir in $(find . -type d -not -path '*/\.*' -not -path '.' -not -path '..'); do
        echo "      - \${PROJECT_SRC_THEMES_DIR}/${dir#./}:\${WP_THEMES_DIR}/${dir#./}" >> ../../docker-compose.override.yml;
    done

    cd ../..
}

start_compose() {
    # Making sure compose is down before we start
    docker-compose stop
    docker-compose up  
}

exit_trap() {
    echo ""
    echo "Exit Script..";
    echo "=============="
    docker-compose stop
    # by default these files are unaccessible as these are created by the docker
    # this permission issue will causes problems with git.
    sudo chmod -R 777 ./.docker
    echo "all done."

}

trap exit_trap EXIT
trap exit_trap SIGTERM

update_project_directories

start_compose