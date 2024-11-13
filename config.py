class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@db:5432/mydatabase"
    ELASTICSEARCH_URL = "http://elasticsearch:9200"
    CELERY_BROKER_URL = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND = "redis://redis:6379/0"
