# Esports Consumption Analysis Dashboard 

An interactive data science dashboard analyzing the hidden psychological factors that drive esports consumption.

## Live Demo

https://malagatti-esports-consumption-pca-2013-app-g3ckvc.streamlit.app/

## Overview

This project takes raw survey data from respondents and applies **Principal Component Analysis (PCA)** to uncover the perceptions of respondents as to why people consume E-sports content.

By mathematically reducing 8 complex survey variables into 2 core psychological dimensions, the application successfully identifies two distinct consumer profiles:

1. **Compensatory Psychological Needs (PC1):** Driven by escapism, loneliness, weak self-control, and low self-esteem.
2. **Social & Competitive Engagement (PC2):** Driven by the thrill of competition, satisfaction, and a sense of community/belonging.

The dashboard allows users to dynamically explore how these psychological profiles shift across different demographic segments, including **Age, Gender, Income, Education Level, and Gaming Frequency**.

## Tech Stack

- **Python** (Core Logic)
- **Streamlit** (Web Dashboard Framework)
- **Scikit-Learn** (Machine Learning & Dimensionality Reduction)
- **Plotly Express** (Interactive Data Visualizations)
- **Pandas & NumPy** (Data Cleaning and Matrix Operations)
