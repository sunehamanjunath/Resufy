# Resufy — Resume Analyzer

Resufy is a full-stack web app that analyzes resumes (PDF or DOCX) and gives instant, actionable feedback — an ATS compatibility score, detected skills, missing skills, and specific suggestions for improvement.

All analysis is rule-based (regex pattern matching, keyword detection, and a transparent point-based scoring system) rather than using machine learning or an LLM — a deliberate choice to keep the logic explainable and fully understood end-to-end. See [Future Improvements](#future-improvements) for planned AI integration.

Built as a learning project to practice Python, Flask, and full-stack web development from the ground up.

## Features

- **Resume Upload** — supports both PDF and DOCX formats
- **Text Extraction** — parses resume content using `pdfplumber` and `python-docx`
- **Field Parsing** — extracts name, email, and phone number using regex
- **Skill Detection** — identifies technical skills mentioned in the resume via keyword matching
- **Gap Analysis** — flags commonly expected skills that are missing
- **ATS Score** — a weighted score (out of 100) based on completeness, skills, sections, and resume depth
- **Actionable Suggestions** — rule-based tips (if/else checks, not AI-generated) covering contact info, resume sections, quantified achievements, and length

## Tech Stack

**Backend:** Python, Flask, `pdfplumber`, `python-docx`, `re` (regex)
**Frontend:** HTML, CSS, JavaScript (vanilla, no frameworks)
**Design:** Custom design system — Fraunces + Inter typography, a paper/highlighter visual theme

## Running Locally

1. Clone the repository
   ```
   git clone <your-repo-url>
   cd AI-Resume-analyzer
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Run the app
   ```
   python app.py
   ```

4. Open `http://127.0.0.1:5000` in your browser

## Project Structure

```
├── app.py                 # Flask app, routes, parsing & scoring logic
├── requirements.txt        # Python dependencies
├── templates/
│   ├── index.html          # Landing page
│   └── dashboard.html      # Results page
├── static/
│   ├── css/style.css
│   └── js/script.js
└── uploads/                 # Temporary storage for uploaded resumes (not tracked in git)
```

## How the ATS Score Works

The score is a simple, transparent point system — not a black box:
- Contact info completeness (name, email, phone): up to 40 points
- Skills matched: up to 20 points
- Key resume sections present: up to 20 points
- Resume depth (word count): up to 20 points

## Future Improvements

- Target-role-specific skill recommendations
- Genuine AI integration — LLM-based suggestions (e.g. OpenAI API) instead of rule-based ones
- Smooth, no-reload uploads (AJAX)
- Persisting past analyses with a database

## Author

Built by Suneha — first-year B.E. Computer Science & Engineering student, Dayananda Sagar College of Engineering.
