
# AI Resume Screening & Candidate Ranking


import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(
    page_title="AI Resume Screening",
    page_icon="📄",
    layout="wide"
)

# SKILLS LIST

with open("skills.txt", "r", encoding="utf-8") as f:

    SKILLS = [

        line.strip().lower()

        for line in f

        if line.strip()

    ]

# st.write("Total Skills =", len(SKILLS))

# st.write(SKILLS[:20])


# PDF TEXT EXTRACTION


def extract_text_from_pdf(pdf_file):

    text = ""

    try:

        reader = PdfReader(pdf_file)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + " "

    except Exception as e:

        st.error(f"Error reading PDF: {e}")

    return text



# TEXT PREPROCESSING

def preprocess_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)

    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# SKILL EXTRACTION


def extract_skills(text):

    text = text.lower()

    found_skills = set()

    for skill in SKILLS:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            found_skills.add(skill)

    return list(found_skills)


# RECOMMENDATION


def get_recommendation(score):  # here score is ATS score 

    if score >= 85:
        return "Highly Suitable"

    elif score >= 60:
        return "Moderately Suitable"

    else:
        return "Not Suitable"


# STREAMLIT UI


st.title(
    "📄 AI Resume Screening & Candidate Ranking System"
)

st.markdown(
    "Match resumes against Job Descriptions using NLP and ATS Scoring"
)

st.write(
    "Upload Resume PDFs and paste Job Description"
)

# JOB DESCRIPTION INPUT

col1, col2 = st.columns(2)

with col1:

    job_description = st.text_area(
        "Paste Job Description",
        height=250
    )

# RESUME UPLOAD


with col2:

    uploaded_files = st.file_uploader(
        "Upload Resume PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )


# ANALYZE BUTTON


if st.button("Analyze Resumes"):

    if not job_description:

        st.warning(
            "Please enter Job Description"
        )

    elif not uploaded_files:

        st.warning(
            "Please upload resumes"
        )

    else:

        resume_texts = []

        resume_names = []

        # ==========================
        # Extract Resume Text
        # ==========================
        for file in uploaded_files:

            text = extract_text_from_pdf(file)

            text = preprocess_text(text)

            resume_texts.append(text)

            resume_names.append(file.name)

        # ==========================
        # TF-IDF
        # ==========================

        job_description = preprocess_text(
            job_description
        )

        documents = (
            [job_description]
            + resume_texts
        )

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1,2)
        )

        tfidf_matrix = (
            vectorizer.fit_transform(
                documents
            )
        )

        # ==========================
        # COSINE SIMILARITY
        # ==========================

        job_vector = tfidf_matrix[0]

        resume_vectors = tfidf_matrix[1:]

        scores = cosine_similarity(
            job_vector,
            resume_vectors
        ).flatten()

        # ==========================
        # DATAFRAME
        # ==========================

        results = pd.DataFrame({

            "Resume": resume_names,

            "Raw Score": scores

        })

        results["Raw Similarity %"] = (
            results["Raw Score"] * 100
        ).round(2)

        # Why did you normalize the scores?
        ##  Raw cosine similarity values are often small and difficult for recruiters to interpret. I normalized scores relative to the highest-ranked candidate so that the best-matching resume receives 100%, and other candidates are scored proportionally. This improves readability while preserving ranking order."
        
        max_score = results["Raw Score"].max()

        if max_score > 0:

            results["Score"] = (

                results["Raw Score"]

                / max_score

            ) * 100

        else:

            results["Score"] = 0

        results.drop(

            columns=["Raw Score"],

            inplace=True

        )

        # ==========================
        # MATCHED & MISSING SKILLS
        # ==========================

        matched_skills = []

        missing_skills = []

        matched_skill_percentage = []

        missing_skill_percentage = []

        jd_skill_set = set(
            extract_skills(job_description)
        )

        jd_skill_count = len(
            jd_skill_set
        )

        for resume in resume_texts:

            resume_skill_set = set(
                extract_skills(resume)
            )

            matched_skill_set = (
                resume_skill_set
                &
                jd_skill_set
            )

            missing_skill_set = (
                jd_skill_set
                -
                resume_skill_set
            )

            matched_skills.append(
                list(matched_skill_set)
            )

            missing_skills.append(
                list(missing_skill_set)
            )

            if jd_skill_count > 0:

                matched_percent = (
                    len(matched_skill_set)
                    / jd_skill_count
                ) * 100

                missing_percent = (
                    len(missing_skill_set)
                    / jd_skill_count
                ) * 100

            else:

                matched_percent = 0

                missing_percent = 0

            matched_skill_percentage.append(
                round(matched_percent, 2)
            )

            missing_skill_percentage.append(
                round(missing_percent, 2)
            )

     
        # STORE IN DATAFRAME
   

        results["Matched Skills"] = (
            matched_skills
        )

        results["Missing Skills"] = (
            missing_skills
        )

        results["Matched Skill %"] = (
            matched_skill_percentage
        )

        results["Missing Skill %"] = (
            missing_skill_percentage
        )


        # ATS SCORE
   

        results["ATS Score"] = (

            results["Score"] * 0.4

            +

            results["Matched Skill %"] * 0.6

        ).round(2)

    
        # RECOMMENDATION
    
        results["Recommendation"] = (
            results["ATS Score"]
            .apply(
                get_recommendation
            )
        )

        # SORTING
       

        results = results.sort_values(

            by="ATS Score",

            ascending=False

        )

        results.reset_index(

            drop=True,

            inplace=True

        )

   
        # SHOW TABLE
     

        st.subheader(
            "Candidate Ranking"
        )

        st.dataframe(results)

        
        # PROJECT SUMMARY

        st.subheader(
            "Project Summary"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Resumes",
                len(results)
            )

        with col2:

            st.metric(
                "Top ATS Score",
                f"{results['ATS Score'].max():.2f}%"
            )

        with col3:

            st.metric(
                "Average ATS Score",
                f"{results['ATS Score'].mean():.2f}%"
            )

        # INDIVIDUAL DETAILS
  

        st.subheader(
            "Candidate Details"
        )

        for index, row in results.iterrows():

            st.markdown("---")

            st.write(
                f"Rank: {index+1}"
            )

            st.write(
                f"Resume: {row['Resume']}"
            )

            st.write(
                f"Normalized Score: {round(row['Score'],2)}%"
            )

            st.write(
                f"Raw Similarity: {round(row['Raw Similarity %'],2)}%"
            )
            st.write(
                f"ATS Score: {round(row['ATS Score'],2)}%"
            )

            st.write(
                f"Matched Skill %: {row['Matched Skill %']}%"
            )

            st.write(
                f"Missing Skill %: {row['Missing Skill %']}%"
            )

            st.write(
                "Matched Skills:"
            )

            if row["Matched Skills"]:
                st.write(
                    ", ".join(
                        row["Matched Skills"]
                    )
                )
            else:
                st.write("No matched skills found")

            st.write(
                "Missing Skills:"
            )

            st.write(
                ", ".join(
                    row["Missing Skills"]
                )
            )

            st.write(
                f"Recommendation: {row['Recommendation']}"
            )

        # BAR CHART
        

        st.subheader(
            "Resume Ranking Chart"
        )

        chart_data = (
            results
            .set_index("Resume")
            ["ATS Score"]
        )

        st.bar_chart(chart_data)

       
        # CSV DOWNLOAD
        

        csv = results.to_csv(
            index=False
        )

        st.download_button(

            label="Download CSV Report",

            data=csv,

            file_name=
            "resume_ranking_results.csv",

            mime="text/csv"
        )


