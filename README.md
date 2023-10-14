# Lanview project backend
<h3>This is a backend for my side project. <br/>
Front-end is located in another repo <a href='https://github.com/Kubalak/lanview-front/'>lanview-front</a>
</h3>


<h2>Libraries used</h2>
<ul>
    <li><a href=''>django</a> framework</li>
    <li><a href=''>django-rest</a> framework</li>
    <li><a href=''>celery</a> to run and schedule tasks</li>
    <li><a href=''>nmap</a> for using nmap in python</li>
</ul>


# Installation
<p>First clone repo and install required packages into the new <a href=''>conda</a> environment:</p>

```
git clone https://github.com/Kubalak/lanview-backend.git
cd lanview-backend
conda create --name YOUR_ENV_NAME --file requiremenst.txt
conda activate YOUR_ENV_NAME
```
<p>It is required to have a working rabbitmq server in system. You can get one using this command:

```
docker run -d -p 5672:5672 rabbitmq
```
</p>

# Usage
<h2>Prequisistes:</h2>
<ul>
    <li>Before running project a database tables need to be created. Use `python manage.py makemigrations` and then `python manage.py migrate` to create them.</li>
    <li> Before starting server a user needs to be created. <br/>To do this please run `python manage.py createsuperuser` and add new superuser to the system</li>
</ul>

<ol>
    <li> Start a rabbitmq server using `docker start` command.</li>
    <li> Start celery worker (requires sudo to run nmap as sudo) e.g. `sudo $(which celery) -A celerytasks worker -l INFO`. Optionally you can add `--autoscale=&lt;max&gt;,&lt;min&gt;` where <i>min</i> is minimal number of processes and <i>max</i> is the maximum. </li>
    <li> Start celery beat to scan network in given periods</li>
    <li> Start main project with `python manage.py runserver`</li>
</ol>

