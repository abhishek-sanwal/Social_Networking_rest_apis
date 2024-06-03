# Django App for Social_Networking

### Step 1 - Clone the repo

```
git clone https://github.com/abhishek-sanwal/Social_Networking_rest_apis.git
```

### If Docker Dekstop app is installed on your machine.

Step 2- Run Docker container.

```
docker-compose up

```

Now server should be started at local host port 8000

Now you can test apis.

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

- For Macos

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
