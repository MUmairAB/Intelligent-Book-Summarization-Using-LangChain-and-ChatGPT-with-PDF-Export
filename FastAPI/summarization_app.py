#Import necessary libraries
from fpdf import FPDF
from fastapi import FastAPI, File, UploadFile
import os, uvicorn
from fastapi.responses import FileResponse
import shutil

#Instantiate the FastAPI app
app = FastAPI()

"""
This function reads the API key from the file
and stores it as an environment variable. If everything works out,
it returns 1 and if there is some error it will return 0.
"""
def extract_api():
    try:
        #Extract the API key as API_key
        from API_file import API_key
        #Create an Environment Variable named OPENAI_API_KEY to store the API_key

        os.environ["OPENAI_API_KEY"] = API_key
        return 1
    except Exception:
        return 0

"""
This function accepts the "file" object as parameter. It:
- reads the files from local "Uploaded_Files" directory
- Summarizes the file using LLMChain
- Returns the summary in the form of a string
"""
def summarization_ftn(file):
    #Load necessary libraries
    from langchain.chat_models import ChatOpenAI
    from langchain.chains.summarize import load_summarize_chain
    from langchain.document_loaders import PyPDFLoader
    import time, random

    ########_______Instantiate the Summarization Chain_______########

    #Instantiate the GPT-4 LLM from OpenAI
    llm = ChatOpenAI(model="gpt-4",
                     temperature=0.4,
                     max_tokens=500)
    
    #Instantiate the LangChain Summarization API
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    
    #########_____________Read the PDF Document_____________########

    #Read the PDF document
    loader = PyPDFLoader(file_path="Uploaded_Files/"+file.filename)
    documents = loader.load_and_split()

    #########____________PDF Text Pre-processing____________########
    """
    Here comes the PDF cleaning part. That is, remove some redundant text.
    But we are making a generic app, so we'll skip this part. But
    pre-processing steps can be added according to the client requirements.
    """

    ######____Apply the LLMChain to summarize the Document____######

    #Variable to store the summarized text
    summary = ""

    #Variable to store the length of words; used to make sure we send less than 10k tokens
    length = 0

    #Variable to store the page number of last request sent to OpenAI
    last_page = 0

    wait_time = 1.1
    for page_num in range(0,len(documents)):
        length = length + len(documents[page_num].page_content.split(" "))
        if length > 6500:
            summary = summary + " " + chain.run(documents[last_page:page_num])
            length = 0
            last_page = page_num
            #Since the ChatGPT takes a lot of time to process, let's 
            # print the progress along the way. So that we could know
            # the prgram is working and is not stuck anywhere
            print("Current Page Number:",page_num)
            print("\n\t\t\t\tSystem is waiting to ensure 10k TPM request")
            #Wait 66 seconds before making the next request
            time.sleep(wait_time*60)
            print("\n\t\t\t\t- System is done waiting")
    #Check if the last pages are summarized or not
    if last_page < len(documents):
        summary = summary + chain.run(documents[last_page:len(documents)])
    
    return summary


"""
This function accepts summary as string input and converts it into a
PDF file. And stores the PDF file in "Summarized_Files" directory.
"""
def pdf_generation(final_summary, file):
    #Load the FPDF library
    from fpdf import FPDF
    import random

    #Instantiate the FPDF class
    pdf = FPDF(orientation='P', #Portrait
           unit= 'in', # Inches
           format='A4' #A4 Page
           )
    
    #Add the font files for Times New Roman
    pdf.add_font(family="Times", style="", fname="fonts/times new roman.ttf", uni=True)
    pdf.add_font(family="Times", style="B", fname="fonts/times new roman bold.ttf", uni=True)
    pdf.add_font(family="Times", style="I", fname="fonts/times new roman italic.ttf", uni=True)
    pdf.add_font(family="Times", style="BI", fname="fonts/times new roman bold italic.ttf", uni=True)
    
    #Set margins to 1 inches
    pdf.set_margins(left= 1, top=1, right=1)
    
    #Add the title and author name
    pdf.set_title(title=f"Summary of {file.filename}")
    pdf.set_author(author="Umair")
    
    #Add a page
    pdf.add_page()

    #Set the style to Bold & Italic, and szie to 20 for the first page
    pdf.set_font(family="Times",
                 style='BI', # Bold and italics
                 size=20
                 )
    
    #Add the tex "Summary of the Book Crime & Punishments" on the first page
    pdf.cell(w=6.25, h=1, txt = "Summary", ln = 1, align = 'C')
    pdf.cell(w=6.25, h=1, txt = "of", ln = 1, align = 'C')
    pdf.cell(w=6.25, h=1, txt = f"{file.filename}", ln = 1, align = 'C')
    
    #Add a new page
    pdf.add_page()

    #Set the style to noraml and font size to 12
    pdf.set_font(family="Times",
                 style='',  # 'I' --> italics, 'U' --> underlined, '' --> regular font
                 size=12
                 )
    
    line = ""
    next_line = random.randrange(start=50, stop=200)
    para_length = 0
    period_words = ["Mrs.", "Mr.", "Ms.", "Dr.", "Prof.", "Capt.", "Gen.", "Sen.", "Rev.", "Hon.", "St."\
                   "Jr.","Sr.", "i.e.","e.g.","etc.","a.m.", "p.m.",]
    for count, word in enumerate(final_summary.split(" ")):
        para_length = para_length + 1
        if para_length > next_line:
            if (word.endswith(".")) and (word not in period_words) and (len(word) > 2):
                #insert the line in pdf
                pdf.cell(w=6.25, h=0.285, txt = line + " "+ word, ln = 1, align = '')
                #insert a line-break
                pdf.cell(w=0, h=0.285, txt = "", ln = 1, align = '')
                line = ""
                next_line = random.randrange(start=50, stop=200)
                para_length = 0
                continue
        if len(line) + len(word) <= 87:
            line = line + " " + word
        else:
            #insert the line in pdf
            pdf.cell(w=6.25, h=0.285, txt = line, ln = 1, align = '')
            line = word
    
    #Write the last line
    pdf.cell(w=6.25, h=0.285, txt = line, ln = 1, align = '')
    
    # save the pdf with name .pdf
    pdf.output("Summarized_Files/summary.pdf")


#Define the landing page
@app.get("/")
async def home():
    return {"Message": "Welcome Intelligent Book Summarization App"}

#Define the summarization endpoint
@app.post("/summarize")
async def summary(file: UploadFile = File(...)):

    #Save the uploaded file locally in the "Uploaded_Files" directory
    # If the storage is successful, then proceed
    # otherwise clode the execution and return an error message.
    try:
        with open("Uploaded_Files/"+file.filename, 'wb') as f:
            shutil.copyfileobj(file.file, f)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    #Use the extract_api() method to read and store the API key
    # as environment variable
    extract_api_ftn_return_value = extract_api()
    if extract_api_ftn_return_value == 0:
        return {"message": "There is some error with your API key. Please check your API_file."}
    
    #Summarize the text
    summary = summarization_ftn(file)

    #Convert the Summarized text from string to a PDF file
    pdf_generation(summary, file)
     
    path = "Uploaded_Files/" + file.filename
    return FileResponse(path)

#Define the main function
if __name__ == "__main__":
    uvicorn.run(app="summarization_app:app",
                host = "127.0.0.1",
                port = 8000,
                reload=True)