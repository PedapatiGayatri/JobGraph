# JobGraph

JobGraph is a graph-powered job search and recommendation web application built using Python, Flask, Neo4j Driver, and CognoDB.

## Project Overview

JobGraph connects candidates, skills, jobs, and companies using a graph database.

The application allows users to:

- Search for jobs based on skills
- View required skills for each job
- See company and location information
- View recommended jobs based on candidate skills
- See the number of matching skills for each recommended job

## Technologies Used

- Python
- Flask
- CognoDB
- Neo4j Python Driver
- Cypher
- HTML
- CSS

## Graph Data Model

The application uses the following nodes:

- Candidate
- Skill
- Job
- Company

Relationships:

- Candidate -[:HAS_SKILL]-> Skill
- Job -[:REQUIRES]-> Skill
- Job -[:BELONGS_TO]-> Company

## Example Graph

Candidate
↓ HAS_SKILL
Skill
↑ REQUIRES
Job
↓ BELONGS_TO
Company

## Sample Cypher Queries

### Find skills required by a job

```cypher
MATCH (j:Job {title: "Junior Data Analyst"})
      -[:REQUIRES]->(s:Skill)
RETURN s.name AS skill