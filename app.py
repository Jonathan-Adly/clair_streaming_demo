import requests
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_URL = "https://galenai.co"
# BASE_URL = "http://localhost:8000"
TOKEN = ""


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form["question"]  # get question from user

        # send question to GalenAI server
        url = f"{BASE_URL}/api/v1/get-clinical-query-streaming-channel/"
        payload = {"query": query}
        # payload = {"query": query, "clinical_summary_mode": True} for clinical summary mode
        token = f"token {TOKEN}"  # your token here
        headers = {"Authorization": token, "Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)

        # by default, GalenAI will not process queries outside of scope of the model.
        if response.status_code != 200:
            return render_template("index.html", error=response.json()["detail"])

        # get a channel_name where generated text will be sent too as SSE (server sent events) as they become ready immmediately
        # Each request is a new channel_name generated on the fly.
        channel_name = response.json()["channel_name"]

        # once the query is finished streaming, you can retrieve the full details via this query_id
        # Save this in your DB to retrieve the full details later
        query_id = response.json()["query_id"]

        # client will call ready to listen endpoint, then listen to the SSE as they become ready
        return render_template(
            "listening.html",
            channel_name=channel_name,
            query_id=query_id,
            base_url=BASE_URL,
        )

    return render_template("index.html")


@app.route("/icd10", methods=["GET", "POST"])
def icd10():
    if request.method == "POST":
        # get the comma separated icd10 codes and turn into a list, stripping all spaces and capitalizing each item
        icd10_codes = [
            code.strip().upper() for code in request.form["icd10_codes"].split(",")
        ]

        # send question to GalenAI server
        url = f"{BASE_URL}/api/v1/create-bulk-icd10-streaming-channel/"
        payload = {"codes": icd10_codes}
        token = f"token {TOKEN}"  # your token here
        headers = {"Authorization": token, "Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)

        # handle errors.
        if response.status_code != 200:
            return render_template("icd10.html", error=response.json()["detail"])

        # get a channel_name where generated text will be sent too as SSE (server sent events) as they become ready immmediately
        # Each request is a new channel_name generated on the fly.
        channel_name = response.json()["channel_name"]

        # once the query is finished streaming, you can retrieve the full details via this query_id
        # Save this in your DB to retrieve the full details later
        query_id = response.json()["query_id"]
        return render_template(
            "listening_icd.html",
            channel_name=channel_name,
            query_id=query_id,
            base_url=BASE_URL,
        )

    return render_template("icd10.html")


@app.route("/stewardship", methods=["GET", "POST"])
def stewardship():
    if request.method == "POST":
        infection = request.form["infection"]  # get infection from user
        age = (
            int(request.form["age"]) if request.form["age"] else None
        )  # get age from user
        weight = (
            int(request.form["weight"]) if request.form["weight"] else None
        )  # get weight from user
        crcl = (
            int(request.form["crcl"]) if request.form["crcl"] else None
        )  # get crcl from user

        liver_disease = False
        if "liver_disease" in request.form:
            liver_disease = True

        # send question to GalenAI server
        url = f"{BASE_URL}/api/v1/create-stewardship-streaming-channel/"
        payload = {"infection": infection}
        if age:
            payload["age"] = age
        if weight:
            payload["weight"] = weight
        if crcl:
            payload["crcl"] = crcl
        if liver_disease:
            payload["liver_disease"] = liver_disease

        token = f"token {TOKEN}"  # your token here

        headers = {"Authorization": token, "Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            return render_template("stewardship.html", error=response.json()["detail"])

        channel_name = response.json()["channel_name"]
        query_id = response.json()["query_id"]

        return render_template(
            "listening_stewardship.html",
            channel_name=channel_name,
            query_id=query_id,
            base_url=BASE_URL,
        )

    return render_template("stewardship.html")


@app.route("/interactions", methods=["GET", "POST"])
def interactions():
    if request.method == "POST":
        # get the comma separated drugs and turn into a list, stripping all spaces
        drug_list = [drug.strip().lower() for drug in request.form["drugs"].split(",")]
        print(drug_list)
        # send question to GalenAI server
        url = f"{BASE_URL}/api/v1/create-interactions-streaming-channel/"
        payload = {"drugs": drug_list}
        token = f"token {TOKEN}"  # your token here
        headers = {"Authorization": token, "Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)

        # handle errors.
        if response.status_code != 200:
            return render_template("interactions.html", error=response.json()["detail"])

        # get a channel_name where generated text will be sent too as SSE (server sent events) as they become ready immmediately
        # Each request is a new channel_name generated on the fly.
        channel_name = response.json()["channel_name"]

        # once the query is finished streaming, you can retrieve the full details via this query_id
        # Save this in your DB to retrieve the full details later
        query_id = response.json()["query_id"]
        return render_template(
            "listening_interactions.html",
            channel_name=channel_name,
            query_id=query_id,
            base_url=BASE_URL,
        )

    return render_template("interactions.html")


if __name__ == "__main__":
    app.run(debug=True)
