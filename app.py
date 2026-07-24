from flask import Flask, render_template, request
import os
import re
import pdfplumber
import docx

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

COMMON_SKILLS = [
    'python', 'java', 'javascript', 'html', 'css', 'sql', 'flask', 'django',
    'react', 'node.js', 'git', 'docker', 'mongodb', 'mysql', 'c++', 'c',
    'aws', 'figma', 'excel', 'pandas', 'machine learning', 'nlp'
]
CORE_SKILLS = ['python', 'javascript', 'html', 'css', 'sql', 'git', 'react', 'flask']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files['resume']

    if file.filename == '':
        return "No file selected", 400

    if not allowed_file(file.filename):
        return "Invalid file type. Please upload a PDF or DOCX.", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    file_extension = file.filename.rsplit('.', 1)[1].lower()

    if file_extension == 'pdf':
        extracted_text = extract_text_from_pdf(filepath)
    elif file_extension == 'docx':
        extracted_text = extract_text_from_docx(filepath)

    parsed_data = parse_resume(extracted_text)
    ats_score = calculate_ats_score(extracted_text, parsed_data)
    parsed_data['ats_score'] = ats_score
    parsed_data['score_label'] = get_score_label(ats_score)
    parsed_data['suggestions'] = generate_suggestions(extracted_text, parsed_data)

    return render_template('dashboard.html', data=parsed_data)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(filepath):
    text = ""
    doc = docx.Document(filepath)
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def parse_resume(text):
    skills = extract_skills(text)
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": skills,
        "missing_skills": get_missing_skills(skills),
    }
def calculate_ats_score(text, parsed_data):
    score = 0

    if parsed_data['name'] != "Not found":
        score += 10
    if parsed_data['email'] != "Not found":
        score += 15
    if parsed_data['phone'] != "Not found":
        score += 15

    skills_found = len(parsed_data['skills'])
    skills_points = min(skills_found * 2.5, 20)
    score += skills_points

    key_sections = ['experience', 'education', 'project', 'certification', 'summary', 'objective']
    text_lower = text.lower()
    sections_found = sum(1 for section in key_sections if section in text_lower)
    section_points = min(sections_found * 5, 20)
    score += section_points

    word_count = len(text.split())
    word_count_points = min((word_count / 200) * 20, 20)
    score += word_count_points
    return round(score)

def get_score_label(score):
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    else:
        return "Needs Work"

def generate_suggestions(text, parsed_data):
    suggestions = []
    text_lower = text.lower()

    if parsed_data['email'] == "Not found":
        suggestions.append("Add a clear email address so recruiters can reach you.")

    if parsed_data['phone'] == "Not found":
        suggestions.append("Add a phone number to your contact information.")

    if 'experience' not in text_lower and 'intern' not in text_lower:
        suggestions.append("Add a Work Experience or Internship section, even if brief.")

    if 'project' not in text_lower:
        suggestions.append("Add a Projects section to showcase hands-on work.")

    if 'certification' not in text_lower:
        suggestions.append("Consider adding a Certifications section, even for online courses.")

    if 'summary' not in text_lower and 'objective' not in text_lower:
        suggestions.append("Add a short Summary or Objective at the top to introduce yourself.")

    has_numbers = bool(re.search(r'\d+%|\d+\+|increased|reduced|improved', text_lower))
    if not has_numbers:
        suggestions.append("Try quantifying your achievements with numbers (e.g., 'improved performance by 20%').")

    word_count = len(text.split())
    if word_count < 100:
        suggestions.append("Your resume looks quite short. Consider adding more detail to your experience and projects.")

    if not suggestions:
        suggestions.append("Great job! Your resume covers all the basics we check for.")

    return suggestions

def extract_name(text):
    lines = text.strip().split('\n')
    return lines[0] if lines else "Not found"

def extract_email(text):
    match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    return match.group() if match else "Not found"

def extract_phone(text):
    match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    return match.group() if match else "Not found"

def extract_skills(text):
    text_lower = text.lower()
    found_skills = []
    for skill in COMMON_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)
    return found_skills
def get_missing_skills(found_skills):
    missing = [skill for skill in CORE_SKILLS if skill not in found_skills]
    return missing

if __name__ == '__main__':
    app.run(debug=True)