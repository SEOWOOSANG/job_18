from flask import Flask, render_template, request, send_file
from scrapper import search_incruit
from file import save_to_csv

app = Flask(__name__)

@app.route("/")
def hello_world():
  return render_template("index.html")

@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  jobs = search_incruit(keyword)
  return render_template("search.html", keyword=keyword, jobs=enumerate(jobs)) 

@app.route("/file")
def file():
  keyword = request.args.get("keword")
  jobs = search_incruit(keyword)
  save_to_csv(jobs)
  return send_file("download.csv", as_attachment=True)

if __name__ == "__main__":
  app.run(debug=True)