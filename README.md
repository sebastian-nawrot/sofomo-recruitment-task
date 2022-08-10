# sofomo-recruitment-task

How to run API:
```
docker compose up
```

How to run tests:
```
docker compose run --rm --entrypoint "python -m pytest" app
```

To generate access token:
```
curl --location --request GET 'https://sofomo-recruitment-task.herokuapp.com/access_token'
```

To add new geolocation to service:
```
curl --location --request POST 'https://sofomo-recruitment-task.herokuapp.com/geolocation' \
--header 'Access-Token: XXX' \
--header 'Content-Type: application/json' \
--data-raw '{
  "address": "172.152.31.241"
}'
```

To get geolocation from service:
```
curl --location --request GET 'https://sofomo-recruitment-task.herokuapp.com/geolocation/172.152.31.241' \
--header 'Access-Token: XXX'
```

To delete geolocation from service:
```
curl --location --request DELETE 'https://sofomo-recruitment-task.herokuapp.com/geolocation/172.152.31.241' \
--header 'Access-Token: XXX'
```
