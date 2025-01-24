
# Sneaker Release Monitor

A Python script that scrapes Nike's website for upcoming sneaker releases, sends email alerts for new products, and calculates urgency based on release time. The tool highlights urgency with color-coded levels and tracks changes over time to notify you only about new releases.

## Features

- **Web Scraping**: Automatically retrieves upcoming sneaker releases from Nike's website.
- **Email Alerts**: Sends notifications with detailed product information, release dates, and product links.
- **Urgency Calculation**: Determines urgency levels (e.g., hours/days left) and highlights them with color codes.
- **Data Tracking**: Compares new sneaker releases with previously tracked data to avoid duplicate alerts.
- **HTML Email Design**: Alerts include product images, release information, and urgency highlights.

## Technologies Used

- **Python**: Core scripting language.
- **BeautifulSoup**: Web scraping library.
- **Pandas**: For data manipulation and comparison.
- **SMTP**: For sending email alerts.
- **dotenv**: To securely manage environment variables.

---

## Setup Instructions

Follow these steps to set up and run the Sneaker Release Monitor:

### 1. Clone the Repository
```bash
git clone https://github.com/matthewlyf/sneaker-release-monitor.git
cd sneaker-release-monitor
```

### 2. Install Dependencies
Ensure you have Python installed, then install the required libraries:
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project directory to securely store sensitive information:
```plaintext
SENDER_EMAIL=your_email@example.com
EMAIL_PASSWORD=your_email_password
RECEIVER_EMAIL=receiver_email@example.com
```

- **SENDER_EMAIL**: Your email address (e.g., Gmail) for sending alerts.
- **EMAIL_PASSWORD**: Your email password (use an app-specific password for Gmail).
- **RECEIVER_EMAIL**: The email address where alerts will be sent.

> **Note**: Never share your `.env` file or hardcode sensitive information in the script.

### 4. Run the Script
Execute the script to start monitoring sneaker releases:
```bash
python src/sneaker_monitor.py
```

---

## Example Email Output

### Sample Alert
**Product Name**: Air Jordan 1 High OG  
**Release Date**: October 15, 2023  
**Urgency Level**: Dropping in 2 days and 3 hours!  
**Link**: [View Product](https://www.nike.com)

---

## How It Works

### 1. Scraping Nike’s Website
- The script uses BeautifulSoup to scrape Nike’s launch page and extract product details like name, release date, and image URLs.

### 2. Data Comparison
- Compares newly scraped data with previously stored data in `old_data.csv` to identify new sneaker releases.

### 3. Email Alerts
- Sends an HTML email containing:
  - Product details
  - Release date
  - Countdown timer
  - Product image and link

### 4. Time Left Calculation
- The `get_time_left` function calculates days, hours, and minutes left until the release date.

---

## File Structure

```plaintext
sneaker-release-monitor/
│
├── src/
│   ├── sneaker_monitor.py        # Main Python script
│
├── examples/
│   ├── sneaker_email.png         # Example email output
│
├── .env.example                  # Sample environment variables file
├── old_data.csv                  # Tracks previous sneaker releases
├── requirements.txt              # Python dependencies
└── README.md                     # Documentation
```

---

## Dependencies

The following Python libraries are required (included in `requirements.txt`):
- `beautifulsoup4`
- `pandas`
- `python-dotenv`
- `requests`

Install them using:
```bash
pip install -r requirements.txt
```

---

## Known Issues

- **Website Changes**: If Nike updates its website structure, the scraping logic may need to be adjusted.
- **Email Configuration**: Ensure you use an app-specific password for Gmail to avoid authentication errors.
- **Time Zones**: The script assumes `America/New_York`. Update the timezone if needed.

---

## Future Enhancements

- Add support for other sneaker retailers (e.g., Adidas, Footlocker).
- Include a front-end dashboard for real-time monitoring.
- Schedule periodic checks using task schedulers like `cron` or `APScheduler`.

---

