# Machine-Learning-Modeling-and-Evaluation-internship


# Overview

This project implements a minimal **MLOps-style batch processing pipeline** in Python.
It demonstrates reproducibility, observability, and deployment readiness using Docker.



## 🚀 Features

* Config-driven execution using YAML
* Deterministic runs using a fixed random seed
* Data validation and error handling
* Rolling mean computation on `close` prices
* Binary signal generation
* Structured metrics output (`metrics.json`)
* Detailed logging (`run.log`)
* Dockerized for one-command execution


#📂 Project Structure

mlops-task/

* run.py
* config.yaml
* data.csv
* requirements.txt
* Dockerfile
* README.md
* metrics.json
* run.log

---

#How to Run Locally

# 1. Install dependencies

pip install -r requirements.txt

### 2. Run the script

python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log


# How to Run with Docker

#Build the Docker image

docker build -t mlops-task .

# Run the container

docker run --rm mlops-task

---

 📊 Output (metrics.json)

{
  "version": "v1",
  "rows_processed": 9996,
  "metric": "signal_rate",
  "value": 0.4991,
  "latency_ms": 183,
  "seed": 42,
  "status": "success"
}






