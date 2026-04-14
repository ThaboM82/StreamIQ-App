from flask import Flask, request, jsonify
from streamiq import get_spark, tokenize, log_experiment, predict_intent
from streamiq.transcriber import transcribe_audio

app = Flask(__name__)

# Existing endpoints (process, logs, transcribe) stay as they are
# Now we add Big Data + Predict

@app.route("/bigdata", methods=["GET"])
def bigdata_demo():
    """
    Demo endpoint: load CSV with Spark and return summary + aggregations.
    """
    spark = get_spark()
    df = spark.read.csv("streamiq/data/call_center_prepared.csv", header=True, inferSchema=True)

    record_count = df.count()
    schema = [f"{field.name}:{field.dataType}" for field in df.schema.fields]

    # Aggregation: issues per agent
    issues_per_agent = (
        df.groupBy("agent")
          .count()
          .orderBy("count", ascending=False)
          .collect()
    )
    issues_summary = [{"agent": row["agent"], "count": row["count"]} for row in issues_per_agent]

    # Aggregation: top complaint categories
    complaints = (
        df.groupBy("issue")
          .count()
          .orderBy("count", ascending=False)
          .collect()
    )
    complaint_summary = [{"issue": row["issue"], "count": row["count"]} for row in complaints]

    return jsonify({
        "records": record_count,
        "schema": schema,
        "issues_per_agent": issues_summary,
        "top_complaints": complaint_summary
    })


@app.route("/predict", methods=["POST"])
def predict():
    """
    Demo endpoint: predict intent category from text.
    """
    data = request.get_json()
    text = data.get("text", "")

    prediction = predict_intent(text)

    # Log with MLflow
    log_experiment(
        run_name="PredictIntentDemo",
        params={"text": text},
        metrics={"prediction": prediction}
    )

    return jsonify({"text": text, "prediction": prediction})


@app.route("/tokenize", methods=["POST"])
def tokenize_text():
    """
    Demo endpoint: tokenize text using HuggingFace.
    """
    data = request.get_json()
    text = data.get("text", "")

    tokens = tokenize(text)

    return jsonify({
        "text": text,
        "input_ids": tokens["input_ids"].tolist(),
        "attention_mask": tokens["attention_mask"].tolist()
    })


if __name__ == "__main__":
    app.run(port=8000, debug=True)
