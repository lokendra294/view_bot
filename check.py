from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up ChromeDriver path
service = Service("C:/Users/lenovo/Desktop/view_bot/chromedriver/chromedriver-win64/chromedriver.exe")  # Update the path if needed

# Set Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment for headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")

# Use a context manager to ensure proper resource management
try:
    # Launch browser
    with webdriver.Chrome(service=service, options=chrome_options) as driver:
        # Test a website
        driver.get("https://www.google.com")
        
        # Wait for the title to be present
        WebDriverWait(driver, 10).until(EC.title_contains("Google"))
        
        print("Title of the page is:", driver.title)

except Exception as e:
    print("An error occurred:", e)