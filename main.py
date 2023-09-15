from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from twilio.rest import Client
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Set up LinkedIn login session using Selenium
driver = webdriver.Chrome()
driver.get('https://www.linkedin.com')
# Fill in your LinkedIn login credentials
username = driver.find_element(By.ID, 'session_key')
username.send_keys('your_email@example.com')
password = driver.find_element(By.ID, 'session_password')
password.send_keys('your_password')
password.send_keys(Keys.RETURN)

# Define job search criteria
search_keywords = "software engineer"
search_location = "San Francisco"

# Perform a job search on LinkedIn
search_box = driver.find_element(By.ID,'input.search-global-typeahead__input')
# Define the search box element
search_box = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search"]')

# Send search keywords and press enter
search_box.send_keys(search_keywords)
search_box.send_keys(Keys.RETURN)

# Wait for search results to load (you may need to adjust the sleep duration)
import time
time.sleep(5)

# Extract job listings (for demonstration purposes, only first 5 are shown)
job_listings = driver.find_elements_by_css_selector('li.job-card-container')

# Twilio configuration
twilio_account_sid = "your_account_sid"
twilio_auth_token = "your_auth_token"
twilio_phone_number = "your_twilio_phone_number"
your_phone_number = "your_phone_number"

client = Client(twilio_account_sid, twilio_auth_token)

# Flag to check if matching job was found
match_found = False

for i, job in enumerate(job_listings[:5], start=1):
    job_title = job.find_element_by_css_selector('h3').text
    job_company = job.find_element_by_css_selector('h4').text
    job_location = job.find_element_by_css_selector('.job-card-container__metadata-item').text

    print(f"Job {i} - Title: {job_title}")
    print(f"Company: {job_company}")
    print(f"Location: {job_location}")
    print("\n")

    # Check if job matches criteria (e.g., contains the keyword)
    if search_keywords.lower() in job_title.lower() or search_keywords.lower() in job_company.lower():
        match_found = True

# Close the Selenium browser window
# driver.quit()

# If a match is found, send a text message
if match_found:
    message = client.messages.create(
        body="A job matching your criteria has been found on LinkedIn.",
        from_=twilio_phone_number,
        to=your_phone_number
    )
    print("Text message sent:", message.sid)
