# notes-app back-end

## Highlights of the app
* Flask based API servlet. GETs, POSTs and DELETEs a 'note' kind to GCP datastore.

* Entity keys are md5 hex of their title to prevent large primary key. Dates, title and user are indexed, note text is excluded from index.

* Working unit testing stubbing datastore functionality (by putting datastore functionality into its own class)


## Running locally on docker
Create a local file with the compute engine service account key file called 'service-account-credential.key'.
 
This shouldn't be uploaded to git (check it isn't on any commit!) as .key files are included in the .gitignore

Then run these commands:

```
docker build --tag notes-app-backend .
docker run --name notes-app-backend -p 8080:8080 -e GOOGLE_APPLICATION_CREDENTIALS='service-account-credential.key' notes-app-backend
```

The service should now be reachable on localhost:8080

## Running on Cloud Run

```
gcloud builds submit --tag gcr.io/{your_project_id}/notes-app-backend
gcloud run deploy --image gcr.io/{your_project_id}/test_datastore --platform managed
```

### Calling locally
Generate a JWT for calling test_gateway using this command
```
gcloud auth print-identity-token
```
This should only work from an authenticated google account that has access to the cloud run service.

See 'Creating private services' on https://cloud.google.com/run/docs/triggering/https-request.
