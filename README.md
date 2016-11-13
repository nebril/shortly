# shortly

Shortly is an application which acts as url shortener which additionally assigns shortened urls to randomly generated users.

## deployment

The site is currently deployed at [mkwiek.pl](http://mkwiek.pl). It's hosted on AWS ECS2 container service.

You can run the container on your own:

```bash
docker build -t shortly .
docker run -d -p 8080:80 shortly
# open localhost:8080 in browser
```

Alternatively, you can install requirements and run the app on host machine.
```bash
mkvirtualenv --python=python3 shortly
pip install -r app/requirements.txt
python app/manage.py migrate
python app/manage.py create_fake_users 100
python app/manage.py runserver
# open 127.0.0.1:8000 in browser
```

## TODO
 - remove not needed django apps (admin/auth/session etc.)
 - reduce size and layer count of docker image 
 - write unit tests
 - make docker container use persistent data (right now it uses database created and populated inside container, which will perish in case of container failure)