#!/bin/bash

update_project_directories() {
    python ./.docker/update_project_directories.py
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