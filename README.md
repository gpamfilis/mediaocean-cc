# Visit http://167.172.181.29:3000 to view in cloud

# To run locally

have docker installed

- rename `sample.env` to `.env`

- run `docker compose up`

visit http://localhost:3000

to run tests make sure you have `poetry` installed.

then run in sequence.

- `cd backend`
- `poetry install`
- `poetry run playwright install`
- `docker compose up`
- `poetry run pytest`



## IMPROVEMENTS

- create a redis service for a worker service
- create workers that for example cache response go fetch new posts etc
- add authentication in this case next-auth to quickly authenticate users using various providers
- Again, for authenticating we simply 'decorate' the routes and inject an auth dict like `{'user_id':'sdfsdfs', 'role':'admin'}`
- for error handling/logging i would use tools like sentry or bugsnag connected to the repo for quick resolution and replay.
- create a swagger doc for testing the endpoints 
