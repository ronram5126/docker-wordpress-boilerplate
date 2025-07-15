function update_project_directories {
    python .docker/update_project_directories.py
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