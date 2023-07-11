## Import the necessary packages
import smtplib
import datetime
import json
import random
import logging
from email.message import EmailMessage
from notion_client import Client


## Notion integration variables
notion_token = 'secret_AthSzZhAx5VuhyQVsX8lv8I16KzaBqEXE6gc3V0zj8v'
notion_database = '9fc2120788a94f189bc8a384ac6611c3'


## Email configuration
smtp_server = "smtp.gmail.com"
smtp_port_tls = 587
#smtp_port_ssl = 465
email_address = "marco.caloba10@gmail.com"
email_password = "qdqogpmqsyvtkist"
recipient_email = "marco_caloba@hotmail.com"


## Set up the log file
logging.basicConfig(filename="script.log", level=logging.ERROR)


## Saving the Notion's page data as a json file for easier inspection
def write_dict_to_file_as_json(content, file_name):
    content_as_json_str = json.dumps(content)
    
    with open(file_name, 'w') as f:
        f.write(content_as_json_str)


## Reading the Notion's page data
def read_text(client, page_id):
    response = client.blocks.children.list(block_id=page_id)
    return response['results']


## Read the properties of a database (?)
def safe_get(data, dot_chained_keys):
    keys = dot_chained_keys.split('.')
    for key in keys:
        try:
            if isinstance(data, list):
                data = data[int(key)]
            else:
                data = data[key]
        except (KeyError, TypeError, IndexError):
            return None
    return data


## Get five random numbers from all quotes
def get_random_numbers(n):
    if n < 5:
        print("Error: 'n' must be greater than or equal to 5.")
        return
    
    numbers = random.sample(range(1, n + 1), 5)
    return numbers


## Prepare the e-mail
def e_mail_prep(string):
    message = EmailMessage()
    message["From"] = email_address
    message["To"] = recipient_email
    message["Subject"] = f"Daily Quotes - {datetime.date.today()}"
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
        client = Client(auth=notion_token)
        db_info = client.databases.retrieve(database_id=notion_database)
        #write_dict_to_file_as_json(db_info, 'db_info.json')
        db_rows = client.databases.query(database_id=notion_database)
        #write_dict_to_file_as_json(db_rows, 'db_rows.json')
        simple_rows = []
        
        for row in db_rows['results']:
            content = row['properties']['Content']['title']
            quote = ''
            
            for line in range(0, len(content)):
                quote += safe_get(row, 'properties.Content.title.' + str(line) + '.plain_text')
            
            author = safe_get(row, 'properties.Author.rich_text.0.plain_text')
            origin = safe_get(row, 'properties.Origin.rich_text.0.plain_text')
            date = safe_get(row, 'properties.Date.date.start')
            simple_rows.append({
                'Content': quote,
                'Author': author,
                'Origin': origin,
                'Date': date
                })
        
        #write_dict_to_file_as_json(simple_rows, 'simple_rows.json')
        
        numbers = get_random_numbers(len(simple_rows))
        string = ""
        
        for num in numbers:
            cont = simple_rows[num-1]['Content']
            auth = simple_rows[num-1]['Author']
            orgn = simple_rows[num-1]['Origin']
            dt = simple_rows[num-1]['Date']
            
            if orgn == None:
                string += '"' + cont + '"\n' + auth + ' - ' + dt + '\n\n'
            else:
                string += '"' + cont + '"\n' + auth + ', ' + orgn + ' - ' + dt + '\n\n'
        
        intro = "Morning boss!\nHere are five quotes you saved:\n\n"
        outro = "\nHave a great day!"
        
        message = e_mail_prep(intro + string + outro)
        send_e_mail(message)
        
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