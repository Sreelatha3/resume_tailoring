import re

def format_projects_latex(txt):
    latex=r""""""
    projects = re.split(r'\n(?=\*\*[^\n]+\*\*\n)', txt.strip())
    for project in projects:
        lines=[line.strip() for line in project.strip().split('\n') if line.strip()]
        latex=latex+r"""  
        \vspace{0.2 cm}
            \begin{twocolentry}{
                
            }
             \textbf{"""+lines[0].strip('*')+r"""} \end{twocolentry}
        \vspace{0.10 cm}
        \begin{onecolentry}
            \begin{highlights}
            """
        pattern = r"^\*\s*\**\s*Technologies"
        idx=1
        if re.match(pattern, lines[1], re.IGNORECASE):
            temp=lines[1].split(':')[1]
            temp=temp.strip('*')
            latex=latex+r"""\item \textbf{Technologies: }"""+temp
            idx=idx+1
        for i in range(idx,len(lines)):
            latex=latex+r"""
            \item """+lines[i].strip('*')
        latex=latex+r"""    
        \end{highlights}
          \end{onecolentry}
        """
    return latex

def format_skills_latex(txt):
    latex=r"""
            \begin{onecolentry}
                \begin{highlightsforbulletentries}"""
    bullet_points = [line.strip() for line in txt.strip().split('\n') if line.strip().startswith('*')]
    for line in bullet_points:
        bolded_text = re.findall(r'\*\*(.*?)\*\*', line)
        after_colon = line.split(':')[1].strip('*')
        latex =latex+r"""
                \item \textbf{"""+bolded_text[0]+r""" }"""+after_colon+r"""
                    """
    latex=latex+r"""
        \end{highlightsforbulletentries}
    \end{onecolentry}
    
    """
    return latex

def format_experience_latex(txt):
    latex=r""""""
    first_line = next(line for line in txt.strip().split('\n') if line.strip())
    pattern = r"\*\*(.*?)\*\*,\s*(.*?)\s+([A-Za-z]+\s+\d{4}\s+â€“\s+\w+)"
    match = re.search(pattern, txt)
    if match:
        title = match.group(1).strip()
        company = match.group(2).strip()
        duration = match.group(3).strip()
   
    latex=latex+r"""
    \begin{twocolentry}{"""+duration+"""}"""+r"""
        \textbf{""" + title+"""},"""+company+r"""\end{twocolentry} \vspace{0.10 cm}
        \begin{onecolentry}
            \begin{highlights}"""
    txt=txt.replace(first_line,'').strip()
    bullet_points = [line.strip() for line in txt.strip().split('\n') if line.strip().startswith('*')]

    for line in bullet_points:
        line=line.replace('*','').strip()
        line=line.replace('%',r'\%')
        latex=latex+r"""
        \item """+line
    latex=latex+r"""
    \end{highlights}
        \end{onecolentry}
        """
    return latex

def format_education_latex(txt):
    latex=r""""""
    latex=latex+r"""  
        \begin{twocolentry}{
        }
            \textbf{"""
    lines=[line.strip().replace('*','') for line in txt.strip().split('\n') if line.strip()]
    grad_details=lines[1].split(',')
    latex=latex+lines[0]+r"""}, \item """+grad_details[0]+r""", 
                \textbf{CGPA:} """+grad_details[1]+r"""
        \end{twocolentry}
        """
    return latex

def clear_section(template, section):
    return re.sub(
        rf"% START_{section}.*?% END_{section}",
        f"% START_{section}\n{{{{{section}}}}}\n% END_{section}",
        template,
        flags=re.DOTALL
    )