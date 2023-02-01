Hello there,

For this project you'll first need to create a virtual environment using the following steps:

1. python -m venv venv
2. .\venv\Scripts\activate

Next is to upgrade pip and install flask in the env

3. python -m pip install --upgrade pip
4. python -m pip install flask
 
You will need to install mysql server and mysql workbench and configure them.
The database used is MYSQL. You will find the querry in a file named MYSQL.sql
Run the querry in that file to create the database with the desired tables.

SQL DB username = root
SQL DB password = FlaskApp1 

Then run the belo command to install the intergrator in the environment.

5. pip install flask-mysqldb

Other dependencies include below:

6. pip install requests

Use the following command to run the app;

python -m flask run 