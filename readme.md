# Django App for Social_Networking

## [Postman api collection] (https://www.postman.com/abhi-sanwal/workspace/public/overview)

=======

### This app provides below functionalites:

- New user registration
- Login
- Apis to search users by username or email.
- Apis to send, accept and reject friend requets.
- List pending friend requests of a user.
- List accepted friend requests of a user.
- List rejected friend requests of a user.
- Api throttling (Rate limit)

Check this document for apis request and response samples. For high level understanding visit(https://rb.gy/p6j9ig)

### Exceot login and signup all apis are for authenticated users. They need to send jwt token to autheticate them.

> > > > > > > fde99e4 (Updated readme file)

### Step 1 - Clone the repo

```
git clone https://github.com/abhishek-sanwal/Social_Networking_rest_apis.git
```

### If Docker Dekstop app is installed on your machine.

Step 2- Go to the directory where docker-compose.yaml file is present and run projetc in docker container.

```
docker-compose up

```

Now server should be started at local host port 8000 .Now you can test apis.

To stop the docker container

```
docker-compose down
```

### If docker Dekstop is not instlled simply create a virtual enviroment using python

Step 2 - Create virtual enviroment using python

- For Windows and Linux

  ```
   python -m venv <enviroment_name>

  ```

- For Macos

      ```
       python3 -m venv <enviroment_name>
      ```

  Step 3 -> Activate virtual enviroment

- For Macos and Linux

  ```
   source <enviroment_name>/bin/activate

  ```

- For Windows

  ```
      <enviroment_name>/Scripts/activate

  ```

Step 4: Install requirments from requirments.txt file

```
pip install -r requirments.txt
```

Step 5 : Run below commands to start server

- For Macos and Linux
  ```
  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py runserver
  ```
- For Windows

  ```
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver
  ```

Now server should be started at local host port 8000

Now you can test apis.
