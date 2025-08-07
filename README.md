# 🧠 Django Mock Exam System

A complete web-based **Mock Test Platform** built using Django — featuring custom exam uploads, timed assessments, question palettes, detailed result analysis, and downloadable PDF reports. Designed with a modern, glassy UI for an immersive exam experience.


## 🚀 Features

✅ Upload exams via JSON files  
✅ Timed exams with auto-submit functionality  
✅ Beautiful question navigation palette  
✅ Single & multiple choice support  
✅ Answer saving between questions  
✅ Result analysis with correct/incorrect highlights  
✅ Download results as professional PDF  
✅ Modern, glassy UI with responsive design


## 🖼 UI Screenshots

| Upload Page | Exam Page | Result Page |
|-------------|-----------|-------------|
| ![upload](screenshots/upload.png) | ![exam](screenshots/exam.png) | ![result](screenshots/result.png) |



## 📁 File Upload Format (JSON)

Here's the structure expected in the uploaded `.json` file:

questions.json
[
  {
    "question": "What is the capital of France?",
    "choices": ["Berlin", "Madrid", "Paris", "Rome"],
    "answer": [2]
  },
  {
    "question": "Which planet is known as the Red Planet?",
    "choices": ["Earth", "Venus", "Mars", "Jupiter"],
    "answer": [2]
  }
]

* `"answer"`: Use list of indexes (0-based), to support **multiple correct answers**.


## 📦 Technologies Used

* Django (Backend + Views)
* HTML5/CSS3 (Frontend UI)
* JavaScript (Timer, navigation)
* ReportLab (PDF generation)
* Bootstrap/Custom CSS (Modern UI)


## 🛠️ How to Run

# 1. Clone the repo
git clone https://github.com/<your-username>/django-mock-exam-system.git
cd django-mock-exam-system

# 2. Create virtual environment & install dependencies
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt

# 3. Run the server
python manage.py runserver

Access the app at: `http://127.0.0.1:8000/mock/`


## 🧪 Demo Flow

1. Visit `/mock/` to upload your JSON exam
2. Start the exam and navigate questions
3. View results after submission
4. Optionally, download results as PDF


## 🙌 Acknowledgements
Special thanks to the open-source community for tools and guidance.
Built with ❤️ by [Royalian28](https://www.linkedin.com/in/DhanushBHarathiM)


1. ✅ Create a folder `screenshots/` in your project.
2. 📸 Save and add the three screenshots as:
   - `upload.png`
   - `exam.png`
   - `result.png`
3. 📝 Add a `requirements.txt` with at least:

Django>=4.2
reportlab

Let me know — we can polish this repo professionally and publish it!
