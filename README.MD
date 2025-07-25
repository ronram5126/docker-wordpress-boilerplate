# Minimalist Docker Wordpress MySQL PHPMyAdmin Boilerplate

This is a minimalistic boilerplate project for simulating wordpress in docker. This project is good for developing plugins and themes for wordpress using docker.

## Prerequisite

The bpiperplate uses docker so the most important prerequisite is the docker and docker compose.  

1. [Install Docker](https://docs.docker.com/engine/install/)
2. [Install Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Once you have installed docker and docker compose, you can simply run the wordpress site by following the steps below.

* **VSCode**: If you are using the vscode you can use debugger with `PHP Debug` to start the docker compose.
  * The settings for `PHP Debug` and `PHPIntelephense` has been added to the workspace.
  * As its very difficult to `chmod` `.docker` with tasks correctly, the files mounted under .docker is simply ignored so there is no conflict with the other systems. It is recommended to migrate the data base manually if you want to use it in different system.

* **LINUX**: on Linux you can get started by running `./start.sh` in the project directory.
  * you might will nedd to add executive permission to start.sh using `chmod +x start.sh` on linux.
  * You will require to provide password on exit as the `start.sh` is programmed to change the permission for files under `.docker` upon exit. If the permission isn't fixed the files under .docker becomes unaccessible to git causing issue if you don't want to ignore the files in the contianer.

* **WINDOWS**: On Windows you can get started by running `./start.ps`, in powershell.
  * Running scripts might be disabled on your system. To eradicate this issue you can run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`.

Once you started the program in the respective platform, You can access the wordpress site via [http://localhost:8000](http://localhost:8000). Additionally you can access PHPMyAdmin at [http://localhost:8088](http://localhost:8088) or connect to the MySQL database at [http://localhost:6033](http://localhost:6033).

## Developing Plugins and Themes

You can get started with development of your plugins and themes by creating directory under `./src/plugins` or `./src/themes`. There is hello_world folder by default, which could be deleted and new directories could be created. These directories are configured to wordpress service using `docker-compose.override.yml` file. `docker-compose.override.yml` is updated automatically when running `start.sh`.

## Things to Note

* Most of the configuration needs could be achieved by editting `.env` file.
  * `docker-composer.yml` mostly uses variables from `.env` file for configuration.
  * The configuration like **service_name** and **port_numbers** could easily be editted as well as the directory location of different project files.
* By Default, most of database and wp-content files are stored under `.docker/mysql` and `.docker/wp` respectively. 
  * You can ignore these directory using `.gitignore` file in project directory, if you don't want these contents to be tracked by git.
  * In Linux, the docker writes the file with `systemcore-dump` ownership and no permission for user. Therefore the shell script upon exit triggers the `chmod` command to change the file permission for the directories under `.docker` so it could be tracked and commited by git.
* You can access the file system for wordpress as well as any other docker service by using `docker-compose exec <service_name> bash` (service_names: **mysql**, **phpmyadmin** and **wordpress**) command on your shell. This will allow you to acces the filesystem in bash environment.
