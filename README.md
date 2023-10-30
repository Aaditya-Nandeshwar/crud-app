# crud-app

## Description

Building & deploying Python-based sample application with CRUD functionality for PostgresSQL support, along with the ability to perform CRUD operations on PostgreSQL DB, and generating Helm charts for the deployment is a multi-step process. I'll outline the steps to achieve this:

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Deployment](#deployment)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

Instructions for setting up the development environment installation steps.

1. Clone the git repo & switch to project directory 

    ```
    git clone https://github.com/Aaditya-Nandeshwar/crud-app.git
    cd crud-app
   ```
2. Setup a postgres SQL database locally using docker. 

    ```
   docker pull postgres
   docker run --name -d postgres -p 5432:5432 -e POSTGRES_PASSWORD=<password> postgres
   ```
3. Set the following environment variable for crud-app

    ```
    expport DB_NAME: "postgres"
    expport DB_SERVER: "localhost"
    expport DB_PASSWORD: "<password>"
    expport DB_USER: "postgres"
    expport DB_PORT: "5432"
   ```
   
4. Run the python app

    ```
    python3 app.py 
   ```
   
5. call db api from another terminal

    ```bash
    curl http://localhost:80/api/records
    curl -X POST -H "Content-Type: application/json" -d '{"name": "Aaditya", "fees": 7500, "duration": 60}' http://localhost:80/api/create
    curl -X PUT -H "Content-Type: application/json" -d '{"name": "k8s", "fees": 7500, "duration": 60}' http://localhost:80/api/update/1
    curl -X DELETE -H "Content-Type: application/json" -d '{"id": 1}' http://localhost:80/api/delete/1
    ```

### Prerequisites

* Any K8s Cluster deployed
* Helm & Kubectl CLI installed with necessary access to create cluster resources

### Installation

Step-by-step instructions on how to install and configure the crud-app. You can use following steps to achieve this.

1. Clone the git repo, switch to project directory & create postgres db password in base64 format
    ```bash
    $ git clone https://github.com/Aaditya-Nandeshwar/crud-app.git
    $ cd crud-app
    $ echo "<postgres-password>" | base64
    ```


2. Open `postgres.yaml` file & add base64 encoded password from in line number 7 
    
    ```
   password: <postgres-password>
   ```

3. Deploy postgres db by applying the `postgres.yaml` manifest.
    ```
   kubectl apply -f postgres.yaml
   ```
4. Verify the postgres deployment
    ```bash
   $ kubectl get pods 
   NAME                                        READY   STATUS    RESTARTS   AGE
   postgres-598d9b9884-hwvnt                   1/1     Running   0          23s
   ```
5. Now update the `values.yaml` file with following variables
    ```
   deploymentVariables:
      DB_NAME: "postgres"
      DB_SERVER: "postgres.default.svc.cluster.local"
      DB_PASSWORD: "<postgres-password>"
      DB_USER: "postgres"
      DB_PORT: "5432"
   ```
6. Deploy the crud-app helm chart using following command.

    ```bash
   #Run this command inside the project directory
   $ helm install crud-app . -f values.yaml
   ```
8. Verify the helm deployment using following commands
    ```bash
   $ helm ls
   NAME     NAMESPACE REVISION        UPDATED                                STATUS         CHART         APP VERSION
   crud-app default      1       2023-10-30 08:37:01.432504712 +0000 UTC    deployed     crud-app-0.1.0      1.16.0  
   
   $ kubectl get pods
   NAME                                        READY   STATUS    RESTARTS   AGE
   crud-app-7b659487dc-nrqq5                   1/1     Running   0          12s
   ```
9. Finally, test the crud-app using following commands

    ```bash
    #Exec into the postgres pod
    $ kubectl exec -ti postgres-598d9b9884-hwvnt -- /bin/sh
    #Install curl package 
    $ apt update 
    $ apt install curl -y
   
   
    # Call the get records api 
    $ curl crud-app.default.svc.cluster.local/api/records
    #You will see the empty list since there is no record created
    []
   
    #call the create api to create db records
    $ curl -X POST -H "Content-Type: application/json" -d '{"name": "Aaditya", "fees": 7500, "duration": 60}' crud-app.default.svc.cluster.local/api/create
    #In the output you will see the following message
    {"message":"Record created successfully"}
    #Veirfy the record in db table by calling get records api one more time
    $ curl crud-app.default.svc.cluster.local/api/records
    [[1,"Aaditya",7500,60]]
   
   
   
    #call update api to update the db record
    $ curl -X PUT -H "Content-Type: application/json" -d '{"name": "k8s", "fees": 7500, "duration": 60}' crud-app.default.svc.cluster.local/api/update/1
    #In the output you will see the following message
    {"message":"Record updated successfully"}
    #Veirfy the updated record in db table by calling get records api one more time
    $ curl crud-app.default.svc.cluster.local/api/records
   
   
    #Finally, call delete api to delete the record by passing the record "id"
    $ curl -X DELETE -H "Content-Type: application/json" -d '{"id": 1}' crud-app.default.svc.cluster.local/api/delete/1
    #In the output you will see the following message
    {"message":"Record deleted successfully"}
    #Veirfy the record has been deleted from db table by calling get records api one more time
    []
     ```
   
10. For cleaning up resources you can use following commands

     ```bash
    $ helm uninstall crud-app 
    $ kubectl delete -f postgres.yaml
    ```