
# Sneaker Release Monitor

This Python script scrapes Nike's website for upcoming sneaker releases and sends email alerts for new products. It calculates urgency based on release time and provides color-coded urgency levels to help you keep track of your favorite sneaker drops.

---

## Features

- **Web Scraping**: Automatically retrieves upcoming sneaker releases from Nike's website.
- **Email Alerts**: Sends alerts for new sneaker releases with detailed product information and release dates.
- **Urgency Calculation**: Determines urgency levels (e.g., hours/days left) and highlights them with color codes.
- **Data Comparison**: Tracks sneaker releases over time, ensuring you only get alerts for new additions.
- **Elegant Email Design**: Emails include product details, images, and urgency highlights.

---

## Technologies Used

- **Python**: Core scripting language.
- **BeautifulSoup**: Web scraping library.
- **Pandas**: Data manipulation and comparison.
- **SMTP**: Sending email alerts.
- **dotenv**: For managing environment variables.

---

## Setup Instructions

Follow these steps to set up and run the Sneaker Release Monitor script:

### 1. Clone the Repository

```bash
git clone https://github.com/matthewlyf/sneaker-release-monitor.git
cd sneaker-release-monitor
```

### 2. Install Required Packages

Make sure you have Python installed. Then, install the required libraries:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project directory to securely store sensitive information:

```
EMAIL_USER=your_email@example.com
EMAIL_PASSWORD=your_email_password
RECEIVER_EMAIL=receiver_email@example.com
```

- `EMAIL_USER`: Your email address (e.g., Gmail) for sending alerts.
- `EMAIL_PASSWORD`: Your email password (use an **app password** for Gmail).
- `RECEIVER_EMAIL`: The email address where alerts will be sent.

**Note**: Never share your `.env` file or hardcode sensitive information in the script.

### 4. Run the Script

Execute the script to start monitoring sneaker releases:

```bash
python sneaker_release_monitor.py
```

---

## Example Email Output

Here’s an example of what the email alert looks like:

- **Product Name**: Air Jordan 1 High OG
- **Release Date**: October 15, 2023
- **Urgency Level**: Dropping in 2 days and 3 hours!
- **Link**: [View Product](https://www.nike.com)

---

## How It Works

1. **Scraping Nike’s Website**:
   - The script uses BeautifulSoup to scrape Nike’s launch page and extract product details like name, release date, and image URLs.
   
2. **Data Comparison**:
   - Compares newly scraped data with previously stored data to identify new sneaker releases.
   
3. **Email Alerts**:
   - Sends an HTML email with:
     - Product details
     - Release date
     - Countdown timer
     - Product image and link

4. **Time Left Calculation**:
   - The `get_time_left` function calculates days, hours, and minutes left until the release date.

---

## File Structure

```
sneaker-release-monitor/
│
├── sneaker_release_monitor.py   # Main Python script
├── old_data.csv                 # Tracks previous sneaker releases (generated automatically)
├── requirements.txt             # Python dependencies
├── .env.example                 # Sample environment variables
└── README.md                    # Documentation
```

---

## Dependencies

Ensure the following libraries are installed (via `requirements.txt`):

```
beautifulsoup4==4.10.0
pandas==1.5.3
python-dotenv==0.21.0
requests==2.28.1
```

Install with:
```bash
pip install -r requirements.txt
```

---

## Known Issues

1. **Website Changes**: If Nike updates its website structure, the scraping logic may need to be adjusted.
2. **Email Configuration**: Ensure you use an app-specific password for Gmail to avoid authentication errors.
3. **Time Zones**: The script assumes `America/New_York`. Update the timezone in the script if needed.

---

## Future Enhancements

- Add support for other sneaker retailers (e.g., Adidas, Footlocker).
- Include a front-end dashboard for real-time monitoring.
- Schedule periodic checks using a task scheduler like `cron` or `APScheduler`.

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute.

---

## Author

Created by **Matthew**. Feel free to contact me with any feedback or suggestions!

---

## Contribution

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

