import streamlit as st
from streamiq.spark_utils import get_spark

def load_dataset(filename: str):
    spark = get_spark("StreamIQDashboard")
    df = spark.read.csv(f"streamiq/data/{filename}", header=True, inferSchema=True)
    return df

def show_summary(df):
    st.write("### Schema")
    schema = [f"{field.name}: {field.dataType}" for field in df.schema.fields]
    st.json(schema)

    st.write("### Record Count")
    st.metric("Rows", df.count())

    st.write("### Issues per Agent")
    issues_per_agent = (
        df.groupBy("agent").count().orderBy("count", ascending=False).toPandas()
    )
    st.bar_chart(issues_per_agent.set_index("agent"))

    st.write("### Top Complaints")
    complaints = (
        df.groupBy("issue").count().orderBy("count", ascending=False).toPandas()
    )
    st.bar_chart(complaints.set_index("issue"))

def run():
    """Entry point for Streamlit sidebar navigation."""
    st.title("📊 Big Data Demo")
    dataset_choice = st.selectbox(
        "Choose a dataset",
        ["call_center_prepared.csv", "claims_prepared.csv", "call_center.csv", "test.csv"]
    )
    if st.button("Load Dataset"):
        df = load_dataset(dataset_choice)
        show_summary(df)
