web: gunicorn -b 0.0.0.0:$PORT src.applications.web.app:app
analyzer: python3 src/applications/analyzer/app.py
collector: gunicorn -b 0.0.0.0:8002 src.applications.collector.app:app