import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Esports Survey Analysis", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel('cleaned_esports_data.xlsx')
    num_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())
        
    gender_cols = [c for c in df.columns if 'Gender' in c]
    if gender_cols:
        df[gender_cols[0]] = df[gender_cols[0]].replace({
            "c) Other": "c) do not wish to disclose",
            "c) other": "c) do not wish to disclose",
            "c)Other": "c) do not wish to disclose",
            "Other": "c) do not wish to disclose"
        })
        
    return df

df = load_data()

st.title("Esports Consumption Analysis: PCA Dashboard")
st.markdown("This dashboard uses **Principal Component Analysis (PCA)** to identify the core underlying factors that drive esports consumption")

demo_cols = {
    'Gaming Frequency': [c for c in df.columns if 'Frequency' in c][0],
    'Age': [c for c in df.columns if 'Age' in c][0],
    'Gender': [c for c in df.columns if 'Gender' in c][0],
    'Income': [c for c in df.columns if 'Income' in c][0],
    'Education Level': [c for c in df.columns if 'Level of Education' in c][0]
}

st.header("Factors Influencing Consumption")
st.markdown("We have reduced the 8 distinct consumption variables from the questionnaire into 2 core driving dimensions.")

selected_demo = st.selectbox("Select Demographic Segmentation (Color Plot By):", options=list(demo_cols.keys()))
color_col = demo_cols[selected_demo]

cons_cols_text = [c for c in df.columns if 'consume e-sports services' in c]
cons_cols_num = [c.split('.')[0] + '_num' for c in cons_cols_text if c.split('.')[0] + '_num' in df.columns]

if len(cons_cols_num) > 1:
    X = df[cons_cols_num]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    pca = PCA(n_components=2)
    components = pca.fit_transform(X_scaled)
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
    
    plot_df = df.copy()
    plot_df['Compensatory Psychological Needs (PC1)'] = components[:,0]
    plot_df['Social & Competitive Engagement (PC2)'] = components[:,1]
    plot_df = plot_df.dropna(subset=[color_col])
    plot_df[color_col] = plot_df[color_col].astype(str)
    
    fig_pca = px.scatter(plot_df, x='Compensatory Psychological Needs (PC1)', y='Social & Competitive Engagement (PC2)', color=color_col, 
                         title=f"2D Projection of Respondent Profiles by {selected_demo}",
                         labels={'color': selected_demo},
                         height=800,
                         color_discrete_sequence=px.colors.qualitative.Bold)
    
    fig_pca.update_traces(marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey'))) 
    
    fig_pca.add_hline(y=0, line_width=2, line_dash="dash", line_color="black")
    fig_pca.add_vline(x=0, line_width=2, line_dash="dash", line_color="black")
    
    x_max = plot_df['Compensatory Psychological Needs (PC1)'].max()
    x_min = plot_df['Compensatory Psychological Needs (PC1)'].min()
    y_max = plot_df['Social & Competitive Engagement (PC2)'].max()
    y_min = plot_df['Social & Competitive Engagement (PC2)'].min()

    fig_pca.add_annotation(x=x_max * 0.7, y=y_max * 0.9, text="<b>High <span style='color:darkred'>PC1</span> &<br>High <span style='color:darkgreen'>PC2</span></b>", showarrow=False, font=dict(size=14, color="dimgray"), bgcolor="white", opacity=0.8)
    fig_pca.add_annotation(x=x_min * 0.7, y=y_max * 0.9, text="<b>Low <span style='color:darkred'>PC1</span> &<br>High <span style='color:darkgreen'>PC2</span></b>", showarrow=False, font=dict(size=14, color="dimgray"), bgcolor="white", opacity=0.8)
    fig_pca.add_annotation(x=x_max * 0.7, y=y_min * 0.9, text="<b>High <span style='color:darkred'>PC1</span> &<br>Low <span style='color:darkgreen'>PC2</span></b>", showarrow=False, font=dict(size=14, color="dimgray"), bgcolor="white", opacity=0.8)
    fig_pca.add_annotation(x=x_min * 0.7, y=y_min * 0.9, text="<b>Low <span style='color:darkred'>PC1</span> &<br>Low <span style='color:darkgreen'>PC2</span></b>", showarrow=False, font=dict(size=14, color="dimgray"), bgcolor="white", opacity=0.8)

    col_chart, col_legend = st.columns([4, 1])
    
    with col_chart:
        st.plotly_chart(fig_pca, use_container_width=True)
        
    with col_legend:
        st.markdown("### Component Legend")
        st.markdown(
            "**<span style='color:darkred'>PC1 (Compensatory Psychological Needs)</span>**:<br>"
            "• Low self-esteem<br>"
            "• Loneliness<br>"
            "• Weak self-control<br>"
            "• Inability to play physical sports<br>"
            "• Escapism<br><br>"
            "**<span style='color:darkgreen'>PC2 (Social & Competitive Engagement)</span>**:<br>"
            "• Satisfaction<br>"
            "• Sense of belonging<br>"
            "• Competition",
            unsafe_allow_html=True
        )
    
    loadings_df = pd.DataFrame(loadings, columns=['Compensatory Psychological Needs (PC1)', 'Social & Competitive Engagement (PC2)'], index=cons_cols_text)
    st.subheader("Factor Loadings (Correlation with Components)")
    st.dataframe(loadings_df.style.background_gradient(cmap='Blues'), use_container_width=True)
    
    st.markdown(f"**Interpretation:** The PCA successfully distilled {len(cons_cols_text)} specific survey questions into two dominant psychological dimensions. **PC1** captures compensatory and escapist motivations ({pca.explained_variance_ratio_[0]:.1%} variance), while **PC2** captures positive social and competitive drivers ({pca.explained_variance_ratio_[1]:.1%} variance).")
