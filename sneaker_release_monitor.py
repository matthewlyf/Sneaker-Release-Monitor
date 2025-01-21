# -*- coding: utf-8 -*-
"""
Nike Sneaker Release Monitor
Scrapes Nike's website for upcoming sneaker releases, sends email alerts for new products,
and calculates urgency based on release time.

Author: Matthew
Date: Oct 10, 2023
"""

import os
import pandas as pd
from datetime import datetime
import pytz
import requests
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Email configuration
SENDER_EMAIL = os.getenv('EMAIL_USER')
PASSWORD = os.getenv('EMAIL_PASSWORD')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')


def get_time_left(release_date_str):
    """
    Calculate the time left until a release date.

    Args:
        release_date_str (str): The release date string in the format "MM-DD at HH:mm a.m./p.m."

    Returns:
        tuple: A string representation of the time left and the total hours remaining.
    """
    date_match = re.search(r'(\d{1,2}-\d{1,2}) at (\d{1,2}:\d{2} [a,p].m.)', release_date_str)
    if not date_match:
        raise ValueError(f"Unexpected date format: {release_date_str}")

    date_part, time_part = date_match.groups()
    current_year = datetime.now().year
    time_part = time_part.replace('.', '')
    release_date = datetime.strptime(f"{current_year}-{date_part} {time_part}", "%Y-%m-%d %I:%M %p")
    time_left = release_date - datetime.now()

    days, remainder = divmod(time_left.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    return (
        f"{int(days)} days {int(hours)} hours {int(minutes)} minutes",
        time_left.total_seconds() / 3600
    )


def get_urgency_color(hours_left):
    """
    Determine urgency color based on time left.

    Args:
        hours_left (float): Total hours remaining.

    Returns:
        str: Hex color code for urgency level.
    """
    if hours_left <= 24:
        return "#FF5733"  # Red
    elif hours_left <= 72:
        return "#FFC300"  # Yellow
    else:
        return "#008000"  # Green


def send_email(subject, body):
    """
    Send an email alert.

    Args:
        subject (str): Email subject line.
        body (str): Email body (HTML).
    """
    if not SENDER_EMAIL or not PASSWORD or not RECEIVER_EMAIL:
        raise ValueError("Email credentials are not set in the environment variables.")

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject

    body = MIMEText(body, 'html')
    msg.attach(body)

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER_EMAIL, PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    server.quit()
    print("Email sent successfully")


def main():
    url = "https://www.nike.com/ca/launch?s=upcoming"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    new_data = []
    for figure in soup.find_all('figure'):
        date = figure.find('h2', class_='headline-5')
        img_tag = figure.find('img')
        product_details = figure.find('a', class_='ncss-col-sm-8')
        product_name = product_details.find('h3', class_='headline-5') if product_details else None
        available_date = product_details.find('div', class_='available-date-component') if product_details else None
        a_tag = figure.find('a', href=True)
        product_url = a_tag['href'] if a_tag else ''
        image_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else ''

        new_data.append({
            "product": product_name.get_text() if product_name else '',
            "available_date": available_date.get_text() if available_date else '',
            "url": f"https://www.nike.com{product_url}",
            "image_url": image_url
        })

    new_df = pd.DataFrame(new_data).dropna(subset=["product"])

    # Load old data if exists
    data_file = "old_data.csv"
    try:
        old_df = pd.read_csv(data_file)
    except FileNotFoundError:
        old_df = pd.DataFrame(columns=new_df.columns)

    # Find differences
    difference = pd.merge(old_df, new_df, how='outer', indicator=True).query('_merge == "right_only"').drop('_merge', axis=1)
    if not difference.empty:
        send_email("New Sneaker Releases Found!", "Check out the latest sneaker releases!")

    # Save updated data
    new_df.to_csv(data_file, index=False)


if __name__ == "__main__":
    main()
