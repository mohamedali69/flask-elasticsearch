from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from sqlalchemy.event import listens_for
from celery import Celery
import logging

app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)
es = Elasticsearch(app.config["ELASTICSEARCH_URL"])

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))

@app.route("/index", methods=["POST"])
def index_data():
    bulk_index_data_async.delay()
    return jsonify({"status": "Indexing started"}), 202

@celery.task
def bulk_index_data_async():
    products = Product.query.all()
    actions = [
        {
            "_index": "products",
            "_id": product.id,
            "_source": {
                "name": product.name,
                "description": product.description,
            },
        }
        for product in products
    ]
    bulk(es, actions)

@listens_for(Product, "after_insert")
@listens_for(Product, "after_update")
def index_product(mapper, connection, target):
    doc = {"name": target.name, "description": target.description}
    es.index(index="products", id=target.id, document=doc)

@listens_for(Product, "after_delete")
def delete_product(mapper, connection, target):
    es.delete(index="products", id=target.id)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["name", "description"],
            }
        },
        "from": (page - 1) * per_page,
        "size": per_page,
        "sort": ["_score"],
    }
    results = es.search(index="products", body=body)
    return jsonify(
        {
            "total": results["hits"]["total"]["value"],
            "products": [
                {
                    "id": hit["_id"],
                    "name": hit["_source"]["name"],
                    "description": hit["_source"]["description"],
                    "score": hit["_score"],
                }
                for hit in results["hits"]["hits"]
            ],
        }
    )

@app.route("/health", methods=["GET"])
def health_check():
    health = es.cluster.health()
    return jsonify({"status": health["status"], "details": health})

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()