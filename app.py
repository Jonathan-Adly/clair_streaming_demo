import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form["question"]  # get question from user
        base_url = "http://localhost:8000" 
        
        #base_url = "https://galenai.co/" # for production

        # send question to GalenAI server
        url = f"{base_url}/api/v1/get-clinical-query-streaming-channel/" 
        payload = {'query': query}
        # payload = {"query": query, "clinical_summary_mode": True} for clinical summary mode
        token = f"token {your_token}" #your token here
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
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
            "listening.html", channel_name=channel_name, query_id=query_id, base_url=base_url
        )

    return render_template("index.html")

@app.route("/icd10", methods=["GET", "POST"])
def icd10():
    if request.method == "POST":
        # get the comma separated icd10 codes and turn into a list, stripping all spaces and capitalizing each item
        icd10_codes = [code.strip().upper() for code in request.form["icd10_codes"].split(",")]

        base_url = "https://galenai.co/" 

        # send question to GalenAI server
        url = f"{base_url}/api/v1/create-bulk-icd10-streaming-channel/"
        payload = {'codes': icd10_codes}
        token = f"token 61cbb3ba57ef2e7d92bc1f1161a87fbd3922acca" #your token here
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
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
        return render_template("listening_icd.html", channel_name=channel_name, query_id=query_id, base_url=base_url)

    return render_template("icd10.html")

@app.route("/stewardship", methods=["GET", "POST"])
def stewardship():
    if request.method == "POST":
        base_url = "http://localhost:8000"
        infection = request.form["infection"]  # get infection from user
        age = int(request.form["age"]) if request.form['age'] else None  # get age from user
        weight = int(request.form["weight"]) if request.form['weight'] else None # get weight from user
        crcl = int(request.form["crcl"]) if request.form['crcl'] else None # get crcl from user
  
        liver_disease = False
        if "liver_disease" in request.form:
            liver_disease = True

        # send question to GalenAI server
        url = f"{base_url}/api/v1/create-stewardship-streaming-channel/"
        payload = {"infection": infection}
        if age:
            payload["age"] = age
        if weight:
            payload["weight"] = weight
        if crcl:
            payload["crcl"] = crcl
        if liver_disease:
            payload["liver_disease"] = liver_disease

        token = f"token 61cbb3ba57ef2e7d92bc1f1161a87fbd3922acca" #your token here

        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            return render_template("stewardship.html", error=response.json()["detail"])

        channel_name = response.json()["channel_name"]
        query_id = response.json()["query_id"]
        
        return render_template("listening_stewardship.html", channel_name=channel_name, query_id=query_id, base_url=base_url)

    return render_template("stewardship.html")


if __name__ == "__main__":
    app.run(debug=True)
