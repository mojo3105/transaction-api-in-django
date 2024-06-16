# Transactions APIs in Django
It contains the transactions api which can perform operation of add/withdraw money from account and buy/sell stocks.

# Run the application.
## Prerequisites

Before running the application, make sure you have the following installed:
- Docker
- Docker Compose

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository:
   git clone https://github.com/Coditas-python-learners/transactions-apis-in-django.git
   cd case_studies

2.Build the Docker image:
   docker-compose build

3.Start the containers:
   docker-compose up -d
   This will start the MySQL and Django application containers in detached mode.  

4.Verify the containers are running:
   docker-compose ps
  You should see the mysql and django services listed as running.

5.Access the application:
  Open your web browser and visit http://localhost:8000 to access the Django application.

6.Clean up:
  To stop and remove the containers, run:
     docker-compose down
  This will stop and remove the containers, but preserve the data volume.

## Configuration
The project uses a YAML file (docker-compose.yml) to configure the containers and services. You can customize the configuration by modifying this file according to your 
requirements.

