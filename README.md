# JobGraph

JobGraph is a graph-powered job search and recommendation web application built using Python, Flask, the Neo4j Python Driver, and CognoDB.

## Project Overview

JobGraph connects candidates, skills, jobs, and companies using a graph database.

The application allows users to:

- Search for jobs based on skills
- View required skills for each job
- See company and location information
- View recommended jobs based on candidate skills
- See the number of matching skills for each recommended job

The application is designed to demonstrate how graph relationships can be used to provide skill-based job search and recommendations.

---

## Why a Graph Database?

A graph database is a natural fit for JobGraph because the application focuses on relationships between candidates, skills, jobs, and companies.

A candidate can have multiple skills, a job can require multiple skills, and multiple jobs can share the same skills. These relationships can be traversed directly to identify suitable jobs and calculate matching skills.

In a relational database, these operations would require multiple tables and joins. A graph database makes relationship-based queries such as Candidate → Skill → Job straightforward using Cypher.

The graph model also makes it easier to extend the application in the future with features such as skill-gap analysis, related jobs, and additional recommendation logic.

---

## Technologies Used

- Python
- Flask
- CognoDB
- Neo4j Python Driver
- Cypher / openCypher
- HTML
- CSS
- Git
- GitHub

---

## Graph Data Model

### Nodes

The application uses the following nodes:

- `Candidate`
- `Skill`
- `Job`
- `Company`

### Relationships

The application uses the following relationships:

- `Candidate -[:HAS_SKILL]-> Skill`
- `Job -[:REQUIRES]-> Skill`
- `Job -[:BELONGS_TO]-> Company`

### Graph Structure

```text
Candidate
    |
    | HAS_SKILL
    v
  Skill
    ^
    | REQUIRES
    |
   Job
    |
    | BELONGS_TO
    v
 Company
```

The graph allows the application to traverse relationships between candidates, skills, jobs, and companies.

---

## Example Graph Data

Example jobs include:

- Junior Data Analyst
- Cloud Support Associate

Example skills include:

- Python
- SQL
- Excel
- Power BI
- AWS

The seed script creates the sample candidates, skills, jobs, companies, and their relationships.

---

## Main Cypher Queries

### 1. Find skills required by a job

```cypher
MATCH (j:Job {title: "Junior Data Analyst"})
      -[:REQUIRES]->(s:Skill)
RETURN s.name AS skill
```

This query finds all skills required by a particular job.

---

### 2. Search jobs by skill

The application uses a parameterized query to search for jobs based on the skill entered by the user.

```cypher
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
```

The `$skill` value is passed as a parameter from the Python application.

This query:

1. Finds jobs requiring the searched skill.
2. Finds the company associated with each job.
3. Retrieves all required skills.
4. Traverses from the candidate to their skills and then to jobs.
5. Counts the candidate's matching skills.
6. Orders the results by the number of matching skills.

---

### 3. Multi-hop candidate-job matching

```cypher
MATCH (candidate:Candidate {name: "Gayatri"})
      -[:HAS_SKILL]->(skill:Skill)
      <-[:REQUIRES]-(job:Job)

RETURN
candidate.name AS candidate,
job.title AS job,
collect(skill.name) AS matchingSkills
```

This query performs a multi-hop traversal:

```text
Candidate → Skill → Job
```

It finds jobs connected to a candidate through skills that the candidate already has.

This demonstrates one of the main advantages of using a graph database for the application.

---

### 4. Job recommendations

```cypher
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
```

This query recommends jobs based on the skills shared between the candidate and each job.

Jobs are ordered by the number of matching skills so that jobs with more matching skills appear first.

---

## Parameterized Queries

The application uses the official Neo4j Python Driver to execute Cypher queries.

User-provided skills are passed as parameters rather than being concatenated directly into Cypher.

For example:

```python
result = session.run(query, skill=skill)
```

The Cypher query uses:

```cypher
$skill
```

as the parameter.

This keeps user input separate from the Cypher query and avoids constructing Cypher using string concatenation.

---

## Data Loading

The `seed.py` script is included in the repository to create and load the sample graph data.

The seed data includes:

- Candidates
- Skills
- Jobs
- Companies
- Candidate-to-skill relationships
- Job-to-skill relationships
- Job-to-company relationships

Run the seed script with:

```bash
python seed.py
```

---

## Setup and Run

### 1. Clone the repository

```bash
git clone https://github.com/PedapatiGayatri/JobGraph.git
```

Move into the project directory:

```bash
cd JobGraph
```

### 2. Create a Python virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Create a CognoDB Cloud instance

Create a CognoDB Cloud account:

https://console.cognodb.com/signup

Create a free CognoDB instance and save the generated connection URI and password.

The application connects to CognoDB using the official Neo4j Python Driver over the Bolt protocol.

### 6. Configure environment variables

Create a local `.env` file containing the CognoDB connection details used by the application.

The application reads the following environment variables:

```text
COGNODB_URI
COGNODB_USERNAME
COGNODB_PASSWORD
```

Example:

```text
COGNODB_URI=your-cognodb-bolt-uri
COGNODB_USERNAME=cognodb
COGNODB_PASSWORD=your-password
```

Do not commit the `.env` file to GitHub.

The `.gitignore` file excludes `.env` from version control.

### 7. Load the graph data

Run:

```bash
python seed.py
```

### 8. Start the Flask application

Run:

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

---

## Application Features

### Skill-Based Job Search

Users can enter a skill such as:

- Python
- SQL
- Excel
- Power BI
- AWS

The application returns jobs that require the selected skill.

### Job Information

Each job result displays:

- Job title
- Company
- Location
- Required skills
- Number of matching candidate skills

### Job Recommendations

The recommendation page finds jobs connected to the candidate through shared skills.

Jobs are ranked based on the number of matching skills.

### Empty Search State

If no job matches the searched skill, the application displays a friendly message:

```text
No jobs found
```

The page also suggests example skills that can be searched.

---

## Error Handling

The application catches database errors and returns an HTTP 500 response when a database operation fails.

This prevents an unhandled database exception from crashing the Flask application.

---

## Project Structure

```text
JobGraph/
│
├── .gitignore
├── README.md
├── app.py
├── requirements.txt
├── seed.py
│
└── templates/
    ├── index.html
    ├── jobs.html
    └── recommendations.html
```

---

## Live Demo

**Live Application:**

https://jobgraph-3rdn.onrender.com

The hosted application allows users to search for jobs and view skill-based job recommendations without running the project locally.

---

## Screenshots

### 1. Home Page

Add your JobGraph home page screenshot below this section.
![alt text](
      <templates/screenshots/Screenshot (212).png>)


### 2. Job Search Results

Add a screenshot showing:

- Job title
- Company
- Location
- Required skills
- Matching skills
![alt text](

<templates/screenshots/Screenshot (219).png>)


### 3. Recommended Jobs

Add a screenshot showing recommended jobs and matching skill counts.
![alt text](

<templates/screenshots/Screenshot (220).png>)


### 4. CognoDB Graph

Add a screenshot showing the graph nodes and relationships in CognoDB.
![alt text](
      <templates/screenshots/Screenshot (221).png>)


---

## Future Improvements

Possible future improvements include:

- Allowing candidates to create and update their own profiles
- Adding more jobs, companies, and skills
- Adding skill-gap analysis
- Improving job ranking and recommendation logic
- Adding filters for location and job type
- Adding more graph-based recommendation features

---

## Author

**Gayatri Pedapati**

GitHub:

https://github.com/PedapatiGayatri/JobGraph