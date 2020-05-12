from project.main import app

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine/ another GCP service, a webserver process such as Gunicorn will serve the app.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files.
    app.run(host='0.0.0.0', port=8080, debug=True)