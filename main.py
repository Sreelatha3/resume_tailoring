import pymupdf4llm
import os
import re
from src import modify_sections
from src.extractor import extract_section,extract_pii_from_markdown
from dotenv import load_dotenv
from google import genai




#step1 extracting the data from the resume.pdf using pymupdf lib in the markdown format
old_resume_txt = pymupdf4llm.to_markdown(r"D:\Dev\resume_tailor\input\resume.pdf")

#step 2: reading the job description into a string before passing it to api,cause gemini cant read local files
with open(r"D:\Dev\resume_tailor\input\jd.txt", "r", encoding="utf-8") as f:
    jd_txt = f.read()


prompt = f"""
            You are a resume optimization expert.
            Given the job description (may include more than one section) and my resume, generate a resume that gives an ATS score > 95% for the job description.

            Strict rules:
            - Analyse the given jd very well to generate the resume well
            - Don't fabricate experience
            - highlight what’s in the resume but can modify the skills that are similar
            - add few of the skills that are not present to enhance the ats score  when a skill is described as a must or required or Mandatory
            - Use keywords and phrases from the job description where they apply.
            - Structure it cleanly in plain text (not PDF or LaTeX).
            - Output only the tailored resume in plain text format and main the same section order and only sections that are in the resume
            - follow ats friendly rules like quantify
            - the no of characters should be less than or equal to 3,258 
            - can remove irrevelant data from the exisisting resume
        

            Job Description:{jd_txt}
            My Resume:{old_resume_txt}
        """

load_dotenv() 

api_key = os.getenv("GEMINI_API_KEY")

#step 3: create a client using the secret api key to consume the api
client = genai.Client(api_key=api_key) 

#step 4: call generate_content using the client instance and passing the prompt comprising the resume and jd txt
response = client.models.generate_content(model="gemini-2.0-flash",contents=[prompt])

#step 5: converting the resume into the text
final_resume = response.text
# print(final_resume)

#step 6: writing the text to the file in \output folder
with open(r"D:\Dev\resume_tailor\output\new_resume.txt", "w", encoding="utf-8") as f:
    f.write(final_resume)


#step 7: read the latex resume template
with open(r"D:\Dev\resume_tailor\templates\resume_template.tex","r") as f:
    latex_template=f.read()

for section in ["Skills", "Projects", "Experience", "Education"]:
    latex_template = modify_sections.clear_section(latex_template, section)

with open(r"D:\Dev\resume_tailor\output\resume.tex", "w") as f:
    f.write(latex_template)

#step 8: read the new resume_output
resume_text = open(r"D:\Dev\resume_tailor\output\new_resume.txt").read()

#step 9: extract the pii info from the resume
header_info = extract_pii_from_markdown(resume_text)

#step 10: parse the sections data from the new resume
parsed_data = {
    "skills_content": extract_section(resume_text, "Skills"),
    "experience_content": extract_section(resume_text, "Experience"),
    "education_content":extract_section(resume_text, "Education"),
    "projects": extract_section(resume_text, "Projects")
}

#step 10: format the sections of new resume using the functions
skills_latex = modify_sections.format_skills_latex(parsed_data["skills_content"])
experience_latex = modify_sections.format_experience_latex(parsed_data["experience_content"])
education_latex = modify_sections.format_education_latex(parsed_data["education_content"])
projects_latex = modify_sections.format_projects_latex(parsed_data["projects"])


#step 11: replace the contents of each section in the latex resume template with the formatted data
latex_template = latex_template.replace("{{candidate_name}}", header_info["candidate_name"])
latex_template = latex_template.replace("{{email_id}}", header_info["email_id"])
latex_template = latex_template.replace("{{phone_number}}", header_info["phone_number"])
latex_template = latex_template.replace("{{linkedin_id}}", header_info["linkedin_id"])
latex_template = latex_template.replace("{{Skills}}", skills_latex)
latex_template = latex_template.replace("{{Experience}}", experience_latex)
latex_template = latex_template.replace("{{Education}}", education_latex)
latex_template = latex_template.replace("{{Projects}}", projects_latex)


#step 12: 
with open(r"D:\Dev\resume_tailor\output\resume.tex", "w") as f:
    f.write(latex_template)

