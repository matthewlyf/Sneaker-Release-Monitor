import os
import time
import re
import requests
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import smtplib

# Define sneaker keywords for filtering
NIKE_SHOE_KEYWORDS = [
    "Low", "High", "Air Force", "Dunk", "Air Jordan", "Retro", "Blazer",
    "VaporMax", "Zoom", "Pegasus", "Trail", "Flyknit", "Zoom Fly", "Infinity Run"
]

def get_time_left(release_date_str):
    """Calculate the time left until the release date."""
    date_match = re.search(r'(\d{1,2}-\d{1,2}) at (\d{1,2}:\d{2} [a,p].m.)', release_date_str)
    if not date_match:
        raise ValueError(f"Unexpected date format: {release_date_str}")
    
    date_part, time_part = date_match.groups()
    current_year = datetime.now().year
    time_part = time_part.replace('.', '')
    release_date = datetime.strptime(f"{current_year}-{date_part} {time_part}", "%Y-%m-%d %I:%M %p")
    time_left = release_date - datetime.now()

    if time_left.total_seconds() < 0:
        return "Already Dropped", 0

    days, remainder = divmod(time_left.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    return f"{int(days)} days {int(hours)} hours {int(minutes)} minutes", time_left.total_seconds() / 3600

def get_urgency_color(hours_left, time_left_str):
    """Determine urgency color based on time left."""
    if time_left_str == "Already Dropped":
        return "#A9A9A9"
    elif hours_left <= 24:
        return "#FF5733"
    elif hours_left <= 72:
        return "#FFC300"
    return "#008000"

def send_email(subject, body, image_paths):
    """Send an email with the specified subject, body, and attached images."""
    smtp_server = "smtp.gmail.com"
    sender_email = os.getenv('SENDER_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    for img_path in image_paths:
        with open(img_path, 'rb') as img_file:
            mime_image = MIMEImage(img_file.read(), name=os.path.basename(img_path))
            mime_image.add_header('Content-ID', f"<{os.path.basename(img_path)}>")
            mime_image.add_header('Content-Disposition', 'inline', filename=os.path.basename(img_path))
            msg.attach(mime_image)

    with smtplib.SMTP_SSL(smtp_server, 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    print("Email sent successfully!")

def is_shoe(product_name):
    """Check if a product name contains any sneaker-related keywords."""
    return any(keyword in product_name for keyword in NIKE_SHOE_KEYWORDS)

def scrape_nike_releases(url):
    """Scrape Nike's website for sneaker releases."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    releases = []
    for figure in soup.find_all('figure'):
        product_details = figure.find('a', class_='ncss-col-sm-8')
        product_name = product_details.find('h3', class_='headline-5').get_text() if product_details else None
        available_date = product_details.find('div', class_='available-date-component').get_text() if product_details else None
        img_tag = figure.find('img')
        image_url = img_tag['src'] if img_tag else 'no img url'
        product_url = figure.find('a', href=True)['href'] if figure.find('a', href=True) else ''

        if product_name and available_date:
            releases.append({
                "product": product_name,
                "available_date": available_date,
                "image_url": image_url,
                "url": f"https://www.nike.com{product_url}"
            })

    return pd.DataFrame(releases)

def update_releases(new_df, old_file_path):
    """Compare new releases with old data and update."""
    if os.path.exists(old_file_path):
        old_df = pd.read_csv(old_file_path)
    else:
        old_df = pd.DataFrame(columns=new_df.columns)

    difference = pd.merge(old_df, new_df, how='outer', indicator=True)
    new_releases = difference[difference['_merge'] == 'right_only'].drop('_merge', axis=1)
    removed_releases = difference[difference['_merge'] == 'left_only'].drop('_merge', axis=1)

    new_df.to_csv(old_file_path, index=False)
    return new_releases, removed_releases

def format_email_body(releases):
    """Format the email body with product details."""
    body = """
    <html>
    <body>
        <h1>New Sneaker Releases</h1>
    """
    for _, row in releases.iterrows():
        time_left_str, hours_left = get_time_left(row['available_date'])
        urgency_color = get_urgency_color(hours_left, time_left_str)
        body += f"""
        <div>
            <img src="{row['image_url']}" alt="{row['product']}" style="width: 150px;"/>
            <p><strong>{row['product']}</strong></p>
            <p>Release Date: {row['available_date']}</p>
            <p style="color: {urgency_color};">{time_left_str}</p>
            <a href="{row['url']}">View Product</a>
        </div>
        <hr/>
        """
    body += "</body></html>"
    return body

if __name__ == "__main__":
    NIKE_URL = "https://www.nike.com/ca/launch?s=upcoming"
    OLD_DATA_FILE = "old_data.csv"
    IMAGE_PATHS = ["path/to/logo.png", "path/to/banner.png"]

    while True:
        new_releases_df = scrape_nike_releases(NIKE_URL)
        new_releases_df = new_releases_df[new_releases_df['product'].apply(is_shoe)]
        new_releases, removed_releases = update_releases(new_releases_df, OLD_DATA_FILE)

        if not new_releases.empty:
            email_body = format_email_body(new_releases)
            send_email("New Sneaker Releases Found!", email_body, IMAGE_PATHS)
        else:
            print("No new releases found.")

        time.sleep(3600)  # Wait an hour before scraping again
