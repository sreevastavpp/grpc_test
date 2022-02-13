import os
from flask import Flask, render_template
import grpc
from google.protobuf.json_format import MessageToJson

from recommendations_pb2 import BookCategory, RecommendationRequest
from recommendations_pb2_grpc import RecommendationsStub

app = Flask(__name__)

recommendations_host = os.getenv("RECOMMENDATIONS_HOST", "localhost")

recommendations_channel = grpc.insecure_channel(
    f"{recommendations_host}:50051"
)
recommendations_client = RecommendationsStub(recommendations_channel)


@app.route("/")
def render_homepage():
    print("request received")

    recommendations_request = RecommendationRequest(
        user_id=1, category=BookCategory.MYSTERY, max_results=3
    )

    print("connecting to grpc")

    recommendations_response = recommendations_client.Recommend(
        recommendations_request
    )

    print("response received")

    return render_template(
        "homepage.html",
        recommendations=recommendations_response.recommendations,
    )


@app.route("/save")
def save_data():
    recommendations_request = RecommendationRequest(
        user_id=1, category=BookCategory.MYSTERY, max_results=3
    )

    recommendations_response = recommendations_client.Recommend(recommendations_request)

    txt_path = os.path.join("/data", "data.txt")

    with open("/data/newfile.txt", "w") as f:
        f.write(MessageToJson(recommendations_response))

    return "data saved"


# Run flask app from terminal
# FLASK_APP=marketplace.py flask run

if __name__ == "__main__":
    app.run(debug=True, port=5000)
