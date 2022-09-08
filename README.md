# Darqube task

## Task description

Framework: FastApi

Database: MongoDB(driver: motor)

Deploy: Docker Compose

1.  Create a user model using Pydantic with fallowing attributes:

        id
        first_name
        last_name
        role (one of: admin, dev, simple mortal)
        is_active
        created_at
        last_login
        hashed_pass

2.  Define and implement validation strategy for each one of given fields.
3.  Implement REST API methods for users using already defined Pydantic model.
4.  Implement a simple authentication middleware.
5.  Crete an route restricted only for user's with admin role which allow to change by oid(ObjectId) other user's attributes except `hashed_pass`.
6.  Crete a docker-compose file to deploy the app.
7.  Upload the solution to github and send the link.

## Docker

> Docker version 20.10.17
>
> docker-compose version 1.21.2

## How to use it

1. Create **.env** file using **.env.example**
2. To build and start the containers run following command. Add **-d** flag to run in detached mode:
   > docker-compose up --build
   >
   > docker-compose up --build -d

## Features

- User with **admin** role and with following credentials:

  > username (first_name): admin
  >
  > password: admin

  is created in DB. Use them to authorize, to be able to make requests. You can change default user values in **.env** file.

- Field **first_name** has unique constraint
- PUT request can be sent only by user with **admin** role, as asked in 5th point of task.
- API docs can be found in **http://0.0.0.0:8000/docs** if other port is not specified in **.env** file.
