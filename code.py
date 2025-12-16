import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime
from io import BytesIO
import random
import warnings
warnings.filterwarnings("ignore")

# Page Configuration
st.set_page_config(
    page_title="Data Analytics Platform",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = 0

# Custom CSS for styling
st.markdown("""
<style>
    /* Make tabs bigger and more prominent */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        white-space: pre-wrap;
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 8px;
        color: #1976d2;
        font-size: 18px;
        font-weight: 700;
        padding: 10px 30px;
        border: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: 2px solid white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Remove default streamlit padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
def descriptive_numeric(series):
    series = series.dropna()
    return {
        "Count": len(series),
        "Mean": series.mean(),
        "Median": series.median(),
        "Std Deviation": series.std(),
        "Variance": series.var(),
        "Minimum": series.min(),
        "Maximum": series.max()
    }

def freq_table(series):
    vc = series.value_counts(dropna=False)
    pct = (vc / len(series) * 100).round(2)
    return pd.DataFrame({
        "Category": vc.index.astype(str),
        "Frequency": vc.values,
        "Percentage (%)": pct.values
    })

def corr_strength(r):
    r = abs(r)
    if r < 0.2: return "Very Weak"
    if r < 0.4: return "Weak"
    if r < 0.6: return "Moderate"
    if r < 0.8: return "Strong"
    return "Very Strong"

def is_likert(series):
    vals = series.dropna().unique()
    return all(v in [1,2,3,4,5] for v in vals)

# Create tabs with bigger font
tab1, tab2, tab3 = st.tabs(["🏠  HOME", "📘  INTRODUCTION", "📊  ANALYSIS"])

# ==================== TAB 1: HOME PAGE ====================
with tab1:
    # Background gradient styling for home page
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .quote-card {
            background: rgba(255, 255, 255, 0.1);
            border-left: 4px solid #FFD700;
            padding: 15px;
            border-radius: 10px;
            font-style: italic;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Title section
    st.markdown('<div style="text-align: center; padding: 20px;">', unsafe_allow_html=True)
    st.markdown('<h1 style="color: white; font-size: 3rem; margin-bottom: 10px;">📊 Data Analytics Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: white; font-size: 1.3rem;">Complete Statistical Analysis Solution for Researchers</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Random Quote
    QUOTES = [
        "Without data, you're just another person with an opinion. - W. Edwards Deming",
        "Data is a precious thing and will last longer than the systems themselves. - Tim Berners-Lee",
        "The goal is to turn data into information, and information into insight. - Carly Fiorina",
        "In God we trust. All others must bring data. - W. Edwards Deming",
        "Data really powers everything that we do. - Jeff Weiner"
    ]
    
    quote = random.choice(QUOTES)
    st.markdown(f"""
    <div class="quote-card">
        <p style="color: white; margin: 0; font-size: 1.1rem;">"{quote.split(' - ')[0]}"</p>
        <p style="color: rgba(255, 255, 255, 0.7); text-align: right; margin: 5px 0 0 0; font-size: 1rem;">
        — {quote.split(' - ')[1]}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome section
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: white; margin-bottom: 10px;">🌟 Welcome!</h3>
        <p style="color: rgba(255, 255, 255, 0.9); font-size: 1.05rem;">
        Empowering researchers with intuitive statistical analysis tools. 
        Transform your data into meaningful insights with our comprehensive platform.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    st.markdown('<h3 style="color: white; margin: 30px 0 15px 0;">🚀 Start Analyzing</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h4 style="color: white;">📘 Introduction</h4>
            <p style="color: rgba(255, 255, 255, 0.8);">Learn about our platform</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center; background: rgba(255, 255, 255, 0.25);">
            <h4 style="color: white;">📊 Data Analysis</h4>
            <p style="color: rgba(255, 255, 255, 0.9);">Start your analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h4 style="color: white;">🎯 Quick Demo</h4>
            <p style="color: rgba(255, 255, 255, 0.8);">Try with sample data</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Core Features
    st.markdown('<h3 style="color: white; margin: 30px 0 15px 0;">✨ Core Features</h3>', unsafe_allow_html=True)
    
    features = [
        ("📋", "Descriptive Statistics", "Mean, median, variance, etc."),
        ("🔗", "Spearman Correlation", "For ordinal data analysis"),
        ("📊", "Data Visualization", "Interactive charts & plots"),
        ("📈", "Regression Analysis", "Trend lines & predictions"),
        ("🎯", "Statistical Testing", "p-values & significance"),
        ("📊", "Correlation Matrix", "Multi-variable relationships")
    ]
    
    cols = st.columns(3)
    for idx, (icon, title, desc) in enumerate(features):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="glass-card">
                <div style="font-size: 1.8rem; margin-bottom: 8px;">{icon}</div>
                <h4 style="color: white; margin: 0 0 5px 0;">{title}</h4>
                <p style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: rgba(255, 255, 255, 0.6); padding: 20px 0;">
        <p style="font-size: 1rem;">© 2024 Data Analytics Platform | Group 3 Project</p>
        <p style="font-size: 0.9rem;">Advanced Statistical Analysis with Spearman Correlation</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== TAB 2: INTRODUCTION PAGE ====================
with tab2:
    # Animated gradient background
    st.markdown("""
    <style>
        @keyframes gradientAnimation {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #e3f2fd 0%, #e0f7fa 25%, #e8eaf6 50%, #f3e5f5 75%, #e3f2fd 100%);
            background-size: 400% 400%;
            animation: gradientAnimation 20s ease infinite;
        }
        
        .main-container {
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2.5rem;
            margin: 1rem auto;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        @keyframes floatAnimation {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .team-member-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 15px;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            border-top: 5px solid;
        }
        
        .team-member-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
        }
        
        .team-member-icon {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.2rem;
            color: white;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
            animation: floatAnimation 3s ease-in-out infinite;
        }
        
        .tech-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            padding: 1.5rem;
            border: 2px solid rgba(33, 150, 243, 0.1);
            transition: all 0.3s ease;
            height: 100%;
        }
        
        .tech-card:hover {
            border-color: #2196f3;
            box-shadow: 0 8px 20px rgba(33, 150, 243, 0.15);
            transform: translateY(-3px);
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 2rem 0;">
        <h1 style="margin-bottom: 0.5rem; color: #1976d2;">📊 Advanced Statistical Analysis Platform</h1>
        <p style="font-size: 1.3rem; color: #666; margin-bottom: 1rem;">
            Comprehensive Data Analysis Solution • Group 3 Project • Professional Analytics Tool
        </p>
        <div style="padding: 1rem; background: rgba(33, 150, 243, 0.1); border-radius: 10px; display: inline-block; margin: 1rem auto;">
            <p style="font-style: italic; color: #2196f3; margin: 0; font-size: 1.1rem;">
                "It is a capital mistake to theorize before one has data." — Sherlock Holmes
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 3px; background: linear-gradient(90deg, #2196f3, #00bcd4, #2196f3); margin: 3rem 0; border-radius: 3px; opacity: 0.7;"></div>', unsafe_allow_html=True)
    
    # Project Objectives
    st.markdown("## 🎯 Project Objectives")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(33, 150, 243, 0.05); padding: 1.5rem; border-radius: 15px; height: 100%;">
            <h3 style="color: #1976d2;">🌍 Global Accessibility</h3>
            <ul style="color: #333; line-height: 1.8;">
                <li><strong>Develop an intuitive web-based platform</strong> for statistical analysis accessible to users of all skill levels</li>
                <li><strong>Support 12 international languages</strong> to ensure global accessibility and usability</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(0, 188, 212, 0.05); padding: 1.5rem; border-radius: 15px; height: 100%;">
            <h3 style="color: #00838f;">📈 Comprehensive Analysis</h3>
            <ul style="color: #333; line-height: 1.8;">
                <li><strong>Implement comprehensive descriptive statistics tools</strong> for data exploration and summary</li>
                <li><strong>Provide advanced correlation analysis</strong> using Spearman method for ordinal data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 3px; background: linear-gradient(90deg, #2196f3, #00bcd4, #2196f3); margin: 3rem 0; border-radius: 3px; opacity: 0.7;"></div>', unsafe_allow_html=True)
    
    # Technology Stack
    st.markdown("## 🛠️ Technology Stack")
    st.write("Our platform is built on a modern technology stack that ensures reliability, performance, and scalability. Each technology is carefully selected for its specific strengths in data analysis and web application development.")
    
    tech_stack = [
        {"icon": "🐍", "name": "Python 3.11+", "desc": "Core programming language for data analysis and backend logic"},
        {"icon": "🐼", "name": "Pandas", "desc": "Powerful data manipulation and analysis library for structured data"},
        {"icon": "📊", "name": "Plotly", "desc": "Interactive graphing library for creating professional visualizations"},
        {"icon": "⚡", "name": "Streamlit", "desc": "Rapid web application development framework for interactive dashboards"},
        {"icon": "🔢", "name": "NumPy", "desc": "Fundamental package for numerical computing and array operations"},
        {"icon": "🔬", "name": "SciPy", "desc": "Scientific computing library with advanced statistical functions"},
    ]
    
    cols = st.columns(3)
    for idx, tech in enumerate(tech_stack):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="tech-card">
                <div style="font-size: 2rem; margin-bottom: 1rem; color: #2196f3;">{tech['icon']}</div>
                <h4 style="margin-bottom: 0.5rem;">{tech['name']}</h4>
                <p style="color: #666; margin: 0;">{tech['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 3px; background: linear-gradient(90deg, #2196f3, #00bcd4, #2196f3); margin: 3rem 0; border-radius: 3px; opacity: 0.7;"></div>', unsafe_allow_html=True)
    
    # Team Members
    st.markdown("## 👥 Our Team")
    st.write("Meet the talented team behind this project. Each member brings unique expertise to create a comprehensive statistical analysis platform.")
    
    team_members = [
        {
            "name": "Hevita Zhofany Putri",
            "role": "Data Analyst",
            "id": "004202400016",
            "icon": "📈",
            "color": "#4CAF50"
        },
        {
            "name": "Ristia Angelina Purba",
            "role": "Data Scientist",
            "id": "004202400071",
            "icon": "👩‍🔬",
            "color": "#2196F3"
        },
        {
            "name": "Mika Lusia Panjaitan",
            "role": "Statistical Systems Developer",
            "id": "004202400101",
            "icon": "👩‍💻",
            "color": "#FF9800"
        },
        {
            "name": "Sarah Aulya Fitri Ritonga",
            "role": "Project Manager",
            "id": "004202400090",
            "icon": "👩‍💼",
            "color": "#9C27B0"
        }
    ]
    
    cols = st.columns(2)
    for idx, member in enumerate(team_members):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="team-member-card" style="border-top-color: {member['color']};">
                <div style="display: flex; align-items: center; gap: 1.5rem;">
                    <div class="team-member-icon" style="background: linear-gradient(135deg, {member['color']}, {member['color']}dd);">
                        {member['icon']}
                    </div>
                    <div style="flex: 1;">
                        <div style="font-size: 1.4rem; font-weight: 700; color: {member['color']}; margin-bottom: 0.5rem;">
                            {member['name']}
                        </div>
                        <div style="font-size: 1.1rem; font-weight: 600; color: #666; margin-bottom: 0.5rem;">
                            {member['role']}
                        </div>
                        <div style="color: #999; font-size: 0.95rem;">Student ID: {member['id']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 3px; background: linear-gradient(90deg, #2196f3, #00bcd4, #2196f3); margin: 3rem 0; border-radius: 3px; opacity: 0.7;"></div>', unsafe_allow_html=True)
    
    # About the Analysis
    st.markdown("## 📊 About the Analysis")
    st.write("""
    This application performs two major statistical procedures on the survey data:

    1. **Descriptive Analysis**, which summarizes and explains the characteristics of each item and of each variable (X and Y).  
    2. **Association Analysis (Spearman Correlation)**, which evaluates the strength and direction of the relationship between the two variables.
    """)

    st.markdown("### 1) Descriptive Analysis — Complete Explanation")
    st.write("""
    Descriptive analysis provides a detailed summary of the survey results, helping users understand the overall shape, tendencies, and variability of the data without making statistical predictions.  
    Below are the components included in this application:
    """)

    st.markdown("#### A. Basic Statistics (per item and per variable)")
    st.write("""
    - **Mean (Average)**: The central tendency of the responses; calculated by dividing the total score by the number of respondents.  
    - **Median**: The middle value of the sorted responses; more stable against extreme values.  
    - **Mode**: The most frequently appearing score — especially useful for Likert-scale items.  
    - **Minimum & Maximum**: Lowest and highest observed values.  
    - **Range**: The difference between maximum and minimum.  
    - **Standard Deviation (SD)**: Measures how much the responses vary from the mean — higher SD = more spread.  
    - **Quartiles / Percentiles (25%, 50%, 75%)**: Show how responses are distributed across the entire range.
    """)

    st.markdown("#### B. Distribution & Frequency")
    st.write("""
    - **Frequency table**: Shows how many respondents choose each scale point (e.g., 1–5).  
    - **Histogram**: Visualizes the shape of the data — skewed, symmetric, or multimodal.  
    - **Bar chart (frequency)**: Best for Likert-scale data or categorical responses.
    """)

    st.markdown("#### C. Variable-Level Summaries")
    st.write("""
    - **Boxplot**: Displays median, quartiles, and outliers of the total scores (X TOTAL, Y TOTAL).  
    - **Heatmap (optional)**: Shows relationships between items within or across variables.
    """)

    st.markdown("#### D. Data Quality Indicators (optional)")
    st.write("""
    - **Missing-value proportion**: Ensures data completeness.  
    - **Reliability (e.g., Cronbach's Alpha)**: Measures internal consistency of each variable (optional but recommended).
    """)

    st.markdown("### 2) Association Analysis Between Variables X and Y")
    st.write("""
    After calculating total scores for each variable (combining the 10 items into X and Y scores), the application performs an association analysis to evaluate the **relationship between the two variables**.
    """)

    st.markdown("#### Elements of the Association Analysis")
    st.write("""
    - **Spearman Correlation Coefficient (ρ)**: Measures the strength and direction of a monotonic relationship.  
    - **p-value**: Determines whether the correlation is statistically significant.  
    - **Automatic interpretation**: Classifies ρ as very weak, weak, moderate, strong, or very strong.  
    - **Scatter Plot (X TOTAL vs. Y TOTAL)**: Visualizes the monotonic pattern between the two variables.  
    - **Heatmap (optional)**: Shows the correlation between all items or between the two variables.
    """)

    st.markdown("#### Diagrams Used & Their Functions")
    st.write("""
    - **Scatter Plot**: Shows whether higher X values correspond to higher (or lower) Y values.  
    - **Trendline (optional)**: Helps visualize the general direction of the relationship.  
    - **Heatmap**: Convenient for evaluating multiple correlations at once.  
    - **Boxplot**: Can show how one variable behaves across categories of the other (optional).
    """)

    st.markdown("### 4) Interpretation Guide")
    st.write("""
    - **ρ > 0**: Positive relationship (higher X tends to accompany higher Y).  
    - **ρ < 0**: Negative relationship (higher X tends to accompany lower Y).  
    - **|ρ| < 0.2**: Very weak or negligible relationship.  
    - **p < 0.05**: Statistically significant — unlikely to occur by chance.  
    Always combine statistical results with conceptual understanding — significance ≠ practical importance.
    """)

    st.markdown("## 🎯 Objectives of This Program")
    st.write("""
    This program was developed with the following objectives:

    1. **Provide complete descriptive statistics** for each item and both variables.  
    2. **Display interactive visualizations** such as histograms, boxplots, scatter plots, and heatmaps.  
    3. **Measure the association** between variables X and Y using Spearman correlation.  
    4. **Generate interpretable insights** that can support academic reports or decision-making.  
    5. **Allow users to upload their own survey data**, making the tool flexible and general-purpose.
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 1.5rem; color: #666; font-size: 0.9rem; border-top: 1px solid rgba(0, 0, 0, 0.1);">
        <p style="margin: 0;">Advanced Statistical Analysis Platform • Group 3 Project • Built with ❤️ using Streamlit</p>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.7;">© 2024 All rights reserved</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== TAB 3: ANALYSIS PAGE ====================
with tab3:
    # Blue gradient background for analysis
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0d47a1, #1976d2, #42a5f5);
        }
        
        .content-box {
            background: white;
            padding: 24px;
            border-radius: 16px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        
        .takeaway-box {
            background: #f4f8ff;
            border-left: 6px solid #1e88e5;
            padding: 16px;
            border-radius: 10px;
            margin-top: 14px;
            color: black;
            font-size: 15px;
        }
        
        h1 { text-align: center; color: white; font-weight: 800; }
        h2 { color: #0d47a1; font-weight: 700; }
        h3 { color: #1565c0; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)
    
    sns.set_theme(style="whitegrid", palette=["#1e88e5", "#42a5f5", "#90caf9"])
    
    # Title
    st.markdown("<h1>📊 STATISTICAL ANALYZER PRO</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;color:white;font-size:18px;'>"
        "Advanced Descriptive & Association Analysis for Survey Data</p>",
        unsafe_allow_html=True
    )
    
    # File Upload
    st.markdown("<div class='content-box'>", unsafe_allow_html=True)
    st.markdown("## 📤 Upload Dataset")
    uploaded_file = st.file_uploader(
        "Accepted formats: CSV, Excel (.xlsx, .xls)",
        type=["csv", "xlsx", "xls"]
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)

        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        st.success("Dataset loaded successfully")
        st.info(f"Rows: {len(df)} | Columns: {len(df.columns)}")
        st.dataframe(df.head(), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Variable Selection
        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        st.markdown("## 🔍 Variable Selection")
        x_items = st.multiselect("Select X variables", df.columns)
        y_items = st.multiselect("Select Y variables", df.columns)
        create_total = st.checkbox("Create composite scores", value=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Run Analysis Button
        if st.button("▶ Run Full Analysis"):
            data = df.copy()

            if create_total:
                if x_items:
                    data["X_total"] = data[x_items].apply(pd.to_numeric, errors="coerce").sum(axis=1)
                if y_items:
                    data["Y_total"] = data[y_items].apply(pd.to_numeric, errors="coerce").sum(axis=1)

            # DESCRIPTIVE ANALYSIS
            st.markdown("## 📊 Descriptive Analysis")
            for col in x_items + y_items + ["X_total", "Y_total"]:
                if col not in data.columns:
                    continue

                st.markdown("<div class='content-box'>", unsafe_allow_html=True)
                st.markdown(f"### Variable: {col}")
                series = data[col]

                if pd.api.types.is_numeric_dtype(series):
                    desc = descriptive_numeric(series)
                    st.dataframe(pd.DataFrame(desc.items(), columns=["Statistic","Value"]))

                    fig, ax = plt.subplots(1,2, figsize=(12,4))
                    sns.histplot(series.dropna(), kde=True, ax=ax[0], color="#1e88e5")
                    sns.boxplot(x=series.dropna(), ax=ax[1], color="#90caf9")
                    st.pyplot(fig)
                    plt.close(fig)

                    st.markdown(f"""
                    <div class="takeaway-box">
                    <b>Key Takeaways:</b><br>
                    • The histogram reveals the distribution shape and potential skewness.<br>
                    • The boxplot highlights the median and identifies possible outliers.<br>
                    • Outliers indicate respondents with extreme responses that may affect the mean.
                    </div>
                    """, unsafe_allow_html=True)

                    if is_likert(series):
                        st.markdown("""
                        <div class="takeaway-box">
                        <b>Likert Scale Insight:</b><br>
                        The variable follows a Likert-type scale, allowing ordinal interpretation
                        and supporting non-parametric analysis if normality is violated.
                        </div>
                        """, unsafe_allow_html=True)

                freq = freq_table(series)
                st.dataframe(freq)
                st.markdown("""
                <div class="takeaway-box">
                <b>Frequency Interpretation:</b><br>
                • Dominant categories represent prevailing respondent opinions.<br>
                • Percentage distribution reflects response variability and concentration.
                </div>
                """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            # NORMALITY TESTING
            st.markdown("<div class='content-box'>", unsafe_allow_html=True)
            st.markdown("## 🧪 Normality Testing")
            x_norm = stats.shapiro(data["X_total"].dropna()).pvalue if "X_total" in data else 0
            y_norm = stats.shapiro(data["Y_total"].dropna()).pvalue if "Y_total" in data else 0

            st.markdown(f"""
            <div class="takeaway-box">
            <b>Normality Results:</b><br>
            X_total p-value = {x_norm:.4f}<br>
            Y_total p-value = {y_norm:.4f}<br><br>
            If p &gt; 0.05 → data is approximately normal.
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # ASSOCIATION ANALYSIS
            st.markdown("<div class='content-box'>", unsafe_allow_html=True)
            st.markdown("## 🔗 Association Analysis")

            if x_norm > 0.05 and y_norm > 0.05:
                r, p = stats.pearsonr(data["X_total"], data["Y_total"])
                method = "Pearson Correlation"
                reason = "Both variables are normally distributed and measure linear association."
            else:
                r, p = stats.spearmanr(data["X_total"], data["Y_total"])
                method = "Spearman Rank Correlation"
                reason = "Normality assumption is violated; monotonic relationship is assessed."

            strength = corr_strength(r)
            direction = "Positive" if r > 0 else "Negative"

            fig, ax = plt.subplots(figsize=(6,5))
            ax.scatter(data["X_total"], data["Y_total"], color="#1565c0", alpha=0.7)
            ax.set_xlabel("X_total")
            ax.set_ylabel("Y_total")
            st.pyplot(fig)
            plt.close(fig)

            st.markdown(f"""
            <div class="takeaway-box">
            <b>Why {method}?</b><br>
            {reason}
            </div>

            <div class="takeaway-box">
            <b>Statistical Interpretation:</b><br>
            • r = {r:.3f} indicates a <b>{strength.lower()}</b> relationship.<br>
            • Direction: <b>{direction}</b>.<br>
            • p-value = {p:.4f} → {"statistically significant" if p < 0.05 else "not statistically significant"} at α = 0.05.<br>
            • The result reflects association, not causality.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            # CONCLUSION
            st.markdown("""
            <div class="content-box">
            <h2>Overall Conclusion</h2>
            • Descriptive analysis reveals meaningful response patterns.<br>
            • Composite scores improve measurement reliability.<br>
            • Association analysis identifies interpretable statistical relationships.<br>
            • Results are suitable for academic reports, evaluations, and survey research.
            </div>
            """, unsafe_allow_html=True)

            # PDF GENERATION
            try:
                from reportlab.lib.pagesizes import letter
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.units import inch
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
                from reportlab.lib import colors
                from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
                
                pdf_buffer = BytesIO()
                doc = SimpleDocTemplate(pdf_buffer, pagesize=letter,
                                       rightMargin=72, leftMargin=72,
                                       topMargin=72, bottomMargin=18)
                
                story = []
                styles = getSampleStyleSheet()
                
                # Custom styles
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=24,
                    textColor=colors.HexColor('#0d47a1'),
                    spaceAfter=30,
                    alignment=TA_CENTER,
                    fontName='Helvetica-Bold'
                )
                
                heading_style = ParagraphStyle(
                    'CustomHeading',
                    parent=styles['Heading2'],
                    fontSize=16,
                    textColor=colors.HexColor('#1565c0'),
                    spaceAfter=12,
                    spaceBefore=12,
                    fontName='Helvetica-Bold'
                )
                
                subheading_style = ParagraphStyle(
                    'CustomSubHeading',
                    parent=styles['Heading3'],
                    fontSize=14,
                    textColor=colors.HexColor('#1976d2'),
                    spaceAfter=10,
                    spaceBefore=10,
                    fontName='Helvetica-Bold'
                )
                
                body_style = ParagraphStyle(
                    'CustomBody',
                    parent=styles['Normal'],
                    fontSize=11,
                    alignment=TA_JUSTIFY,
                    spaceAfter=12
                )
                
                highlight_style = ParagraphStyle(
                    'Highlight',
                    parent=styles['Normal'],
                    fontSize=10,
                    leftIndent=20,
                    rightIndent=20,
                    spaceAfter=12,
                    spaceBefore=12,
                    backColor=colors.HexColor('#f4f8ff'),
                    borderColor=colors.HexColor('#1e88e5'),
                    borderWidth=1,
                    borderPadding=8
                )
                
                # Title
                story.append(Paragraph("📊 STATISTICAL ANALYSIS REPORT", title_style))
                story.append(Spacer(1, 0.5*inch))
                
                # Report Information
                story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style))
                story.append(Paragraph(f"<b>Total Respondents:</b> {len(data)}", body_style))
                story.append(Paragraph(f"<b>X Variables:</b> {', '.join(x_items)}", body_style))
                story.append(Paragraph(f"<b>Y Variables:</b> {', '.join(y_items)}", body_style))
                story.append(Spacer(1, 0.3*inch))
                
                # Executive Summary
                story.append(Paragraph("Executive Summary", heading_style))
                summary = f"""
                This report presents a comprehensive statistical analysis of survey data. 
                The analysis reveals a <b>{strength.lower()}</b> {direction.lower()} relationship 
                between X and Y variables (r = {r:.3f}, p = {p:.4f}). The relationship is 
                {"<b>statistically significant</b>" if p < 0.05 else "<b>not statistically significant</b>"} 
                at α = 0.05.
                """
                story.append(Paragraph(summary, body_style))
                story.append(PageBreak())
                
                # Descriptive Analysis
                story.append(Paragraph("DESCRIPTIVE ANALYSIS", heading_style))
                story.append(Spacer(1, 0.2*inch))
                
                for idx, col in enumerate(x_items + y_items + ["X_total", "Y_total"]):
                    if col not in data.columns:
                        continue
                    
                    story.append(Paragraph(f"Variable: {col}", subheading_style))
                    series = data[col]
                    
                    if pd.api.types.is_numeric_dtype(series):
                        desc = descriptive_numeric(series)
                        
                        desc_data = [['Statistic', 'Value']]
                        for stat_name, stat_value in desc.items():
                            if isinstance(stat_value, (int, float)):
                                desc_data.append([stat_name, f"{stat_value:.2f}"])
                            else:
                                desc_data.append([stat_name, str(stat_value)])
                        
                        desc_table = Table(desc_data, colWidths=[2.5*inch, 2*inch])
                        desc_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e3f2fd')),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0d47a1')),
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 11),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                        ]))
                        story.append(desc_table)
                        story.append(Spacer(1, 0.2*inch))
                        
                        # Add charts to PDF
                        fig, ax = plt.subplots(1, 2, figsize=(10, 3.5))
                        sns.histplot(series.dropna(), kde=True, ax=ax[0], color="#1e88e5")
                        ax[0].set_title(f"Distribution of {col}", fontsize=11, fontweight='bold')
                        ax[0].set_xlabel(col, fontsize=10)
                        ax[0].set_ylabel("Frequency", fontsize=10)
                        
                        sns.boxplot(x=series.dropna(), ax=ax[1], color="#90caf9")
                        ax[1].set_title(f"Boxplot of {col}", fontsize=11, fontweight='bold')
                        ax[1].set_xlabel(col, fontsize=10)
                        
                        plt.tight_layout()
                        
                        img_buffer = BytesIO()
                        fig.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
                        img_buffer.seek(0)
                        plt.close(fig)
                        
                        img = Image(img_buffer, width=6*inch, height=2.1*inch)
                        story.append(img)
                        story.append(Spacer(1, 0.15*inch))
                        
                        takeaway = f"""
                        <b>Key Takeaways:</b><br/>
                        • The histogram reveals the distribution shape and potential skewness.<br/>
                        • The boxplot highlights the median (middle line) and identifies outliers (dots beyond whiskers).<br/>
                        • Mean = {desc['Mean']:.2f}, Median = {desc['Median']:.2f}, Std Dev = {desc['Std Deviation']:.2f}.<br/>
                        • Outliers may indicate extreme responses that affect the mean.
                        """
                        story.append(Paragraph(takeaway, highlight_style))
                        story.append(Spacer(1, 0.15*inch))
                        
                        if is_likert(series):
                            likert_note = """
                            <b>Likert Scale Insight:</b><br/>
                            This variable follows a Likert-type scale (1-5), allowing ordinal interpretation 
                            and supporting non-parametric analysis if normality is violated.
                            """
                            story.append(Paragraph(likert_note, highlight_style))
                            story.append(Spacer(1, 0.15*inch))
                    
                    # Frequency table
                    freq = freq_table(series)
                    story.append(Paragraph(f"Frequency Distribution for {col}:", subheading_style))
                    
                    freq_data = [['Category', 'Frequency', 'Percentage (%)']]
                    for _, row in freq.head(10).iterrows():
                        freq_data.append([str(row['Category']), str(row['Frequency']), f"{row['Percentage (%)']}%"])
                    
                    freq_table_obj = Table(freq_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch])
                    freq_table_obj.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e3f2fd')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0d47a1')),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ]))
                    story.append(freq_table_obj)
                    story.append(Spacer(1, 0.15*inch))
                    
                    freq_interp = """
                    <b>Frequency Interpretation:</b><br/>
                    • Dominant categories represent prevailing respondent opinions.<br/>
                    • Percentage distribution reflects response variability and concentration.
                    """
                    story.append(Paragraph(freq_interp, highlight_style))
                    story.append(Spacer(1, 0.3*inch))
                
                # Normality Testing
                story.append(PageBreak())
                story.append(Paragraph("NORMALITY TESTING", heading_style))
                story.append(Spacer(1, 0.2*inch))
                
                norm_text = """
                The Shapiro-Wilk test was performed to assess the normality of composite variables. 
                This test is crucial for determining which correlation method to use.
                """
                story.append(Paragraph(norm_text, body_style))
                story.append(Spacer(1, 0.15*inch))
                
                norm_data = [
                    ['Variable', 'p-value', 'Distribution', 'Interpretation'],
                    ['X_total', f'{x_norm:.4f}', 
                     'Normal' if x_norm > 0.05 else 'Not Normal',
                     'Use parametric tests' if x_norm > 0.05 else 'Use non-parametric tests'],
                    ['Y_total', f'{y_norm:.4f}', 
                     'Normal' if y_norm > 0.05 else 'Not Normal',
                     'Use parametric tests' if y_norm > 0.05 else 'Use non-parametric tests']
                ]
                
                norm_table = Table(norm_data, colWidths=[1.2*inch, 1*inch, 1.3*inch, 2*inch])
                norm_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e3f2fd')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0d47a1')),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ]))
                story.append(norm_table)
                story.append(Spacer(1, 0.2*inch))
                
                norm_interp = f"""
                <b>Normality Test Results:</b><br/>
                • X_total: p = {x_norm:.4f} → {'Data is approximately normal (p > 0.05)' if x_norm > 0.05 else 'Data is NOT normal (p ≤ 0.05)'}<br/>
                • Y_total: p = {y_norm:.4f} → {'Data is approximately normal (p > 0.05)' if y_norm > 0.05 else 'Data is NOT normal (p ≤ 0.05)'}<br/>
                • <b>Decision:</b> {'Both variables are normal, use Pearson correlation' if (x_norm > 0.05 and y_norm > 0.05) else 'At least one variable is not normal, use Spearman correlation'}
                """
                story.append(Paragraph(norm_interp, highlight_style))
                
                # Association Analysis
                story.append(PageBreak())
                story.append(Paragraph("ASSOCIATION ANALYSIS", heading_style))
                story.append(Spacer(1, 0.2*inch))
                
                story.append(Paragraph(f"Method Selected: {method}", subheading_style))
                method_reason = f"""
                <b>Why {method}?</b><br/>
                {reason}
                """
                story.append(Paragraph(method_reason, highlight_style))
                story.append(Spacer(1, 0.2*inch))
                
                # Scatter plot
                fig_scatter, ax = plt.subplots(figsize=(6, 5))
                ax.scatter(data["X_total"], data["Y_total"], color="#1565c0", alpha=0.7, s=60, edgecolors='white', linewidth=0.5)
                ax.set_xlabel("X_total", fontsize=12, fontweight='bold')
                ax.set_ylabel("Y_total", fontsize=12, fontweight='bold')
                ax.set_title(f"{method}\nr = {r:.3f}, p = {p:.4f}", fontsize=13, fontweight='bold', pad=15)
                ax.grid(True, alpha=0.3, linestyle='--')
                
                z = np.polyfit(data["X_total"].dropna(), data["Y_total"].dropna(), 1)
                p_fit = np.poly1d(z)
                ax.plot(data["X_total"].dropna().sort_values(), 
                       p_fit(data["X_total"].dropna().sort_values()), 
                       "r--", alpha=0.8, linewidth=2, label=f'Trend line')
                ax.legend()
                
                plt.tight_layout()
                
                scatter_buffer = BytesIO()
                fig_scatter.savefig(scatter_buffer, format='png', dpi=150, bbox_inches='tight')
                scatter_buffer.seek(0)
                plt.close(fig_scatter)
                
                scatter_img = Image(scatter_buffer, width=5*inch, height=4.2*inch)
                story.append(scatter_img)
                story.append(Spacer(1, 0.2*inch))
                
                # Correlation Results
                story.append(Paragraph("Correlation Results:", subheading_style))
                
                corr_data = [
                    ['Metric', 'Value', 'Interpretation'],
                    ['Correlation Coefficient (r)', f'{r:.3f}', f'{strength} {direction}'],
                    ['p-value', f'{p:.4f}', 'Significant' if p < 0.05 else 'Not Significant'],
                    ['Strength', strength, corr_strength(r)],
                    ['Direction', direction, 'Variables move together' if r > 0 else 'Variables move oppositely'],
                    ['Significance Level', 'α = 0.05', 'Yes' if p < 0.05 else 'No']
                ]
                
                corr_table = Table(corr_data, colWidths=[2*inch, 1.5*inch, 2*inch])
                corr_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e3f2fd')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0d47a1')),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ]))
                story.append(corr_table)
                story.append(Spacer(1, 0.2*inch))
                
                # Interpretation
                story.append(Paragraph("Statistical Interpretation:", subheading_style))
                interpretation = f"""
                <b>Detailed Interpretation:</b><br/>
                • The correlation coefficient of <b>r = {r:.3f}</b> indicates a <b>{strength.lower()}</b> relationship between X and Y.<br/>
                • Direction: <b>{direction}</b> - as X increases by one unit, Y tends to {"increase" if r > 0 else "decrease"}.<br/>
                • The p-value of <b>{p:.4f}</b> indicates the relationship is <b>{"statistically significant" if p < 0.05 else "not statistically significant"}</b> at α = 0.05.<br/>
                • Effect size: {"Small effect" if abs(r) < 0.3 else "Medium effect" if abs(r) < 0.5 else "Large effect"}.<br/>
                • <b>Important:</b> This analysis shows <b>association, NOT causation</b>. Correlation does not imply that X causes Y or vice versa.
                """
                story.append(Paragraph(interpretation, highlight_style))
                
                # Conclusions
                story.append(PageBreak())
                story.append(Paragraph("CONCLUSIONS AND RECOMMENDATIONS", heading_style))
                story.append(Spacer(1, 0.2*inch))
                
                conclusion_text = f"""
                <b>Key Findings:</b><br/>
                1. <b>Descriptive Analysis:</b> Revealed meaningful response patterns across all variables with appropriate measures of central tendency and dispersion.<br/>
                2. <b>Composite Scores:</b> X_total and Y_total were created to improve measurement reliability by aggregating multiple items.<br/>
                3. <b>Normality Testing:</b> {"Both variables showed normal distribution" if (x_norm > 0.05 and y_norm > 0.05) else "At least one variable violated normality assumption"}, 
                guiding the selection of {method}.<br/>
                4. <b>Association Analysis:</b> Found a {strength.lower()} {direction.lower()} relationship (r = {r:.3f}) that is 
                {"statistically significant (p < 0.05)" if p < 0.05 else "not statistically significant (p ≥ 0.05)"}.<br/>
                <br/>
                <b>Practical Implications:</b><br/>
                • Results are suitable for academic reports, research papers, and program evaluations.<br/>
                • The {"significant" if p < 0.05 else "non-significant"} relationship {"suggests" if p < 0.05 else "does not support"} 
                a meaningful association between X and Y variables.<br/>
                • Consider additional analyses such as regression modeling to explore predictive relationships.<br/>
                <br/>
                <b>Limitations:</b><br/>
                • Correlation does not imply causation - experimental studies needed to establish causal relationships.<br/>
                • Results are specific to this sample and may not generalize to other populations.<br/>
                • Potential confounding variables were not controlled in this analysis.<br/>
                <br/>
                <b>Recommendations:</b><br/>
                • Conduct follow-up studies with larger sample sizes to validate findings.<br/>
                • Investigate potential mediating or moderating variables.<br/>
                • Consider longitudinal designs to examine relationships over time.<br/>
                • Use these results as preliminary evidence for hypothesis generation.
                """
                story.append(Paragraph(conclusion_text, body_style))
                
                # Methodology Notes
                story.append(Spacer(1, 0.3*inch))
                story.append(Paragraph("METHODOLOGY NOTES", heading_style))
                
                methodology = f"""
                <b>Statistical Methods Used:</b><br/>
                • Descriptive Statistics: Mean, Median, Standard Deviation, Variance, Min/Max<br/>
                • Normality Testing: Shapiro-Wilk test (α = 0.05)<br/>
                • Association Analysis: {method}<br/>
                • Significance Level: α = 0.05 (95% confidence level)<br/>
                • Data Processing: Missing values handled via listwise deletion<br/>
                <br/>
                <b>Software & Tools:</b><br/>
                • Python 3.x with scientific computing libraries<br/>
                • pandas for data manipulation<br/>
                • scipy.stats for statistical testing<br/>
                • matplotlib and seaborn for visualizations<br/>
                • reportlab for PDF generation<br/>
                <br/>
                <b>Sample Characteristics:</b><br/>
                • Total Respondents: {len(data)}<br/>
                • X Variables Analyzed: {len(x_items)}<br/>
                • Y Variables Analyzed: {len(y_items)}<br/>
                • Composite Scores: Created by summing individual items<br/>
                <br/>
                <b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
                <b>Analysis Tool:</b> Statistical Analyzer Pro
                """
                story.append(Paragraph(methodology, body_style))
                
                # Build PDF
                doc.build(story)
                pdf_buffer.seek(0)
                
                # Download button
                st.download_button(
                    label="📄 Download Complete Analysis Report (PDF)",
                    data=pdf_buffer,
                    file_name=f"statistical_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    help="Click to download the complete analysis with all charts and interpretations"
                )
                
                st.success("✅ PDF report with ALL charts and analysis generated successfully!")
                st.info("📊 The PDF includes: Descriptive stats, all charts, frequency tables, normality tests, correlation analysis, and detailed interpretations.")
                
            except ImportError as ie:
                st.error("❌ Error: Required library not found!")
                st.info("Please install: pip install reportlab")
                st.code("pip install reportlab", language="bash")
            except Exception as e:
                st.error(f"❌ Error generating PDF: {str(e)}")
                st.info("Please make sure all required libraries are installed and data is properly loaded.")