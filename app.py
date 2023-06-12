import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form["question"]  # get question from user
        # send question to GalenAI server
        url = "https://galenai.co/api/v1/get-clinical-query-streaming-channel/" 
        payload = {'query': query}
        # payload = {"query": query, "clinical_summary_mode": True} for clinical summary mode
        token = f"token {your_token}" #your token here
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        response = requests.post(url, json=payload, headers=headers)

        # by default, GalenAI will not process queries outside of scope of the model.
        if response.status_code != 200:
            return render_template("index.html", error=response.json()["details"])

        # get a channel_name where generated text will be sent too as SSE (server sent events) as they become ready immmediately
        # Each request is a new channel_name generated on the fly.
        channel_name = response.json()["channel_name"]

        # once the query is finished streaming, you can retrieve the full details via this query_id
        # Save this in your DB to retrieve the full details later
        query_id = response.json()["query_id"]

        # client will call ready to listen endpoint, then listen to the SSE as they become ready
        return render_template(
            "listening.html", channel_name=channel_name, query_id=query_id
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
