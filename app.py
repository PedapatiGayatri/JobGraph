from flask import Flask, render_template, request
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/jobs")
def jobs():
    skill = request.args.get("skill", "").strip()

    results = []

    if skill:
        query = """
        MATCH (j:Job)-[:REQUIRES]->(s:Skill)
        WHERE toLower(s.name) = toLower($skill)

        OPTIONAL MATCH (j)-[:BELONGS_TO]->(c:Company)

        OPTIONAL MATCH (j)-[:REQUIRES]->(required:Skill)

        OPTIONAL MATCH (candidate:Candidate {name: "Gayatri"})
               -[:HAS_SKILL]->(matched:Skill)
              <-[:REQUIRES]-(j)


        RETURN
        j.title AS job,
        j.location AS location,
        c.name AS company,
        collect(DISTINCT required.name) AS skills,
        count(DISTINCT matched) AS matching_skills
        ORDER BY matching_skills DESC, j.title
        """

        try:
            with driver.session() as session:
                result = session.run(query, skill=skill)

                results = [
                     {
                        "job": record["job"],
                        "location": record["location"],
                        "company": record["company"],
                        "skills": record["skills"],
                        "matching_skills": record["matching_skills"]
                     }
                     for record in result
                ]

        except Exception as e:
            return f"Database error: {str(e)}", 500

    return render_template(
        "jobs.html",
        skill=skill,
        results=results
    )


@app.route("/recommendations")
def recommendations():

    query = """
    MATCH (candidate:Candidate {name: "Gayatri"})
          -[:HAS_SKILL]->(skill:Skill)
          <-[:REQUIRES]-(job:Job)

    OPTIONAL MATCH (job)-[:BELONGS_TO]->(company:Company)

    OPTIONAL MATCH (job)-[:REQUIRES]->(required:Skill)

    RETURN
        job.title AS job,
        job.location AS location,
        company.name AS company,
        collect(DISTINCT required.name) AS skills,
        count(DISTINCT skill) AS matching_skills
    ORDER BY matching_skills DESC, job.title
    """

    try:
        with driver.session() as session:
            result = session.run(query)

            results = [
                {
                    "job": record["job"],
                    "location": record["location"],
                    "company": record["company"],
                    "skills": record["skills"],
                    "matching_skills": record["matching_skills"]
                }
                for record in result
            ]

        return render_template(
            "recommendations.html",
            results=results
        )

    except Exception as e:
        return f"Database error: {str(e)}", 500
if __name__ == "__main__":
    app.run(debug=True)