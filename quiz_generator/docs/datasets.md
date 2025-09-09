# Datasets

*(Template refs: Annex IV ¶2(d))*  

## Overview

The Quiz Generator (CrewAI) relies on official certification documentation as its primary dataset.  
The goal is to ensure that generated quiz questions remain aligned with the **“skills measured”** defined by certification providers.

## Sources

- **Certification:** Azure AI Fundamentals (AI-900)  
- **Source:** [AI-900 Skills Measured - Microsoft Learn](https://learn.microsoft.com/en-us/credentials/certifications/exams/ai-900/)  
- **Data acquisition:** PDFs downloaded directly from Microsoft Learn documentation pages.  
- **Format:** `.pdf` (converted to text/Markdown during preprocessing).  

## Dataset Location

- **Local path:** `src/quiz_generator/dataset/`  
