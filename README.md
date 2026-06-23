
# 📄 AI Resume Screening & Candidate Ranking System

An NLP-based Resume Screening System that ranks resumes against a Job Description using TF-IDF, Cosine Similarity, Skill Matching, and ATS Scoring.

---

## 🚀 Features

- Upload multiple PDF resumes
- Paste any Job Description
- Extract text from resumes automatically
- Skill Extraction from Resume and JD
- Missing Skill Analysis
- TF-IDF Vectorization
- Cosine Similarity Matching
- ATS Score Calculation
- Candidate Ranking
- Interactive Streamlit Dashboard
- Download Results as CSV

---

## 🏗️ Project Architecture

Resume PDF
↓
Text Extraction
↓
Text Preprocessing
↓
Skill Extraction
↓
TF-IDF Vectorization
↓
Cosine Similarity
↓
Skill Gap Analysis
↓
ATS Score Calculation
↓
Candidate Ranking
↓
Dashboard & CSV Export

---

## 🛠️ Technologies Used

- Python
- NLP
- Streamlit
- Scikit-Learn
- Pandas
- PyPDF2
- TF-IDF
- Cosine Similarity

---

## 📊 ATS Score Formula

ATS Score is calculated as:

ATS Score = (40% Similarity Score) + (60% Skill Match Percentage)

Where:

- Similarity Score = TF-IDF + Cosine Similarity Match
- Skill Match Percentage = Matching JD Skills found in Resume

---

## 📂 Project Structure

```text
resume-screening-system/
│
├── app.py
├── skills.txt
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ▶️ How to Run Locally

### 1. Clone Repository

```bash
git clone <repository-url>
```

### 2. Move into Project Folder

```bash
cd resume-screening-system
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
streamlit run app.py
```

---

## 📈 Output

The system provides:

- Resume Ranking
- Raw Similarity Score
- Normalized Score
- ATS Score
- Matched Skills
- Missing Skills
- Recommendation Category

---

## 🎯 Recommendation Categories

| ATS Score | Recommendation |
|------------|----------------|
| 85+ | Highly Suitable |
| 60 - 84 | Moderately Suitable |
| Below 60 | Not Suitable |

---

## 🔮 Future Improvements

- Sentence-BERT Embeddings
- Experience Matching
- Education Matching
- Semantic Search
- LLM-based Resume Analysis
- Interview Question Generator

---