Clair Streaming Demo
============

This is a Flask application that allows users to submit clinical queries and retrieve responses using the Clair server. The application uses server-sent events (SSE) to stream the generated text back to the client as it becomes available.

Installation
------------

1.  Clone the repository:
    
    
    `git clone https://github.com/Jonathan-Adly/clair_streaming_demo`
    
2.  Install the required dependencies using pip:
    
    
    `pip install -r requirements.txt`
    

Configuration
-------------

Before running the application, you need to provide your Clair access token. You can get a Clair access token by making  developer account at https://askclair.ai . Feel free to contact us at hello@askclair.ai . 

Follow these steps:

1.  Open the `app.py` file.
2.  Locate the line `TOKEN = ""`.
3.  Replace `TOKEN` with your actual Clair access token.

You should use enviromental variables in production.

Usage
-----

To start the Flask application, run the following command:

`flask run`

This will start the Flask development server, and you should see the application running on `http://localhost:5000`.

### Submitting a Query

1.  Open your web browser and navigate to `http://localhost:5000`.
2.  Enter your clinical query in the input field provided.
3.  Click the "Submit" button or press Enter to submit the query.

The application will send the question to the Clair server and retrieve a streaming channel for receiving the generated text.

### Listening for Responses

Once the query has been submitted and the streaming channel has been obtained, the application will render the `listening.html` template. This page allows you to listen for responses as they become available. H

1.  Click the "Start Listening" button to initiate the connection and start receiving events.
    
2.  The page will update with the generated answer, context, and references as they are received from the Clair server.
    
3.  Once the stream ends, the console will display a message indicating that the stream has ended.
    

### Retrieving Full Details

After the query has finished streaming, you can retrieve the full details by using the `query_id`. It is recommended to save the `query_id` in your database for later retrieval.

Contributing
------------

If you'd like to contribute to this project, please follow these steps:

1.  Fork the repository on GitHub.
2.  Create a new branch with a descriptive name for your feature or bug fix.
3.  Commit your changes and push the branch to your fork.
4.  Submit a pull request explaining your changes and why they should be merged.

License
-------

This project is licensed under the [MIT License](LICENSE).
