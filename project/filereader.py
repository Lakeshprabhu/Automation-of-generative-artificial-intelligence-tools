import json
import time




from xcel import Xcel

from openai import Chatgpt
from gemini import Gemini
from deepseek import Deepseek
import pymupdf
import pymupdf4llm

import sys
import os

def get_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class PDF():
    def __init__(self,file_loc,model_num,user,gem_key):
        self.out = open(get_path("output.txt"), "wb")
        self.key= user
        self.google = Gemini(gem_key)
        self.file_loc=f"{file_loc}"


        self.doc = pymupdf.open(file_loc)
        self.llama_conv = pymupdf4llm.LlamaMarkdownReader()
        self.ai_doc = self.llama_conv.load_data(file_loc)

        self.model_name = str(model_num)



        self.num_of_pages = self.get_page_count()
        self.excel_loc = None
        self.answers = ""
        f = open(get_path("Instruction Set/simple_extract.txt"), "r")

        f_read = f.read()
        self.simple_prompt = f_read
        f.close()
        F = open(get_path("Instruction Set/complex_extract.txt"), "r",encoding="utf-8")
        F_read = F.read()
        self.complex_prompt = F_read
        F.close()



    def start_(self):
        pages = self.num_of_pages
        if pages  <= 10 :
            abc =  self.extract_questions_up(False)
            script = Xcel(abc,f"{self.file_loc}.xlsx")

            self.excel_loc = f"{self.file_loc}.xlsx"



        elif pages  > 10:
            self.extract_complex()
            self.excel_loc = f"final.xlsx"



        return self.excel_loc






    def get_answers(self,file):
        if self.model_name == "3":
            dps = Deepseek(self.simple_prompt,file,self.key)

            answers = dps.get_response()
            answers = self.fix_json(answers)
        if self.model_name == "2":
            self.google.gen(self.simple_prompt,file)
            Gemini.metrics.print_summary()
            answers = self.google.get_response()
        elif self.model_name == "1":
            CHAT = Chatgpt(self.simple_prompt, "B", file,self.key)
            Chatgpt.metrics.print_summary()
            answers = CHAT.get_response()
            answers = self.fix_json(answers)
        answers = (answers.replace("```", "")).strip()
        answers = (answers.replace("json", "")).strip()
        print(answers)
        with open(get_path("abc.txt"), "w", encoding="utf-8") as file:

            file.write(answers)
        json_ob = json.loads(answers)
        return json_ob



    def get_complex_answer(self,file):

        if self.model_name =="3":
            dps = Deepseek(self.complex_prompt,file,self.key)
            answers=dps.get_response()

        if self.model_name == "2":
            self.google.gen(self.complex_prompt,user_content=file)
            answers = self.google.get_response()
            Gemini.metrics.print_summary()
        elif self.model_name == "1":
            CHAT = Chatgpt(self.complex_prompt,"B",file,self.key)
            Chatgpt.metrics.print_summary()
            answers = CHAT.get_response()
        answers = self.fix_json(answers)
        answers = (answers.replace("```", "")).strip()
        answers = (answers.replace("json", "")).strip()
        print(answers)
        return str(answers)


    def get_page_count(self):
        page_count = 0
        for page in self.doc:
            page_count+=1
        return page_count

    def extract_complex(self):
        QandA = []
        text_files = []
        count=1
        i = 1
        text_part = 1
        self.complex_text = open(get_path(f"complex_extract/text_part{text_part}.txt"), "wb")

        text_files.append(f"complex_extract/text_part{text_part}.txt")
        for page in self.doc:
            print(f"{count}")
            all_text = page.get_text().encode("utf-8")
            self.complex_text.write(all_text)
            str_page = f"\n\npage_number:-{count}\n\n"
            page_count_bytes = str_page.encode("utf-8")
            self.complex_text.write(page_count_bytes)
            self.complex_text.write(bytes((12,)))
            check  = i % 10
            if check == 0:
                text_part+=1
                self.complex_text.close()
                self.complex_text = open(f"complex_extract/text_part{text_part}.txt", "wb")
                text_files.append(f"complex_extract/text_part{text_part}.txt")
            i+=1
            count+=1

        self.complex_text.close()
        i=0
        answers_fin = ""
        for text in text_files:
            print(text)
            sending_file_og = open(get_path(text), "r", encoding="utf-8")

            sending_file = sending_file_og.read()
            answers = self.get_complex_answer(sending_file)
            answers = (answers.replace("```", "")).strip()
            answers = (answers.replace("json", "")).strip()
            self.answers = json.loads(answers)
            script = Xcel(self.answers, f"excel/part{i}.xlsx")
            i+=1
            sending_file_og.close()
            time.sleep(3)
        script.combine_excel_files()



    def extract_to_file_text(self):
        page_count = 1
        for page in self.doc:
            text = page.get_text().encode("utf-8")
            self.out.write(text)
            str_page = f"\n\npage_number:-{page_count}\n\n"
            page_count_bytes = str_page.encode("utf-8")
            self.out.write(page_count_bytes)
            self.out.write(bytes((12,)))
            page_count += 1
        print("done")
        self.out.close()


    def extract_questions_up(self,complexity):
        if complexity == False:
            file = open(get_path("output.txt"), "r", encoding="utf-8")
            file_1 = file.read()
            file.close()
        else:
            file_1 = complexity
        if self.model_name == "2":
            self.google.gen(f"Please identify and extract all questions from the following text, regardless of whether they are explicitly marked or numbered. The questions are the ones the student must write answers to . Dont add any introductory remarks ",file_1)
            extracted_questions = self.google.get_response()
            Gemini.metrics.print_summary()
        else:
            Extracted_questions_set = None
            if self.model_name == "1":
                Extracted_questions_set = Chatgpt(
                    f"Please identify and extract all questions from the following text, regardless of whether they are explicitly marked or numbered. The questions are the ones the student must write answers to ",
                    "B", file_1,self.key)
                Chatgpt.metrics.print_summary()
            elif self.model_name == "3":
                Extracted_questions_set = Deepseek("Please identify and extract all questions from the following text, regardless of whether they are explicitly marked or numbered. The questions are the ones the student must write answers to",
                        file_1,self.key)


            extracted_questions = Extracted_questions_set.get_response()




        with open(get_path("output_2.txt"), "w", encoding="utf-8") as file:

            file.write(str(extracted_questions))
        return self.get_answers(file_1)


    def fix_json(self,text):
        original = self.model_name
        self.model_name = "2"
        if self.model_name == "1":
            filtered_pdf_text = Chatgpt(f"Please remove the opening introductory information from the text , till the paper actually starts , and print everything afterwards","B",text,self.key)
            Chatgpt.metrics.print_summary()
            self.model_name = original
            return filtered_pdf_text.get_response()
        elif self.model_name =="2":
            self.google.gen("The following JSON data may contain errors such as incorrect syntax, improper formatting, duplicate entries, or structural issues. Please correct any errors and return the fixed JSON in a valid and properly formatted JSON structure, ensuring it is correctly structured and follows standard JSON rules. Do not modify the content unless necessary to fix errors. Return only the corrected JSON output. Every dictionary should be IN A SINGLE LIST ",
                                            user_content=text)
            Gemini.metrics.print_summary()
            self.model_name = original
            return self.google.get_response()


