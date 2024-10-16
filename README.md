# Application Tracking System (ATS)

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [File Upload](#file-upload)
7. [Analysis Components](#analysis-components)
8. [Customization](#customization)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)
11. [License](#license)

## Project Overview

The Application Tracking System (ATS) is a Streamlit-based web application designed to help job seekers optimize their resumes for specific job descriptions. By leveraging natural language processing techniques, the ATS provides insights into how well a resume matches a given job description, suggests improvements, and offers a comprehensive analysis of the application materials.

## Features

- **Resume-Job Description Similarity**: Calculates and displays a match score between the resume and job description.
- **Keyword Analysis**: Extracts and compares top keywords from both the job description and resume.
- **Keyword Recommendations**: Suggests keywords from the job description that are missing in the resume.
- **Visual Keyword Comparison**: Provides a pie chart visualizing the distribution of common and unique keywords.
- **Skills Analysis**: Generates a heatmap to compare required skills mentioned in the job description against those present in the resume.
- **Sentiment Analysis**: Analyzes the overall tone of both the job description and resume, alerting users to significant discrepancies.
- **Multiple Input Methods**: Supports direct text input and file uploads (TXT, PDF, DOCX) for both job descriptions and resumes.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Clone this repository or download the source code.

2. Navigate to the project directory in your terminal.

3. Install the required dependencies by running:

   ```
   pip install streamlit pandas scikit-learn matplotlib seaborn textblob PyPDF2 docx2txt
   ```

## Usage

1. In the project directory, run the following command:

   ```
   streamlit run ats_app.py
   ```

2. Your default web browser should open automatically with the ATS application. If it doesn't, copy the URL provided in the terminal and paste it into your browser.

3. Once the application is loaded:
   - Enter or upload a job description
   - Enter your resume text or upload a resume file
   - Click the "Analyze" button to see the results

## File Upload

The ATS supports the following file formats for resume uploads:

- Plain Text (.txt)
- PDF (.pdf)
- Microsoft Word (.docx)

Ensure your files are in one of these formats for successful processing.

## Analysis Components

### Resume Match Score

A percentage indicating how closely your resume matches the job description. The higher the percentage, the better the match.

### Keyword Analysis

Displays the top keywords from both the job description and your resume. It also provides a list of keywords present in the job description but missing from your resume.

### Keyword Comparison Visualization

A pie chart showing the distribution of keywords that are:

- Common to both the job description and resume
- Unique to the job description
- Unique to the resume

### Skills Analysis

A heatmap displaying a predefined set of skills and their presence or absence in both the job description and resume.

### Sentiment Analysis

Provides a sentiment score for both the job description and resume, indicating the overall tone of each document.

## Customization

### Modifying the Skills List

To customize the skills analyzed in the Skills Analysis section, locate the `analyze_skills` function in the `ats_app.py` file and modify the `skills` list:

```python
def analyze_skills(job_description, resume):
    skills = ['python', 'java', 'c++', 'javascript', 'html', 'css', 'sql', 'react', 'angular', 'node.js',
              'machine learning', 'data analysis', 'project management', 'agile', 'scrum']
    # ... rest of the function
```

Add or remove skills as needed to match your specific use case or industry.

### Adjusting Stopwords

The application uses a custom list of stopwords for text preprocessing. To modify this list, find the `STOPWORDS` set near the beginning of the `ats_app.py` file and add or remove words as needed.

## Troubleshooting

If you encounter any issues:

1. Ensure all dependencies are correctly installed.
2. Check that you're using a compatible Python version (3.7+).
3. Verify that your input files are in the correct format and are not corrupted.
4. If you're having problems with PDF or DOCX files, make sure they are not password-protected.

For persistent issues, please open an issue on the project's GitHub repository.

## Contributing

Contributions to improve the ATS are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
