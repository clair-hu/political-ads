# Frontend with Vue

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

# Startup Cloud SQL Proxy
./cloud_sql_proxy -instances=windy-marker-279018:us-west2:political-db=tcp:3306 -credential_file=cs348-group-project-2ddcf4e20dfb.json


# Backend with flask

# To share python environemnt, run the following (Requires installation of anaconda)
conda env create --file environment.yml

# Run the flask backend
python3 src/python/app.py

# Test it is running
curl -v 'http://127.0.0.1:5000/'
curl -v 'http://127.0.0.1:5000/user?email=SomeString'

