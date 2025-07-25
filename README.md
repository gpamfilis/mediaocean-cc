# Ad Insight Exporer Lite

The ultimate tool for fraud detection (and this is just the light version...)

### Visit http://167.172.181.29:3000 to view in cloud



## how it works

The service fetches from your posts api in this case jsonplaceholder and computes summaries and anomalies based on user behavious and post characteristcs.



# To run locally

have docker installed

- rename `sample.env` to `.env`

- run `docker compose up --build`

visit http://localhost:3000

to run tests make sure you have `poetry` installed.

then run in sequence.

- `cd backend`
- `poetry install`
- `poetry run playwright install`
- `docker compose up`
- `poetry run pytest`



## IMPROVEMENTS

- Queue Service
    - create workers that for example cache responses 
    - go fetch new posts from the data source
    - perform anomaly/sumarry calculations in the background
    - send email/notification alerts for new detections
- add authentication in this case next-auth to quickly authenticate users using various providers
    - Again, for authenticating we simply 'decorate' the routes and inject an auth dict like `{'user_id':'sdfsdfs', 'role':'admin'}` I can show this from my other projects. NextAuth offers an easy way of handling providers, creating magic links etc.
- for error handling/logging i would use tools like sentry or bugsnag connected to the repo for quick resolution and replay.
- create a swagger doc for accessing the endpoints, or postman collections to run periodic tests.
- When clicking on row that has similar post flag. I should display in a modal/dialog to actually what user/post the row was similar to.
- split anomaly types into their own tabs/tables so there can be some freedom with the table logic and display logic, even a mini dashboard.
- Obviously more tests to actually cover all bizlogic such as similar title detection etc.
- Currently i have to access through ssh the digitalocean droplet / vps and perform a git (...) or docker compose (...) commands. I should either tie the 2 services backend/frontend with digital ocean apps. and build and push to the registry like i do 

    ```
    build_manager_backend_main:
    stage: build
    extends: .with-docker-login
    variables:
        SERVICE_TYPE: backend
        IMAGE_NAME: myapp
        IMAGE_PATH: $REGISTRY/$IMAGE_NAME-$BRANCH_NAME/$SERVICE_TYPE
    script:
        - docker build --no-cache -t $IMAGE_PATH:latest -f ./backend/Dockerfile ./backend
        - docker tag $IMAGE_PATH:latest $IMAGE_PATH:$CI_COMMIT_SHA
        - docker push $IMAGE_PATH:latest
        - docker images
    # when: manual
    only:
        changes:
        - backend/** # Monitor changes in this directory
        refs:
        - main # Run this job only on the develop branch
    ```

    with test and linting steps...

- For anomaly detection It could also run in parallel (multiprocessing) to avoid loops.
