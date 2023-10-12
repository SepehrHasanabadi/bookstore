it's been required to run the postgres database via the docker compose

```console
 docker compose up -d
 ```

the server should be running through the vscode `launch.json` or by runnng the script below in the api directory:

```console
main:app--host 0.0.0.0 --port 8000 --reload
```

the nuxt app should be running with the following command

```console
  npm run dev
```

make sure to install the requirements on the backend via:
```console
pip install -r requirements
``` 
(it's recommended to use `virtualenv`)

and the frontend by:
```console
npm install
```

in order to have the tables and some dummy data, the migrations should be applied:

```console
alembic upgrade head
```

the username and password for being able to see the portal is:

```console
username: bob
password: password
```

in order to run the testcases on backend, the following command should be exexuted:

```console
pytest
```