
## How to Run Docker Compose

This repository uses Docker Compose to manage the execution of the "ejtrader/ejtraderct:rest" application. Follow the instructions below to run the project on your local machine.

### Prerequisites

Before getting started, make sure you have Docker and Docker Compose installed on your system. You can find information on how to install them at [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/) and [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/).

### Steps to Run

1. Clone this repository to your local environment.

2. In the root directory of the project, create a file named `.env` and configure the required environment variables for the application. Make sure to fill in all the required variables.

3. Open a terminal and navigate to the root directory of the project.

4. Run the following command to start the application using Docker Compose:

This command will build the necessary containers and start the application. The output will be displayed in the terminal.

Once the application is up and running, you can access it in using postman at http://localhost:8000.
That's it! You have successfully run the "ejtrader/ejtraderct:rest" application using Docker Compose.

Note: If you want to run the containers in the background (detached mode), you can use the -d flag:

```shell
docker-compose up -d
```


Please add your credentials to the `env_example` file and rename it to `.env`. Then, run the following command:

```shell
docker-compose up
```

or


```shell
docker build --build-arg HOST_NAME=your_host_name --build-arg SENDER_COMPID=your_sender_compid --build-arg PASSWORD=your_password -t ejtrader/ejtraderct:rest .
```

```shell
docker run -e "HOST_NAME=your_host_name" -e "SENDER_COMPID=your_sender_compid" -e "PASSWORD=your_password" ejtrader/ejtraderct:rest
```


### Option 2: Use Pre-Built Image with Docker Compose
Prerequisites

Before getting started, make sure you have Docker Compose installed on your system. You can find information on how to install Docker Compose at https://docs.docker.com/compose/install/.

Steps to Run

Copy the contents of the docker-compose.yml file below and paste it into a file named docker-compose.yml in the root directory of your project:
```yml
version: '3.8'
services:
  ejtraderctrest:
    image: ejtrader/ejtraderct:rest
    container_name: rabbitmq
    restart: always
    environment:
      HOST_NAME: "68.205.95.20"
      SENDER_COMPID: "live.icmarkets.1104926"
      PASSWORD: "12345678"
      
    ports:
      - "8000:8000"
    env_file:
      - .env
```

In the root directory of the project, open a terminal.
Run the following command to start the application using Docker Compose:
For Windows and Linux:

```shell
docker-compose up -d 
```

For macOS:

```shell
docker compose up -d 
```
