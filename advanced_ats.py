import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import io
import PyPDF2
import docx2txt

# Custom stopwords list
STOPWORDS = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"])

def preprocess_text(text):
    # Convert to lowercase and remove special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    
    # Tokenize and remove stopwords
    words = text.split()
    return ' '.join([word for word in words if word not in STOPWORDS])

def get_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    return cosine_similarity(vectorizer)[0][1]

def extract_keywords(text, n=10):
    words = text.split()
    word_counts = Counter(words)
    return [word for word, _ in word_counts.most_common(n)]

def plot_keyword_comparison(jd_keywords, resume_keywords):
    jd_set = set(jd_keywords)
    resume_set = set(resume_keywords)
    common = jd_set.intersection(resume_set)
    only_jd = jd_set - resume_set
    only_resume = resume_set - jd_set
    
    data = [len(common), len(only_jd), len(only_resume)]
    labels = ['Common', 'Only in Job Description', 'Only in Resume']
    colors = ['#66b3ff', '#ff9999', '#99ff99']
    
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

def analyze_skills(job_description, resume):
    skills = ['python', 'java', 'c++', 'javascript', 'html', 'css', 'sql', 'react', 'angular', 'node.js',
              'machine learning', 'data analysis', 'project management', 'agile', 'scrum']
    
    jd_skills = [skill for skill in skills if skill in job_description.lower()]
    resume_skills = [skill for skill in skills if skill in resume.lower()]
    
    data = {'Skill': skills,
            'In Job Description': [skill in jd_skills for skill in skills],
            'In Resume': [skill in resume_skills for skill in skills]}
    
    df = pd.DataFrame(data)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.set_index('Skill')[['In Job Description', 'In Resume']], cmap='YlGnBu', cbar=False, ax=ax)
    plt.title('Skills Comparison')
    st.pyplot(fig)

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_file):
    return docx2txt.process(docx_file)

def main():
    st.title("Advanced Application Tracking System")

    # Job Description Input
    st.header("Job Description")
    job_description = st.text_area("Enter the job description:")

    # Resume Input
    st.header("Resume")
    resume_input_method = st.radio("Choose resume input method:", ("Upload File", "Enter Text"))

    if resume_input_method == "Upload File":
        uploaded_file = st.file_uploader("Choose your resume file", type=['txt', 'pdf', 'docx'])
        if uploaded_file is not None:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            try:
                if file_extension == 'txt':
                    resume = uploaded_file.getvalue().decode("utf-8")
                elif file_extension == 'pdf':
                    resume = extract_text_from_pdf(uploaded_file)
                elif file_extension == 'docx':
                    resume = extract_text_from_docx(uploaded_file)
                st.success("File successfully uploaded and processed!")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                resume = ""
        else:
            resume = ""
    else:
        resume = st.text_area("Enter your resume:")

    if st.button("Analyze"):
        if job_description and resume:
            try:
                # Preprocess texts
                processed_jd = preprocess_text(job_description)
                processed_resume = preprocess_text(resume)

                # Calculate similarity
                similarity = get_cosine_similarity(processed_jd, processed_resume)
                st.subheader("Resume Match Score")
                st.progress(similarity)
                st.write(f"Similarity: {similarity:.2%}")

                # Extract keywords
                jd_keywords = extract_keywords(processed_jd)
                resume_keywords = extract_keywords(processed_resume)

                # Find missing keywords
                missing_keywords = set(jd_keywords) - set(resume_keywords)

                st.subheader("Keyword Analysis")
                col1, col2 = st.columns(2)

                with col1:
                    st.write("Top Job Description Keywords:")
                    st.write(", ".join(jd_keywords))

                with col2:
                    st.write("Top Resume Keywords:")
                    st.write(", ".join(resume_keywords))

                st.subheader("Recommended Keywords to Add")
                st.write(", ".join(missing_keywords))

                st.subheader("Keyword Comparison")
                plot_keyword_comparison(jd_keywords, resume_keywords)

                st.subheader("Skills Analysis")
                analyze_skills(job_description, resume)

                # Sentiment Analysis
                st.subheader("Sentiment Analysis")
                
                jd_sentiment = TextBlob(job_description).sentiment.polarity
                resume_sentiment = TextBlob(resume).sentiment.polarity
                
                st.write(f"Job Description Sentiment: {jd_sentiment:.2f}")
                st.write(f"Resume Sentiment: {resume_sentiment:.2f}")
                
                if abs(jd_sentiment - resume_sentiment) > 0.5:
                    st.warning("The tone of your resume significantly differs from the job description. Consider adjusting your language.")

            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
        else:
            st.warning("Please enter both job description and resume.")

if __name__ == "__main__":
    main()