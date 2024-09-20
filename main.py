from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
import time
import pandas as pd

# Automatically set up the WebDriver
chrome_driver_path = r'D:\Ajay - Viosa\chromedriver-win64\chromedriver.exe'  # Update with your actual path
driver = webdriver.Chrome(service=Service(chrome_driver_path))

# Configuration parameters
login_time = 50  # Time to allow user to scan the QR code
new_msg_time = 10  # Time to wait between opening new messages
send_msg_time = 15  # Time to wait between sending messages
country_code = 91  # Country code for the phone numbers

# Open WhatsApp Web and give time for login
driver.get('https://web.whatsapp.com')
print("Waiting for WhatsApp Web login...")
time.sleep(login_time)  # Pause to allow QR code scanning

# Function to send PDF with dynamic text to WhatsApp
def send_pdf_with_text(driver, num, pdf_path, text):
    try:
        print(f"Opening chat for {num}...")
        link = f'https://web.whatsapp.com/send/?phone={country_code}{num}&text={quote(text)}'
        driver.get(link)
        time.sleep(new_msg_time)  # Wait for the chat to load

        # Click on the attachment (paperclip) icon
        print("Clicking on attachment icon...")
        attachment_icon = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@title="Attach"]'))
        )
        attachment_icon.click()

        # Select 'Document' from the attachment options
        print("Selecting 'Document' to upload the PDF...")
        doc_option = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@accept="*"]'))  # For PDFs, '*'
        )
        doc_option.send_keys(pdf_path)  # Send the PDF file path

        # Wait for file to upload
        time.sleep(5)  # Adjust this if larger files take longer to upload

        # Click on the Send button
        print("Sending the PDF...")
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
        )
        send_button.click()

        print(f"PDF and message sent to {num}")
    except Exception as e:
        print(f"Failed to send message to {num}: {str(e)}")

# Read the data from a CSV file containing phone numbers, PDF paths, and message texts
print("Reading data from CSV file...")
data = pd.read_csv('data.csv')  # Update with the path to your CSV file

# The CSV file should have columns: 'Phone Number', 'PDF Path', 'Message'
for index, row in data.iterrows():
    num = row['Phone Number']
    pdf_path = row['PDF Path']
    # Create a personalized message
    text = f"Dear {row['Name']},\n\nGreetings from Viosa Learning!!!\n\nPFA your career assessment report.\nKindly use the link below to access the student dashboard.\n\nhttps://pca.viosa.in/\n\nEmail: {row['Email']}\nPassword: {row['Password']}\n\nRegards,\nTeam Viosa."


    # Send message and PDF
    send_pdf_with_text(driver, num, pdf_path, text)
    time.sleep(send_msg_time)  # Wait before sending the next message

# Close the browser after all messages are sent
print("All messages sent. Closing the browser...")
driver.quit()
