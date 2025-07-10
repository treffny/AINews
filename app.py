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

# Custom CSS for clean greyscale styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
        background-color: #fafafa;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom header styling - greyscale */
    .header-container {
        background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 600;
        text-align: center;
        margin: 0;
        letter-spacing: -0.025em;
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.85);
        font-size: 1.1rem;
        text-align: center;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Control panel styling - greyscale */
    .control-panel {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
    }
    
    .control-panel h3 {
        color: #374151;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
        border-bottom: 1px solid #f3f4f6;
        padding-bottom: 0.5rem;
    }
    
    /* Date badge styling - greyscale */
    .date-badge {
        background: linear-gradient(135deg, #9ca3af 0%, #6b7280 100%);
        color: white;
        padding: 0.75rem 1.25rem;
        border-radius: 6px;
        font-size: 1rem;
        font-weight: 500;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Section styling - greyscale */
    .news-section {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-left: 3px solid #6b7280;
    }
    
    .section-title {
        color: #1f2937;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    /* News item styling - greyscale */
    .news-item {
        background: #f9fafb;
        border-radius: 6px;
        padding: 1.25rem;
        margin: 1rem 0;
        border-left: 2px solid #d1d5db;
        transition: all 0.2s ease;
    }
    
    .news-item:hover {
        background: #f3f4f6;
        border-left-color: #6b7280;
    }
    
    .news-title {
        color: #1f2937;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    
    .news-content {
        color: #4b5563;
        line-height: 1.6;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }
    
    .news-source {
        color: #6b7280;
        font-size: 0.85rem;
        font-style: italic;
    }
    
    /* Status indicators - greyscale */
    .status-success {
        background: #6b7280;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .status-error {
        background: #374151;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .last-updated {
        background: #f3f4f6;
        color: #4b5563;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        font-size: 0.9rem;
        text-align: center;
        margin: 0.5rem 0;
        border: 1px solid #e5e7eb;
    }
    
    .info-text {
        color: #6b7280;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Footer styling - greyscale */
    .footer {
        background: #374151;
        color: #d1d5db;
        padding: 1.5rem;
        margin: 2rem -1rem -1rem -1rem;
        border-radius: 8px 8px 0 0;
        text-align: center;
    }
    
    .footer-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        color: white;
    }
    
    .footer-info {
        color: #9ca3af;
        font-size: 0.85rem;
        line-height: 1.5;
    }
    
    /* Button styling - greyscale */
    .stButton > button {
        background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4b5563 0%, #374151 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
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
            padding: 1rem;
        }
        .control-panel {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🤖 Daily AI News Report</h1>
    <p class="header-subtitle">Professional AI intelligence briefing and analysis</p>
</div>
""", unsafe_allow_html=True)

# Control Panel
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.markdown("### 📊 Report Status")
    
    # Show last updated time
    try:
        report_path = "daily_ai_news_report.md"
        if os.path.exists(report_path):
            mod_time = os.path.getmtime(report_path)
            last_updated = datetime.fromtimestamp(mod_time).strftime("%B %d, %Y at %I:%M %p")
            st.markdown(f'<div class="last-updated">📅 Last updated: {last_updated}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="last-updated">📅 Report file not found</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown('<div class="last-updated">📅 Status check failed</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Automation Settings")
    st.markdown("""
    <div class="info-text">
    🕐 <strong>Schedule:</strong> Daily at 1:00 AM London time<br>
    📧 <strong>Email:</strong> raphael.treffny@teleplanforsberg.com<br>
    🔄 <strong>Auto-sync:</strong> GitHub & Streamlit Cloud<br>
    📱 <strong>Status:</strong> Active and monitoring
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.markdown("### 🔄 Manual Update")
    
    # Refresh button with proper error handling
    if st.button("🔄 Refresh News", help="Fetch latest AI news", use_container_width=True):
        with st.spinner("🔍 Fetching latest AI news..."):
            try:
                # Store current directory
                current_dir = os.getcwd()
                
                # Change to the AINews directory
                target_dir = "/home/ubuntu/AINews"
                if os.path.exists(target_dir):
                    os.chdir(target_dir)
                    
                    # Run the script with proper error handling
                    result = subprocess.run(
                        ["python3", "generate_and_push_report.py"], 
                        capture_output=True, 
                        text=True,
                        timeout=180,  # 3 minute timeout
                        cwd=target_dir
                    )
                    
                    # Restore original directory
                    os.chdir(current_dir)
                    
                    if result.returncode == 0:
                        st.markdown('<div class="status-success">✅ News updated successfully!</div>', unsafe_allow_html=True)
                        time.sleep(2)
                        st.rerun()
                    else:
                        error_msg = result.stderr if result.stderr else "Unknown error occurred"
                        st.markdown(f'<div class="status-error">❌ Update failed: {error_msg[:100]}...</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="status-error">❌ Script directory not found</div>', unsafe_allow_html=True)
                    
            except subprocess.TimeoutExpired:
                st.markdown('<div class="status-error">⏰ Update timed out. Please try again.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="status-error">❌ Error: {str(e)[:50]}...</div>', unsafe_allow_html=True)
            finally:
                # Ensure we're back in the original directory
                try:
                    os.chdir(current_dir)
                except:
                    pass
    
    st.markdown('</div>', unsafe_allow_html=True)

# Load and display the report content
try:
    with open("daily_ai_news_report.md", "r") as f:
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
                st.markdown(f'<div style="margin: 0.5rem 0; color: #6b7280;"><strong>{ref_num}</strong> <a href="{ref_url}" target="_blank" style="color: #4b5563; text-decoration: none;">{ref_url}</a></div>', unsafe_allow_html=True)
    
    # Close the last section
    st.markdown('</div>', unsafe_allow_html=True)
    
except FileNotFoundError:
    st.markdown("""
    <div class="news-section">
        <div style="text-align: center; color: #6b7280; padding: 2rem;">
            <h2>📄 Report Not Available</h2>
            <p>The daily report file is not found. Please click the 'Refresh News' button to generate the latest report.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
except Exception as e:
    st.markdown(f"""
    <div class="news-section">
        <div style="text-align: center; color: #6b7280; padding: 2rem;">
            <h2>⚠️ Loading Error</h2>
            <p>Unable to load the report. Please try refreshing the page or click 'Refresh News'.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-title">🤖 AI News Intelligence System</div>
    <div class="footer-info">
        Automated daily intelligence briefing • Professional email delivery • Real-time updates<br>
        📧 Newsletter: raphael.treffny@teleplanforsberg.com • 🕐 Schedule: 1:00 AM London time<br>
        🔄 Manual refresh available • 📊 Continuous monitoring and reporting
    </div>
</div>
""", unsafe_allow_html=True)

