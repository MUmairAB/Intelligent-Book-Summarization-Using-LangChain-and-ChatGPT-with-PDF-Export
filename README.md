# Intelligent Book Summarization Using LangChain and ChatGPT with PDF Export

## Table of Contents

- [Introduction](introduction)
  - [LangChain Framework](langChain-framework)
  - [ChatGPT as Language Model](ChatGPT-as-language-model)
  - [Summarization Process](summarization-process)
  - [PDF Export Using FPDF](PDF-export-using-FPDF)
  - [Contributions and Workaround for API Limits](contributions-and-workaround-for-API-limits)
  - [PDF Generation](PDF-generation)
- [FastAPI](fastapi)
- [Features](features)
- [Getting Started](getting-started)
  - [Prerequisites](prerequisites)
  - [Installation](installation)
- [Usage](usage)
- [Contributing](contributing)


---

## Introduction <a name="introduction"></a>

In today's fast-paced world, the ability to distill large volumes of information into concise summaries is a valuable skill. This project aims to leverage cutting-edge technologies to create an intelligent book summarization system that combines the power of the **LangChain** framework, **ChatGPT** as a Language Model, and the **FPDF** Python library to produce well-structured PDF summaries of books.

### LangChain Framework <a name="langChain-framework"></a>

The LangChain framework serves as the foundation of our project. LangChain is a versatile and flexible tool that provides a structured approach to processing and analyzing natural language text. It allows us to extract key insights, identify important themes, and break down complex sentences, making it an ideal choice for our summarization task.

### ChatGPT as Language Model <a name="ChatGPT-as-language-model"></a>

ChatGPT, an advanced Language Model, plays a central role in this project. It harnesses the power of deep learning and natural language processing to understand and generate human-like text. We employ ChatGPT to process the content of the book, ensuring that our summaries are not only concise but also coherent and contextually accurate.

### Summarization Process <a name="summarization-process"></a>

Our project follows a systematic summarization process. We first load the PDF book using **PyPDFLoader** API from LangChain, which uses the **PyPDF** library. Then comes the pre-process of text to remove noise and identify relevant content. Next, the text is subjected to ChatGPT, which generates a summary based on this refined input, ensuring that it captures the most salient points and key takeaways from the book. The combination of LangChain and ChatGPT ensures that our summaries are both accurate and comprehensive.

### PDF Export Using FPDF <a name="PDF-export-using-FPDF"></a>

To make our summaries easily accessible and shareable, we utilize the FPDF Python library to convert the generated summaries into PDF documents. FPDF allows us to format the content, add headers and footers, include images or graphs (although we did not add any), and create a professional-looking document that retains the essence of the book. The PDF export feature ensures that our summaries can be seamlessly integrated into various platforms, such as e-readers or websites. A noteworthy highlight is the addition of external encoding within the FPDF to accommodate special characters.

### Contributions and Workaround for API Limits <a name="contributions-and-workaround-for-API-limits"></a>

The OpenAI limits the API usage to certain constraints like limiting the number of tokens and API call in 1 minute. A workaround is also provided to address these constraints. We break down API calls into segments, typically corresponding to individual pages, and subsequently merge the individual summaries to create a comprehensive summary. This approach ensures compliance with OpenAI's rate limits while efficiently summarizing lengthy texts like books.

### PDF Generation <a name="PDF-generation"></a>

The last step is to convert the generated summary from a string to a clean PDF document using the FPDF library. Special attention is given to handling special characters to prevent errors during the conversion process. Font files for the standard **Time New Roman** font are included in the project for this purpose.

## FastAPI

To implement this project in a production environment within an application or as a standalone application, we have developed a REST-based FastAPI as well. It can be accessed [here](https://github.com/MUmairAB/Intelligent-Book-Summarization-Using-LangChain-and-ChatGPT-with-PDF-Export/blob/main/FastAPI/summarization_app.py).

## Getting Started <a name="getting-started"></a>

### Prerequisites <a name="prerequisites"></a>

Before using this tool, ensure you have the following prerequisites installed:

- Python 3.7+
- Pip (Python package manager)
- Git
- ChatGPT API Keys

### Installation <a name="installation"></a>

1. Clone the repository to your local machine using Git:

   ```
   git clone https://github.com/MUmairAB/Intelligent-Book-Summarization-Using-LangChain-and-ChatGPT-with-PDF-Export.git
   ```
   
Navigate to the project directory:

  ```
  cd Intelligent-Book-Summarization-Using-LangChain-and-ChatGPT-with-PDF-Export
  ```

Install the required Python dependencies:

  ```
  pip install -r requirements.txt
  ```

## Usage <a name="usage"></a>

To use this tool, follow these simple steps:

Put your own API keys in [API_file.py](https://github.com/MUmairAB/Intelligent-Book-Summarization-Using-LangChain-and-ChatGPT-with-PDF-Export/blob/main/API_file.py) file.

Place the book you want to summarize in the input directory. Change the **file_path** parameter.

Run the following command to generate a summary:

  ```
  jupyter nbconvert --to script App.ipynb # Convert the .ipynb file to .py file 
  python App.py
  ```

Your book summary will be generated and saved as **summary.pdf** file.

#### **Enjoy reading your concise book summary!**

## Contributing <a name="contributing"></a>

Contributions to this project are welcome! If you have ideas for improvements, new features, or bug fixes, please open an issue or submit a pull request. For major changes, please discuss your ideas in an issue before proceeding.

**Thank you for using the Intelligent Book Summarization tool. We hope it simplifies your reading experience and saves you time. If you have any questions, issues, or feedback, please don't hesitate to reach out. Happy reading!**
