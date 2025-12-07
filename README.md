# Mental Health Prediction & AI Support System

## Overview
This project is a comprehensive web application designed to assess mental health risks based on a 54-question survey. By utilizing Machine Learning (Random Forest/Logistic Regression), the system predicts potential risk levels and identifies the top 3 contributing factors for each user.

Beyond simple prediction, the platform offers an **AI-driven Chatbot** (powered by Ollama) that generates a "Chain-of-Thought" action plan tailored to the user's specific risk factors. The system includes detailed statistics, email reporting, and role-based access control.

## Key Features

* **Risk Prediction:** ML model analyzes survey responses to provide a risk score and identify key threat factors (Feature Importance).
* **Role-Based Access:**
    * **Anonymous:** Can take the survey and see the result score.
    * **Registered:** Access to historical data, "You vs. Population" statistics, email reports, and the AI Chatbot.
    * **Counselor/Admin:** Access to aggregated data and system management.
* **Interactive Statistics:** Visual breakdown of answers compared to the population average (per-question analysis).
* **AI Assistant:** Integrated LLM (Ollama) capable of conversation and generating a step-by-step action plan based on the user's top risk factors.
* **Automated Reporting:** Asynchronous email dispatch containing a summary of results and risk analysis.

## Tech Stack

### Backend & Infrastructure
* **OS:** Debian 13 (Running on HP EliteDesk hardware)
* **Language:** Python 3.11+
* **Framework:** Django 4.x
* **Database:** PostgreSQL
* **Server:** Gunicorn (WSGI) + Nginx (Reverse Proxy)
* **Security & Network:** Cloudflare (DNS, SSL, WAF, DDoS Protection)
* **Async Tasks:** Celery + Redis (for emails and heavy ML computations)

### Machine Learning & AI
* **Libraries:** Scikit-learn (Model training), Pandas (EDA)
* **LLM:** Ollama (Local/Self-hosted) for the Chatbot and Plan generation
* **Interpretation:** Feature Importance extraction

### DevOps & Tools
* **Email:** External SMTP Service (e.g., SendGrid / Mailgun / Amazon SES)
* **Backups:** Automated Bash scripts (Cron jobs)
* **Version Control:** Git (GitHub)

---

## Production Deployment

The application is deployed on a dedicated **Debian 13** server.

* **Web Server:** Nginx (Reverse Proxy) with SSL handled via Cloudflare.
* **App Server:** Gunicorn serving the Django application, managed by `systemd`.
* **Database:** PostgreSQL.

### Automated Backups
We utilize a custom Bash script triggered by `cron` to handle backups without using Docker containers.

**Script location:** `/scripts/backup_daily.sh`
**Function:**
1.  Creates a timestamped dump of the PostgreSQL database (`pg_dump`).
2.  Compresses uploaded media files (`tar`).
3.  Rotates backups (deletes files older than 7 days).

```bash
# Example Cron Entry (Runs every day at 3 AM)
0 3 * * * /path/to/project/scripts/backup_daily.sh >> /var/log/backup.log 2>&1
