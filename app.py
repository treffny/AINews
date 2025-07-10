import streamlit as st
import subprocess
import os
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Daily AI News Report",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern, professional styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .header-title {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        text-align: center;
        margin: 0.5rem 0 0 0;
        font-weight: 300;
    }
    
    /* Control panel styling */
    .control-panel {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 2rem 0;
        box-shadow: 0 2px 15px rgba(0,0,0,0.08);
        border: 1px solid #e1e5e9;
    }
    
    /* Date badge styling */
    .date-badge {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: 600;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
    }
    
    /* Section styling */
    .news-section {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 2px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
    }
    
    .section-title {
        color: #2d3748;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* News item styling */
    .news-item {
        background: #f8fafc;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 3px solid #4299e1;
        transition: all 0.3s ease;
    }
    
    .news-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .news-title {
        color: #2d3748;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .news-content {
        color: #4a5568;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }
    
    .news-source {
        color: #718096;
        font-size: 0.9rem;
        font-style: italic;
    }
    
    /* Status indicators */
    .status-success {
        background: #48bb78;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    
    .status-error {
        background: #f56565;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    
    .last-updated {
        background: #edf2f7;
        color: #4a5568;
        padding: 0.8rem 1.2rem;
        border-radius: 10px;
        font-size: 0.95rem;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
    }
    
    /* Footer styling */
    .footer {
        background: #2d3748;
        color: white;
        padding: 2rem;
        margin: 3rem -1rem -1rem -1rem;
        border-radius: 20px 20px 0 0;
        text-align: center;
    }
    
    .footer-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .footer-info {
        color: #a0aec0;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        .header-subtitle {
            font-size: 1rem;
        }
        .news-section {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🤖 Daily AI News Report</h1>
    <p class="header-subtitle">Your comprehensive source for the latest AI developments and insights</p>
</div>
""", unsafe_allow_html=True)

# Control Panel
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.markdown("### 📊 Report Status")
    
    # Show last updated time
    try:
        report_path = "/home/ubuntu/AINews/daily_ai_news_report.md"
        if os.path.exists(report_path):
            mod_time = os.path.getmtime(report_path)
            last_updated = datetime.fromtimestamp(mod_time).strftime("%B %d, %Y at %I:%M %p")
            st.markdown(f'<div class="last-updated">📅 Last updated: {last_updated}</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div class="last-updated">📅 Last updated: Unknown</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Automation Info")
    st.markdown("""
    <div style="color: #4a5568; font-size: 0.9rem; line-height: 1.6;">
    🕐 <strong>Schedule:</strong> Daily at 1:00 AM London time<br>
    📧 <strong>Email:</strong> raphael.treffny@teleplanforsberg.com<br>
    🔄 <strong>Auto-sync:</strong> GitHub & Streamlit Cloud
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.markdown("### 🔄 Manual Update")
    
    # Refresh button
    if st.button("🔄 Refresh News", type="primary", help="Click to fetch the latest AI news", use_container_width=True):
        with st.spinner("🔍 Fetching latest AI news... This may take a moment."):
            try:
                # Change to the correct directory and run the script
                os.chdir("/home/ubuntu/AINews")
                result = subprocess.run(
                    ["python3", "generate_and_push_report.py"], 
                    capture_output=True, 
                    text=True,
                    timeout=120  # 2 minute timeout
                )
                
                if result.returncode == 0:
                    st.markdown('<div class="status-success">✅ News updated successfully!</div>', unsafe_allow_html=True)
                    time.sleep(2)  # Give a moment for the success message to be seen
                    st.rerun()  # Refresh the page to show new content
                else:
                    st.markdown(f'<div class="status-error">❌ Error: {result.stderr}</div>', unsafe_allow_html=True)
                    
            except subprocess.TimeoutExpired:
                st.markdown('<div class="status-error">⏰ Update timed out. Please try again.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="status-error">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Load and display the report content
try:
    with open("/home/ubuntu/AINews/daily_ai_news_report.md", "r") as f:
        content = f.read()
    
    # Parse the content
    lines = content.split('\n')
    current_section = ""
    current_date = ""
    
    for line in lines:
        if line.startswith('## Date:'):
            current_date = line.replace('## Date:', '').strip()
            st.markdown(f'<div class="date-badge">📅 {current_date}</div>', unsafe_allow_html=True)
        elif line.startswith('### '):
            current_section = line.replace('### ', '').strip()
            st.markdown(f'<div class="news-section"><h2 class="section-title">{current_section}</h2>', unsafe_allow_html=True)
        elif line.strip() and line[0].isdigit() and '. **' in line:
            # Parse news item
            parts = line.split('** - ', 1)
            if len(parts) == 2:
                title_part = parts[0].split('. **', 1)
                if len(title_part) == 2:
                    number = title_part[0]
                    title = title_part[1]
                    content_part = parts[1]
                    
                    # Extract source
                    source_match = content_part.rfind('(Source: ')
                    if source_match != -1:
                        content_text = content_part[:source_match].strip()
                        source_text = content_part[source_match:].strip()
                    else:
                        content_text = content_part
                        source_text = ""
                    
                    st.markdown(f"""
                    <div class="news-item">
                        <div class="news-title">{number}. {title}</div>
                        <div class="news-content">{content_text}</div>
                        <div class="news-source">{source_text}</div>
                    </div>
                    """, unsafe_allow_html=True)
        elif line.startswith('## References'):
            st.markdown('</div>', unsafe_allow_html=True)  # Close current section
            st.markdown('<div class="news-section"><h2 class="section-title">📚 References</h2>', unsafe_allow_html=True)
        elif line.startswith('[Ref') and ']' in line:
            ref_parts = line.split('] ', 1)
            if len(ref_parts) == 2:
                ref_num = ref_parts[0] + ']'
                ref_url = ref_parts[1]
                st.markdown(f'<div style="margin: 0.5rem 0; color: #4299e1;"><strong>{ref_num}</strong> <a href="{ref_url}" target="_blank" style="color: #4299e1; text-decoration: none;">{ref_url}</a></div>', unsafe_allow_html=True)
    
    # Close the last section
    st.markdown('</div>', unsafe_allow_html=True)
    
except FileNotFoundError:
    st.markdown("""
    <div class="news-section">
        <div style="text-align: center; color: #e53e3e; padding: 2rem;">
            <h2>❌ Report Not Found</h2>
            <p>The daily report file is not available. Please click the 'Refresh News' button to generate the latest report.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
except Exception as e:
    st.markdown(f"""
    <div class="news-section">
        <div style="text-align: center; color: #e53e3e; padding: 2rem;">
            <h2>❌ Error Loading Report</h2>
            <p>Error: {str(e)}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-title">🤖 AI News Automation System</div>
    <div class="footer-info">
        Powered by advanced AI news aggregation • Automated daily updates • Professional email delivery<br>
        📧 Newsletter delivered to raphael.treffny@teleplanforsberg.com<br>
        🔄 Manual refresh available • 🕐 Scheduled updates at 1:00 AM London time<br>
        <br>
        <em>Stay informed with the latest AI developments in technology, defense, and innovation</em>
    </div>
</div>
""", unsafe_allow_html=True)

