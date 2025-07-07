import re

def extract_section(text, section_name):
        pattern = rf"\*\*{section_name}\*\*\s*((?:.|\n)*?)(?=\n\*\*|\Z)"
        match = re.search(pattern, text, re.IGNORECASE)
        if section_name== "Projects":
            pattern = r"\*\*Projects\*\*\s*((?:.|\n)*?)(?=\n\*\*(Experience|Education|Skills|Certifications|Achievements|Summary|Profile|Work Experience)\*\*|\Z)"
            match = re.search(pattern, text, re.IGNORECASE)
            return match.group(1).strip() if match else ""
             
        return match.group(1).strip() if match else ""


def extract_pii_from_markdown(text):

    lines = text.strip().splitlines()

    candidate_name = lines[0].strip()
    contact_line = lines[1]

    matches = re.findall(r'\[(.*?)\]\((.*?)\)', contact_line)

    email = matches[0][0] if len(matches) > 0 else ''
    phone = matches[1][0].replace('+91 ', '').strip() if len(matches) > 1 else ''
    linkedin = matches[2][0].strip().replace('https://', '').replace('www.', '') if len(matches) > 2 else ''

    return {
        "candidate_name": candidate_name,
        "email_id": email,
        "phone_number": phone,
        "linkedin_id": linkedin
    }