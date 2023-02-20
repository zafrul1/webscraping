import requests, webbrowser, sys, bs4
from PyPDF2 import PdfReader


class Uni : 

    def __init__(self, name, course, subject) :
        self.name = name
        self.course = course
        self.subject = subject 

    def getUni (self) : 
        return f"{self.name} {self.course} {self.subject} "

    def listSubject(self, university_name, course_name):
         
        url = requests.get(f"https://www.google.com/search?q={university_name}/{course_name}/pdf") 
        

        # # Download the PDF file from a URL
        # url = 'https://www.hs-augsburg.de/Binaries/Binary16581/SPO-TI-BAC-WS-2010.pdf'
        # response = requests.get(url)

        # with open('SPO-TI-BAC-WS-2010.pdf', 'wb') as f:
        # f.write(response.content)

        # # Open the PDF file
        # pdf_file = open('SPO-TI-BAC-WS-2010.pdf', 'rb')
        # pdf_reader = PdfReader(pdf_file)

        # # Get the number of pages in the PDF file 
        # num_pages = len(pdf_reader.pages)

        # # Extract the text from each page
        # for page_num in range(num_pages):
        #  page = pdf_reader.pages[page_num]
        # text = page.extract_text()
        # print("This is page" , page_num)
        # print(text)

        # #    Close the PDF file
        # pdf_file.close()


        # import requests
        # from bs4 import BeautifulSoup
        # university_name = input("Enter the name of the university: ")
        # course_name = input("Enter the name of the course of study: ")
        # url = f"https://www.{university_name}.edu/courses/{course_name}"
        # response = requests.get(url)
        # soup = BeautifulSoup(response.content, "html.parser")
        # subjects = soup.find_all("li", class_="subject")
        # for subject in subjects:
        #     print(subject.text)