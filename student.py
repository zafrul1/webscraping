from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from io import BytesIO
from datetime import datetime
import json
import urllib.parse
import requests
import os 
import pandas as pd
import numpy as np
import tabula

class Student : 

    subjects = ""

    def __init__(self,uni, course , name="MaxMusterman", age=18, batch=1) :
        self.name = name
        self.age = age
        self.batch = batch
        self.uni = uni
        self.course = course
        self.search_term = f"{uni}/\"{course}\"Pruefungsordnung"
        self.get_info(self.search_term)
  
    def getStudent(self):
        print(f"{self.name} {self.age} {self.batch}")
        
    def get_info(self,search_term):

      soup = self.search_google(search_term)
      summary = []

      for container in soup.findAll('div', class_='tF2Cxc'):
         pdf_link = container.find('a')['href']
         if self.check_pdf(pdf_link):
          summary.append(pdf_link)
         
      self.downl_latest_pdf(summary)
      self.print_link(summary)

    def get_creation_date(self,url):
      string = str(url)
      response = requests.head(string)
      creation_date = response.headers.get("creation-date", None)
      if creation_date is None:
         creation_date = response.headers.get("last-modified", None)

      if creation_date is not None:
         creation_date = datetime.strptime(creation_date, "%a, %d %b %Y %H:%M:%S %Z")

      return creation_date

    def get_latest_updated_pdf(self,summary = []):

        latest_creation_date = None
        for url in summary:
         creation_date = self.get_creation_date(url)
         if latest_creation_date is None or creation_date > latest_creation_date:
             latest_creation_date = creation_date
        return latest_creation_date

    def get_pdfname(self, pdf_link):
        string = str(pdf_link) #convert to string
        #case1 - get name from url that ends with .pdf
        if string.endswith(".pdf"):
            pdfname = pdf_link.split("/")[-1]
            return pdfname
        #case2 - get name from auto download url
        elif self.auto_downl(pdf_link) :  
            pdfname = self.parsed_url(pdf_link)
            return pdfname
        return 0    

    def check_pdf (self,pdf_link):
        string = str(pdf_link)
        if string.endswith(".pdf") or self.auto_downl(pdf_link):
         return 1

    def auto_downl(self,pdf_link): # check if url auto download pdf 
        if self.parsed_url(pdf_link) : 
            string = self.parsed_url(pdf_link)
            self.subjects = string
            if string.endswith(".pdf") : 
                return 1
        return 0 

    def parsed_url(self,pdf_link):
        parsed_link = urllib.parse.urlparse(pdf_link)
        query = urllib.parse.parse_qs(parsed_link.query)
        if "download" in query:
            pdfname = query["download"][0]
            return pdfname
        return 0

    def print_link(self,summary):
        print(json.dumps(summary, indent=2, ensure_ascii=False))

    def print_pdf(self,pdf_link):
        # Open the PDF file
        pdf_file = open(self.get_pdfname(pdf_link), 'rb')

        # Create a PDF reader object
        pdf_reader = PdfReader(pdf_file)

        # Get the number of pages in the PDF file 
        num_pages = len(pdf_reader.pages)
        subject = ""
        # Extract the text from each page
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            if "Orientierungsphase" in text :
              subject_index = text.index("Orientierungsphase") + len("Orientierungsphase")
              subject = text[subject_index:]
            #print("This is page" , page_num)
            print(subject)

        #Close the PDF file
        pdf_file.close()

    def downl_pdf(self,pdf_link):

        pdfname = self.get_pdfname(pdf_link)
        pdf_response = requests.get(pdf_link)
        with open(pdfname, "wb") as f:
            f.write(pdf_response.content)
            print(f"Successfully downloaded {pdfname}.pdf")

    def search_google(self,search_term):
        # Use the search term to query Google
        
        query = search_term.replace(" ", "+")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
        url = f"https://www.google.com/search?q={query}"

        # Send a GET request to the URL and parse the response
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def downl_latest_pdf(self,summary = []):
     latest_date = self.get_latest_updated_pdf(summary)
     for pdf_link in summary:
         creation_date = self.get_creation_date(pdf_link)
         if creation_date == latest_date:
              self.downl_pdf(pdf_link)
              self.print_table(self.get_pdfname(pdf_link))
              #self.print_pdf(pdf_link)
              #self.delete_pdf(pdf_link)

    def delete_pdf(self,pdf_link):
        file_path = self.get_pdfname(pdf_link)
        # Check if the file exists
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
            print(f"{file_path} has been deleted.")
        else:
            print(f"{file_path} does not exist.")
    
    def print_table(self,pdf_name):
        df_list = tabula.io.read_pdf(pdf_name, pages="all",encoding="UTF-8") #encoding UTF-8 for Linux, cp1252 for windows
        df = df_list[0]
        is_nan = df.isna()
        row, col = np.where(is_nan)
        row = row[0]
        col = col[0]
        df.at[row, col] = 0
        print(df)
        

   
   




