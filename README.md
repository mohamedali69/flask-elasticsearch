# Flask Elasticsearch Integration Project

This project demonstrates how to integrate Flask with PostgreSQL, Elasticsearch, Redis, and Celery for an efficient and scalable data indexing and search system. It includes features like real-time data indexing, advanced search capabilities, and asynchronous task handling with Celery.

## Project Overview

- **Backend**: Flask, SQLAlchemy
- **Database**: PostgreSQL
- **Search Engine**: Elasticsearch
- **Task Queue**: Celery with Redis as the message broker
- **Containerization**: Docker and Docker Compose

### Key Features

- **Asynchronous Bulk Indexing**: Index large volumes of data asynchronously using Celery tasks.
- **Real-time Data Indexing**: Automatically index data upon creation, update, and deletion using SQLAlchemy event listeners.
- **Advanced Search**: Full-text search with filtering, pagination, and relevance scoring.
- **Health Check Endpoint**: Monitor the status of Elasticsearch to ensure smooth operation.
