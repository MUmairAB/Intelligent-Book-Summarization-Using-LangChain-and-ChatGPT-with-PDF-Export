#Import the necessary libraries
import requests

#Define the API Endpoint URL
url = 'http://127.0.0.1:8000/summarize'

#Instantiate the document name that you want to summarize
doc_name = 'sample.pdf'

#Read the file that we want to summarize
file = {'file': open(doc_name, 'rb')}

#Make the POST request and get the response
response = requests.post(url=url, files=file)

#If we get HTTP 200 OK success status then save the file
if response.status_code == 200:
    with open('summary.pdf', 'wb') as f:
        f.write(response.content)
else:
    print("Sorry! There is some error in the respnse from the API.")
