from fuzzywuzzy import fuzz
import re
import os
import pandas as pd


def find_pattern_in_file(line, pattern, similarity_threshold=50):
        
        similarity = fuzz.ratio(line, pattern)
        if similarity >= similarity_threshold:
            return True
        return False


def collect_related_articles(filepath, pattern):

    subsets = []
    subset = []

    with open(filepath, 'r',encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:

        if not find_pattern_in_file(line,pattern):
            subset.append(line)

        else:
            subsets.append(''.join(subset).strip())
            subset = [line]

    if subset:
        subsets.append(''.join(subset).strip())
    
    return subsets


def break_articles_to_rules(article, pattern):
    rules = []
    rule = []
    for line in article.split('\n'):
        #print(line)
        if not find_pattern_in_file(line, pattern, 60):
            rule.append(line)
        else:
           # print(line)
            rule.append(line)
            rules.append(' '.join(rule).strip())
            rule = []
        
    if rule:
        rules.append(' '.join(rule).strip())
    
    return rules

def get_topic(text):
    title = None
    for line in text.split('\n'):

        if 'TITLE' in line:
            title = re.search('—(.*)CHAPTER', line)

        if title:
            title = title.group(1).strip()
    
    return title



def get_agency(text):
    agency = None
    for line in text.split('\n'):

        if 'CHAPTER' in line:
            agency = re.search('CHAPTER(.*)—',line)
        
        if agency:
            return agency.group(1).strip()
    return None


def extract_date(text):
    # Define the date pattern
    
    for line in text.split('\n'):
    # Search for the date pattern in the text
        date_match = re.search('Filed,(.*)', line)
    
        if date_match:
            return date_match.group(1).strip()
        else:
            date_match = re.search('Approved,(.*)', line)

            if date_match:
                return date_match.group(1).strip()
            else:
                date_match = re.search('Piled,(.*)', line)
                if date_match:
                    return date_match.group(1).strip()
    return None


def extract_document_no(text):

    for line in text.split('\n'):

        date_match = re.search('R.  Doc.(.*);', line)

        if date_match:
            return date_match.group(1).strip()
    return None

def list_files_in_directory(path):
    try:
        # List all files and directories in the given path
        with os.scandir(path) as entries:
            files = [entry.name for entry in entries if entry.is_file()]
        return files
    except FileNotFoundError:
        return f"The directory {path} does not exist."
    except PermissionError:
        return f"Permission denied to access {path}."
    except Exception as e:
        return f"An error occurred: {e}"


     



if __name__ == "__main__":

    file_path = 'c://Users//lakha//Desktop//Machine Learning//Innovate Files//'
    article_pattern = 'TITLE  7— AGRICULTURE'
    rules_pattern = '[F.  R.  Doc.  40-7;  Filed,  December  29,  1939;'

    files = list_files_in_directory(file_path)
    data = []

    if files:
        i = 0
        for file in files:
            i+=1
            if i == 100:
                break
            articles = collect_related_articles(os.path.join(file_path,file),article_pattern)

            if articles: 
                for article in articles:
                    rules = break_articles_to_rules(article, rules_pattern)

                    if rules:
                        title = get_topic(rules[0])
                        agency = get_agency(rules[0])

                        for rule in rules:
                            date = extract_date(rule)
                            document = extract_document_no(rule)
                            data.append({
                                "topic" : title,
                                "agency": agency,
                                "date" : date,
                                "rule" : rule,
                                "document" : document
                            })
    
    df = pd.DataFrame(data)
    df.to_csv('c://Users//lakha//Desktop//Machine Learning//Innovate Files//extracted_rules.csv', index=False)
    print("Data has been written to extracted_rules.csv")
                        


