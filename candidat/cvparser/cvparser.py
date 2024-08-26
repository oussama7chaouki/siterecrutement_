from PyPDF2 import PdfReader
import re
import csv
import os

def cvparser(file_path):
    formation_data = {
        'user_id': None,  # Assuming this field represents the user ID
        'formation': '',
        'school': '',
        'startyear': None,
        'endyear': None
    }

    experience_data = {
        'user_id': None,  # Assuming this field represents the user ID
        'experience': '',
        'company': '',
        'startyear': None,
        'endyear': None
    }
    skills = {
        'user_id': None,
        'skill' :''
    }
    languages = {
        'user_id': None,
        'language' :''
    }
    array_experience=[]
    array_formation=[]
    # Manually specify the file path (cv)

    # Parse PDF file using PyPDF2
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text()
    # File path
    file_path = 'data\etude.csv'

    ypattern = r'((Janv(ier)?|F(e|é)vr(ier)?|Mars|Avr(il)?|Mai|Juin|juill(et)?|Ao(u|û)t|Sept(embre)?|Oct(obre)?|Nov(embre)?|D(e|é)c(embre)?)\s*)?(19|20)\d{2}[^\d]{0,8}\s*((Janv(ier)?|F(e|é)vr(ier)?|Mars|Avr(il)?|Mai|Juin|juill(et)?|Ao(u|û)t|Sept(embre)?|Oct(obre)?|Nov(embre)?|D(e|é)c(embre)?)\s*)?(19|20)\d{2}'
    # $lycee
    lycee_pattern = r'l\s*y\s*c\s*(é|e)\s*e\s*\b[A-Z]+[a-z]*\b\s*(\b[A-Z]+[a-z]*\b)*'

    # $school
    school_pattern = r'f\s*a\s*c\s*u\s*l\s*t\s*(é|e)\s*(d\s*e|d\s*\')\s*(\s*\w*\s*){5}|(e\s*c\s*o\s*l\s*e\s*(\s*\w*\s*){5})|(i\s*n\s*s\s*t\s*u\s*t\s*e\s*(\s*\w*\s*){5})|(U\s*N\s*I\s*V\s*E\s*R\s*S\s*I\s*T\s*É\s*(\s*\w*\s*\W){5})'

    # $faculte
    faculte_pattern = r'f\s*a\s*c\s*u\s*l\s*t\s*(é|e)\s*(d\s*e|d\s*\')\s*(\s*\w*\s*){5}'


    month=r'Janv(ier)?|F(e|é)vr(ier)?|Mars|Avr(il)?|Mai|Juin|juill(et)?|Ao(u|û)t|Sept(embre)?|Oct(obre)?|Nov(embre)?|D(e|é)c(embre)?'
    # Initialize an empty list to store the rows

    months_regex = [
        r'J\s*a\s*n\s*v\s*(i\s*e\s*r)?',
        r'F\s*(e|é)\s*v\s*r\s*(i\s*e\s*r)?',
        r'M\s*a\s*r\s*s',
        r'A\s*v\s*r\s*(i\s*l)?',
        r'M\s*a\s*i',
        r'J\s*u\s*i\s*n',
        r'j\s*u\s*i\s*l\s*l\s*(e\s*t)?',
        r'A\s*o\s*(u|û)\s*t',
        r'S\s*e\s*p\s*t\s*(e\s*m\s*b\s*r\s*e)?',
        r'O\s*c\s*t\s*(o\s*b\s*r\s*e)?',
        r'N\s*o\s*v\s*(e\s*m\s*b\s*r\s*e)?',
        r'D\s*(e|é)\s*c\s*(e\s*m\s*b\s*r\s*e)?'
    ]

    months_values = [
        "01", "02", "03", "04", "05", "06",
        "07", "08", "09", "10", "11", "12"
    ]
    company_pattern = r'(S\s*O\s*C\s*I\s*(E|É)\s*T\s*(E|é)|s\s*o\s*c\s*i\s*(e|é)\s*t\s*(e|é)|S\s*o\s*c\s*i\s*(e|é)\s*t\s*(e|é)|G\s*r\s*o\s*u\s*p\s*e)\s*(\b[A-Z][a-zA-Z]*\b)'

    data = []
    yearposition = []
    def csvlist(file):
        file_path = os.path.join(os.path.dirname(__file__), file)
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            rows = csvfile.readlines()
            roww = rows[0].strip().split(',')  # Extract and split the header row
        return roww
    etudes=csvlist("data/etude.csv")
    ecoles=csvlist("data/ecole.csv")
    jobs=csvlist('data/conjob.csv')
    skillspaternarray=csvlist('data/skill.csv')
    languagespaternarray=csvlist('data/language.csv')

    for etude in etudes :
            matches = list(re.finditer(etude, text_content, re.IGNORECASE))

    # Check if there are any matches
            if matches:
                match= matches[0]
                    # Access match and its offset
                    # print("etude:", match.group(0))
                    # print("Offset:", match.start())

                    # Define the length of the context to extract before and after the match
                context_length = 30  # Adjust this according to your needs

                    # Get the start and end indices for the extracted substring
                start_index = max(0, match.start() - context_length)
                end_index = min(len(text_content), match.end() + context_length)

                    # Extract the substring around the match using the calculated indices
                extracted_text = text_content[start_index:end_index]
                # print("Extracted text:", extracted_text)
                schollou = ""
                startyea = '2023'
                endyear = '2023'

                etude = etude.replace(r"\s*", "")
                etude = etude.replace(r"\s+", "")
                etude = etude.replace("(ô|o)", "o")
                etude = etude.replace("(é|e)", "e")

                    # Uncomment the line below if you want to print etude
                    # print(etude)

                parts = etude.split("|")
                etude = parts[0]
                # print("etudee  "+etude)
                if( etude=="Bac"):
                        school = list(re.finditer(lycee_pattern, extracted_text, re.IGNORECASE))
                        if school:
                            schollou=school[0].group(0)
                            #  print("school :", school[0].group(0))
                else:
                        school = list(re.finditer(school_pattern, extracted_text, re.IGNORECASE))
                        if school:
                            schollou=school[0].group(0)
                            #  print(" school:", school[0].group(0))
                        else:
                            for ecole in ecoles:
                                eco =  re.search(r'\b{}\b'.format(re.escape(ecole)), extracted_text, flags=re.IGNORECASE)
                                if eco:
                                    schollou=eco.group(0)
                                    # print(" school:",eco.group(0))
                                    break
                
                year = list(re.finditer(ypattern, extracted_text, re.IGNORECASE))  
                if year:
                    # remove the year already retrive from education in work
                    value= year[0].start() + start_index             
                    yearposition.append(value)
                    statyear=list(re.finditer(r"(\d\s*\d\s*\d\s*\d)", year[0].group(0), re.IGNORECASE))
                    startyea=statyear[0].group(0) 
                    endyear = statyear[1].group(0) if len(statyear) > 1 else 2023
                    
                    
                startyeaString=startyea+'-01-01'
                endyeaString=endyear+'-01-01'
                array_formation.append({
            'user_id': None,
            'formation': etude,
            'school': schollou,
            'startyear': startyeaString,
            'endyear': endyeaString
        })

    # print(yearposition)
    jobs=csvlist("data\conjob.csv")
    yearworks=list(re.finditer(ypattern, text_content, re.IGNORECASE))

    for i in range(len(yearworks)):
        if yearworks[i].start() in yearposition:
            continue

        statyearwork=list(re.finditer(r"(\d\s*\d\s*\d\s*\d)", yearworks[i].group(0), re.IGNORECASE))
        if(statyearwork):
            month_value_dict = {}
            month_value_dict[0]='01'
            month_value_dict[1]='01'
            startyearwork=statyearwork[0].group(0)
            #   print(startyearwork)
            monthworkregex=list(re.finditer(month, yearworks[i].group(0), re.IGNORECASE))
            if monthworkregex:
                for po in range(len(monthworkregex)):
                        for index, regex in enumerate(months_regex):
                            if re.match(regex, monthworkregex[po].group(0), re.IGNORECASE):
                                month_value_dict[po] = months_values[index]
                                break
            #   print(month_value_dict)
            endyearwork=2023
            if len(statyearwork) >= 1:
                endyearwork=statyearwork[1].group(0)
            workdatestart=startyearwork+'-'+month_value_dict[0]+'-01'
            workdateend=endyearwork+'-'+month_value_dict[1]+'-01'
            array_experience.append({
        'user_id': None,  
        'experience': '',
        'company': '',
        'startyear': workdatestart,
        'endyear': workdateend
    })

    micho=[]
    postjobwork=''

    com=''
    j=0
    for postjob in jobs:
        
        postjobworks=re.search(r'\b{}\b'.format(re.escape(postjob)), text_content, flags=re.IGNORECASE)
        if postjobworks:
                postjobwork =postjobworks.group(0)
                if(len(array_experience)>0):
                    array_experience[j]['experience']=postjobwork
                    if(len(array_experience)>j+1):
                        j=j+1
                    else:
                        break

                
    coms= list(re.finditer(company_pattern, text_content, re.IGNORECASE))
    for i in range(len(coms)):
        if(len(array_experience)>0):
            array_experience[j]['company']=coms[i].group(0)
            if(len(array_experience)>j+1):
                j=j+1
            else:
                break
        

        

    siko = []
    ligo = []
    array_skills=''
    array_languages=''

    for pattern in skillspaternarray:
        if re.search(r"\b" + re.escape(pattern) + r"\b", text_content, re.I):
            pattern = pattern.replace("\s*", "")
            siko.append(pattern)

    for pattern1 in languagespaternarray:
        if re.search(r"\b" + re.escape(pattern1) + r"\b", text_content, re.I):
            pattern1 = pattern1.replace("\s*", "")
            ligo.append(pattern1)

    sikosize = len(siko)
    if sikosize >= 1:
        array_skills = ",".join(siko)

    ligosize = len(ligo)
    if ligosize >= 1:
        array_languages = ",".join(ligo)
    skill=({'user_id': None,'skill':array_skills})
    lang=({'user_id': None,'language':array_languages})

    return array_formation,array_experience,skill,lang


         




                    
          
