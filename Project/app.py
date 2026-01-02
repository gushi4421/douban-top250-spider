import sys
import os
import pandas as pd
from flask import Flask, render_template

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import CSV_PATH

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)

app = Flask(
    __name__,
    static_folder=os.path.join(root_dir, "static"),
    template_folder=os.path.join(current_dir, "templates"),
)


def get_movie_data():
    """读取 CSV 数据"""
    csv_path = os.path.join(root_dir, CSV_PATH)
    if not os.path.exists(csv_path):
        return pd.DataFrame()
    df = pd.read_csv(csv_path)
    df = df.fillna("未知")
    return df


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/index")
def home():
    return index()


@app.route("/movie")
def movie():
    df = get_movie_data()
    if df.empty:
        datalist = []
    else:
        datalist = df.to_dict("records")
    return render_template("movie.html", movies=datalist)


@app.route("/score")
def score():
    df = get_movie_data()
    if df.empty:
        return render_template("score.html", score=[], num=[], num2=[], score2=[])

    rating_series = pd.to_numeric(df["nums-rating"], errors="coerce").dropna()
    rating_counts = rating_series.value_counts().sort_index()
    score_list = rating_counts.index.astype(str).tolist()
    num_list = rating_counts.values.tolist()

    year_series = pd.to_numeric(df["year"], errors="coerce").dropna()
    year_counts = year_series.astype(int).value_counts().sort_index()

    score2_list = year_counts.index.astype(str).tolist()
    num2_list = year_counts.values.tolist()

    res = dict(zip(score_list, num_list))

    return render_template(
        "score.html",
        score=score_list,
        num=num_list,
        res=res,
        num2=num2_list,
        score2=score2_list,
    )


@app.route("/word")
def word():
    return render_template("cloud.html")


@app.route("/team")
def team():
    return render_template("team.html")


@app.route("/aboutMe")
def aboutMe():
    return render_template("aboutMe.html")


if __name__ == "__main__":
    app.run(debug=True)
