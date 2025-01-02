## Import the necessary packages
import smtplib
import datetime
import json
import random
import logging
from email.message import EmailMessage
import csv


## For more information about configuration please go here https://docs.python.org/3/library/smtplib.html
## Email configuration
smtp_server = "smtp.gmail.com"
smtp_port_tls = 587
#smtp_port_ssl = 465
email_address = "asdf@asfd.com"
email_password = "password here (use app password if possible"
recipient_email = "asdfasdf@asdfasdf.com"


## Set up the log file
logging.basicConfig(filename="script.log", level=logging.ERROR)


## Saving the Notion's page data as a json file for easier inspection
def read_prompt_csv(file_name):
    with open(file_name, 'r') as file:
        csv_reader = csv.DictReader(file)
        prompts = [row for row in csv_reader]
    return prompts


def update_csv(file_name, prompts):
    with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Prompt', 'Done'])
        for dictionary in prompts:
            writer.writerow(dictionary.values())

## Get five random numbers from all quotes
def get_random_numbers(n):
    number = random.randint(0,n)
    return number


## Prepare the e-mail
def e_mail_prep(string):
    message = EmailMessage()
    message["From"] = email_address
    message["To"] = recipient_email
    message["Subject"] = f"Poetry Prompt - {datetime.date.today()}"
    message.set_content(string)
    return message


## Send the e-mail
def send_e_mail(message):
    with smtplib.SMTP(smtp_server, smtp_port_tls) as server:
        server.starttls()
        server.login(email_address, email_password)
        server.send_message(message)


## Main function
def main():
    try:
        file_path='path_to_file'
        prompts = read_prompt_csv(file_path)
        prompt_cnt=len(prompts)

        done = 1
        while done == 1:
            number = get_random_numbers(prompt_cnt)
            if prompts[number]['Done'] == 1:
                done = 1
            else:
                prompts[number]['Done'] = 1
                done = 0
                content = prompts[number]['Prompt']


        intro = "Morning!\n\nHere is today's prompt:\n\n"
        outro = "\n\nNow Start Writing!"
        
        message = e_mail_prep(intro + content + outro)
        send_e_mail(message)
        update_csv(file_path, prompts)

    except Exception as e:
        logging.exception("An error occurred during script execution:")
        
        # Prepare error notification email
        error_message = f"An error occurred in the script:\n\n{str(e)}"
        error_email = EmailMessage()
        error_email["From"] = email_address
        error_email["To"] = recipient_email
        error_email["Subject"] = "Script Error Notification"
        error_email.set_content(error_message)
        
        # Send error notification email
        with smtplib.SMTP(smtp_server, smtp_port_tls) as server:
            server.starttls()
            server.login(email_address, email_password)
            server.send_message(error_email)


## Starting block
if __name__ == '__main__':
    main()