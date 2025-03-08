import os
from flask import Flask, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Add root route
    @app.route("/")
    def index():
        return "Index Page"
    
    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"
    
    @app.route("/analyze_sentiment", methods=["POST"])
    def analyze_sentiment():
        # Get the text from the POST request
        text = request.json.get("text")
        if text:
            # Create a sentiment analyzer
            analyzer = SentimentIntensityAnalyzer()
            
            sentences = [text]
            scores = [analyzer.polarity_scores(sentence) for sentence in sentences]
            return jsonify(
                {"sentiments": scores}
            )
        else:
            return jsonify({"error": "No text provided"}), 400
    
    return app

# Create app instance for gunicorn
app = create_app()