# notes-app back-end

## Highlights
* Flask based API servlet. GETs, POSTs and DELETEs a 'note' kind to GCP datastore.

* Entity keys are md5 hex of their title to prevent large primary key. Dates, title and user are indexed, note text is excluded from index.

* Working unit testing stubbing datastore functionality (by putting datastore functionality into its own class)