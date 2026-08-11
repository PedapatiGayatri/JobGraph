from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def create_graph(tx):
    query = """
    // Create candidate
    MERGE (c:Candidate {name: $candidate_name})
    SET c.education = $education

    // Create skills
    MERGE (python:Skill {name: "Python"})
    MERGE (sql:Skill {name: "SQL"})
    MERGE (excel:Skill {name: "Excel"})
    MERGE (powerbi:Skill {name: "Power BI"})
    MERGE (aws:Skill {name: "AWS"})

    // Create candidate skill relationships
    MERGE (c)-[:HAS_SKILL]->(python)
    MERGE (c)-[:HAS_SKILL]->(sql)
    MERGE (c)-[:HAS_SKILL]->(excel)

    // Create companies
    MERGE (company1:Company {name: "TechNova Solutions"})
    MERGE (company2:Company {name: "DataBridge Technologies"})

    // Create jobs
    MERGE (job1:Job {
        title: "Junior Data Analyst"
    })
    SET job1.location = "Hyderabad"

    MERGE (job2:Job {
        title: "Cloud Support Associate"
    })
    SET job2.location = "Bangalore"

    // Connect jobs to companies
    MERGE (job1)-[:BELONGS_TO]->(company1)
    MERGE (job2)-[:BELONGS_TO]->(company2)

    // Job requirements
    MERGE (job1)-[:REQUIRES]->(python)
    MERGE (job1)-[:REQUIRES]->(sql)
    MERGE (job1)-[:REQUIRES]->(excel)
    MERGE (job1)-[:REQUIRES]->(powerbi)

    MERGE (job2)-[:REQUIRES]->(python)
    MERGE (job2)-[:REQUIRES]->(aws)
    """

    tx.run(
        query,
        candidate_name="Gayatri",
        education="B.Tech Electronics and Communication Engineering"
    )


try:
    with driver.session() as session:
        session.execute_write(create_graph)

    print("Graph data created successfully!")

finally:
    driver.close()