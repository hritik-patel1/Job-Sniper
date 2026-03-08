import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import defaultdict


# EMAIL = "hritikpatel4775@gmail.com"
# PASSWORD = "dmsasbxngypubvic" # App password generated for this script. Do not use your main password.
# TO_EMAIL = "hritikpatel4775@gmail.com"

EMAIL = "hritiksamplle@gmail.com"
PASSWORD = "yyiaajwidacvvoyl" # App password generated for this script. Do not use your main password.
TO_EMAIL = "hritiksamplle@gmail.com"


def send_email(jobs):

    if not jobs:
        return

    company_jobs = defaultdict(list)

    for job in jobs:
        company_jobs[job["company"]].append(job)

    # Build subject with job counts
    subject_parts = []

    for company, jobs_list in company_jobs.items():
        subject_parts.append(f"{company.capitalize()}({len(jobs_list)})")

    subject = f"New Jobs ({len(jobs)}): " + ", ".join(subject_parts)

    body = ""

    for job in jobs:
        body += f"""
Company: {job['company']}
Title: {job['title']}
Location: {job['location']}
Link: {job['link']}

-----------------------
"""

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(EMAIL, PASSWORD)

    server.send_message(msg)

    server.quit()