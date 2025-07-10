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

# Custom CSS for modern, clean design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        min-height: 100vh;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Main container */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }
    
    /* Header styling */
    .header-section {
        text-align: center;
        margin-bottom: 3rem;
        padding: 3rem 0;
        background: white;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #64748b;
        margin: 1rem 0 0 0;
        font-weight: 400;
    }
    
    .date-display {
        display: inline-block;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        margin-top: 1.5rem;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    /* Control panel */
    .control-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .control-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid #f1f5f9;
        transition: all 0.3s ease;
    }
    
    .control-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .card-content {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    .status-badge {
        background: #f0f9ff;
        color: #0369a1;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid #bae6fd;
    }
    
    /* News sections */
    .news-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f1f5f9;
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
    }
    
    .section-icon {
        font-size: 1.5rem;
    }
    
    /* News items */
    .news-grid {
        display: grid;
        gap: 1.5rem;
    }
    
    .news-item {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 4px solid #3b82f6;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .news-item:hover {
        background: #f1f5f9;
        transform: translateX(4px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .news-number {
        position: absolute;
        top: -8px;
        left: -8px;
        background: #3b82f6;
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .news-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0 0 0.75rem 0;
        line-height: 1.4;
    }
    
    .news-content {
        color: #475569;
        line-height: 1.6;
        margin-bottom: 0.75rem;
    }
    
    .news-source {
        color: #94a3b8;
        font-size: 0.85rem;
        font-style: italic;
    }
    
    /* Button styling */
    .refresh-button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        width: 100%;
    }
    
    .refresh-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4) !important;
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
    }
    
    /* Status messages */
    .status-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .status-error {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Footer */
    .footer-section {
        background: #1e293b;
        color: #cbd5e1;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-top: 3rem;
    }
    
    .footer-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: white;
        margin-bottom: 1rem;
    }
    
    .footer-content {
        font-size: 0.9rem;
        line-height: 1.6;
        opacity: 0.8;
    }
    
    /* References section */
    .references-section {
        background: #f8fafc;
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 2rem;
        border: 1px solid #e2e8f0;
    }
    
    .reference-link {
        display: block;
        color: #3b82f6;
        text-decoration: none;
        padding: 0.5rem 0;
        border-bottom: 1px solid #f1f5f9;
        transition: color 0.3s ease;
    }
    
    .reference-link:hover {
        color: #1d4ed8;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        .control-grid {
            grid-template-columns: 1fr;
        }
        .news-container {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="header-section">
    <h1 class="main-title">AI Intelligence Brief</h1>
    <p class="subtitle">Daily insights into artificial intelligence developments</p>
    <div class="date-display">📅 Today's Report</div>
</div>
""", unsafe_allow_html=True)

# Control Panel
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="control-card">
        <h3 class="card-title">📊 Report Status</h3>
        <div class="card-content">
    """, unsafe_allow_html=True)
    
    # Show last updated time
    try:
        report_path = "daily_ai_news_report.md"
        if os.path.exists(report_path):
            mod_time = os.path.getmtime(report_path)
            last_updated = datetime.fromtimestamp(mod_time).strftime("%B %d, %Y at %I:%M %p")
            st.markdown(f'<div class="status-badge">Last updated: {last_updated}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-badge">Report pending</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div class="status-badge">Status unknown</div>', unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="control-card">
        <h3 class="card-title">⚙️ Automation</h3>
        <div class="card-content">
            <strong>Schedule:</strong> 1:00 AM London time<br>
            <strong>Email:</strong> raphael.treffny@teleplanforsberg.com<br>
            <strong>Status:</strong> <span style="color: #10b981;">Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="control-card">
        <h3 class="card-title">🔄 Manual Update</h3>
        <div class="card-content">
    """, unsafe_allow_html=True)
    
    # Refresh button
    if st.button("🔄 Refresh News", help="Fetch latest AI news", use_container_width=True):
        with st.spinner("🔍 Fetching latest AI news..."):
            try:
                current_dir = os.getcwd()
                target_dir = "/home/ubuntu/AINews"
                
                if os.path.exists(target_dir):
                    os.chdir(target_dir)
                    
                    result = subprocess.run(
                        ["python3", "generate_and_push_report.py"], 
                        capture_output=True, 
                        text=True,
                        timeout=180,
                        cwd=target_dir
                    )
                    
                    os.chdir(current_dir)
                    
                    if result.returncode == 0:
                        st.markdown('<div class="status-success">✅ News updated successfully!</div>', unsafe_allow_html=True)
                        time.sleep(2)
                        st.rerun()
                    else:
                        error_msg = result.stderr if result.stderr else "Unknown error"
                        st.markdown(f'<div class="status-error">❌ Update failed: {error_msg[:100]}...</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="status-error">❌ Script directory not found</div>', unsafe_allow_html=True)
                    
            except subprocess.TimeoutExpired:
                st.markdown('<div class="status-error">⏰ Update timed out. Please try again.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="status-error">❌ Error: {str(e)[:50]}...</div>', unsafe_allow_html=True)
            finally:
                try:
                    os.chdir(current_dir)
                except:
                    pass
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

# Load and display content
try:
    with open("daily_ai_news_report.md", "r") as f:
        content = f.read()
    
    lines = content.split('\n')
    current_section = ""
    current_date = ""
    
    for line in lines:
        if line.startswith('## Date:'):
            current_date = line.replace('## Date:', '').strip()
            # Update the date display
            st.markdown(f"""
            <script>
            document.querySelector('.date-display').innerHTML = '📅 {current_date}';
            </script>
            """, unsafe_allow_html=True)
            
        elif line.startswith('### '):
            if current_section:  # Close previous section
                st.markdown('</div></div>', unsafe_allow_html=True)
            
            current_section = line.replace('### ', '').strip()
            
            # Choose icon based on section
            if "General" in current_section:
                icon = "🤖"
            elif "Defense" in current_section or "Security" in current_section:
                icon = "🛡️"
            elif "Tools" in current_section or "Innovation" in current_section:
                icon = "🔧"
            else:
                icon = "📰"
            
            st.markdown(f"""
            <div class="news-container">
                <div class="section-header">
                    <span class="section-icon">{icon}</span>
                    <h2 class="section-title">{current_section}</h2>
                </div>
                <div class="news-grid">
            """, unsafe_allow_html=True)
            
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
                        <div class="news-number">{number}</div>
                        <div class="news-title">{title}</div>
                        <div class="news-content">{content_text}</div>
                        <div class="news-source">{source_text}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
        elif line.startswith('## References'):
            if current_section:  # Close current section
                st.markdown('</div></div>', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="news-container">
                <div class="section-header">
                    <span class="section-icon">📚</span>
                    <h2 class="section-title">References</h2>
                </div>
                <div class="references-section">
            """, unsafe_allow_html=True)
            
        elif line.startswith('[Ref') and ']' in line:
            ref_parts = line.split('] ', 1)
            if len(ref_parts) == 2:
                ref_num = ref_parts[0] + ']'
                ref_url = ref_parts[1]
                st.markdown(f'<a href="{ref_url}" target="_blank" class="reference-link"><strong>{ref_num}</strong> {ref_url}</a>', unsafe_allow_html=True)
    
    # Close any open sections
    if current_section:
        st.markdown('</div></div>', unsafe_allow_html=True)
    
except FileNotFoundError:
    st.markdown("""
    <div class="news-container">
        <div style="text-align: center; padding: 3rem; color: #64748b;">
            <h2>📄 No Report Available</h2>
            <p>Click the 'Refresh News' button to generate the latest AI news report.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
except Exception as e:
    st.markdown("""
    <div class="news-container">
        <div style="text-align: center; padding: 3rem; color: #64748b;">
            <h2>⚠️ Loading Error</h2>
            <p>Unable to load the report. Please try refreshing.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer-section">
    <div class="footer-title">🤖 AI Intelligence System</div>
    <div class="footer-content">
        Automated daily briefings • Professional analysis • Real-time monitoring<br>
        📧 Newsletter delivery • 🕐 Scheduled updates • 🔄 Manual refresh capability
    </div>
</div>
""", unsafe_allow_html=True)

