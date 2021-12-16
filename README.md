<h1>For Linux users</h1>
  <h2>Create virualenv and activate</h2>
    <p>python3 -m venv venv</p>
    <p>source ./venv/bin/activate</p>
   <h2>Install requirements</h2>
     <p>pip install -r requirements.txt</p>
   <h2>Run server</h2>
   <p>cd application</p>
   <p>flask run<br> (if flask run doesnt work write - "export FLASK_APP"=app<br>
    then "flask run")</p>
   <h2>Run script get_data.py</h2>
    <p>venv/bin/python3 get_data.py</p>
   <h2>Run script request_samples.py</h2>
    <p>venv/bin/python3 request_samples.py</p>

   

<h1>For Windows users</h1>
  <h2>Create virualenv and activate</h2>
    <p>pip install virtualenv</p>
    <p>python -m virtualenv venv</p>
    <p>venv\Scripts\activate</p>
   <h2>Install requirements</h2>
     <p>pip install -r requirements.txt</p>
   <h2>Run server</h2>
   <p>cd application</p>
   <p>flask run  (if flask run doesnt work write - "set FLASK_APP"=app
then "flask run")</p>
    <h2>Run script get_data.py</h2>
    <p>venv\Scripts\python.exe get_data.py</p>
   <h2>Run script request_samples.py</h2>
    <p>venv\Scripts\python.exe request_samples.py</p>
    
    
<h1>Some CLI commands (DB is already seted up so its not obligatory</h1>
  <h3>Create tables in DB</h3>
    <p>flask create-tables</p>
   <h3>Drop tables in DB</h3>
    <p>flask drop-tables</p>


