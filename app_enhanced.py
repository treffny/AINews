import streamlit as st
import os
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="Daily AI News Report",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS for better readability and expanded content
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
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
    
    /* Header styling */
    .header-section {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }
    
    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e293b 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #475569;
        margin: 1rem 0 0 0;
        font-weight: 500;
    }
    
    .date-display {
        display: inline-block;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        font-size: 1rem;
    }
    
    /* Control cards */
    .control-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .control-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .card-content {
        color: #475569;
        font-size: 0.9rem;
        line-height: 1.6;
        font-weight: 500;
    }
    
    .status-badge {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        color: #0369a1;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid #bae6fd;
        display: inline-block;
    }
    
    /* News sections with improved contrast */
    .news-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid #f1f5f9;
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1e293b;
        margin: 0;
    }
    
    .section-icon {
        font-size: 1.6rem;
    }
    
    .section-count {
        background: #3b82f6;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: auto;
    }
    
    /* Enhanced news items for better readability */
    .news-item {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 16px;
        padding: 1.75rem;
        margin-bottom: 1.25rem;
        border-left: 5px solid #3b82f6;
        transition: all 0.3s ease;
        position: relative;
        cursor: pointer;
        text-decoration: none;
        color: inherit;
        display: block;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #f1f5f9;
    }
    
    .news-item:hover {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        transform: translateX(6px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        border-left-color: #1d4ed8;
        text-decoration: none;
        color: inherit;
    }
    
    .news-number {
        position: absolute;
        top: -10px;
        left: -10px;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.85rem;
        font-weight: 700;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    .news-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0 0 1rem 0;
        line-height: 1.4;
        padding-right: 1rem;
    }
    
    .news-content {
        color: #374151;
        line-height: 1.7;
        margin-bottom: 1rem;
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    .news-source {
        color: #6b7280;
        font-size: 0.85rem;
        font-style: italic;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
    }
    
    .click-hint {
        color: #3b82f6;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.75rem;
        opacity: 0;
        transition: opacity 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .news-item:hover .click-hint {
        opacity: 1;
    }
    
    /* Pagination for large sections */
    .pagination-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        margin: 2rem 0;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .pagination-button {
        background: #3b82f6;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .pagination-button:hover {
        background: #1d4ed8;
        transform: translateY(-1px);
    }
    
    .pagination-button:disabled {
        background: #94a3b8;
        cursor: not-allowed;
        transform: none;
    }
    
    .pagination-info {
        color: #475569;
        font-weight: 600;
    }
    
    /* References section */
    .references-section {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1rem;
        border: 1px solid #e2e8f0;
    }
    
    .reference-link {
        display: block;
        color: #3b82f6;
        text-decoration: none;
        padding: 0.75rem 0;
        border-bottom: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .reference-link:hover {
        color: #1d4ed8;
        background: #f0f9ff;
        padding-left: 1rem;
        border-radius: 8px;
    }
    
    /* Footer */
    .footer-section {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #cbd5e1;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .footer-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
    }
    
    .footer-content {
        font-size: 0.95rem;
        line-height: 1.7;
        opacity: 0.9;
        font-weight: 500;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        .news-container {
            padding: 1.5rem;
        }
        .news-item {
            padding: 1.5rem;
        }
        .section-title {
            font-size: 1.5rem;
        }
    }
    
    /* Loading animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #3b82f6;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="header-section">
    <h1 class="main-title">AI Intelligence Brief</h1>
    <p class="subtitle">Comprehensive daily insights into artificial intelligence developments</p>
    <div class="date-display">📅 Today's Enhanced Report</div>
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
            <strong>Status:</strong> <span style="color: #10b981; font-weight: 700;">Active</span><br>
            <strong>Sources:</strong> 25+ AI news outlets
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="control-card">
        <h3 class="card-title">📊 Enhanced Stats</h3>
        <div class="card-content">
            <strong>Content:</strong> 10-15 items per section<br>
            <strong>Focus:</strong> 40-50% Defense & Security<br>
            <strong>Updates:</strong> <span style="color: #10b981; font-weight: 700;">Daily at 1 AM</span><br>
            <strong>Format:</strong> Comprehensive briefing
        </div>
    </div>
    """, unsafe_allow_html=True)

# Enhanced content parsing with pagination support
def parse_and_display_content():
    try:
        with open("daily_ai_news_report.md", "r") as f:
            content = f.read()
        
        lines = content.split('\n')
        current_section = ""
        current_date = ""
        references = {}
        
        # First pass: collect all references
        for line in lines:
            if line.startswith('[Ref') and ']' in line:
                ref_parts = line.split('] ', 1)
                if len(ref_parts) == 2:
                    ref_num = ref_parts[0].replace('[', '').replace('Ref', '')
                    ref_url = ref_parts[1]
                    references[ref_num] = ref_url
        
        # Second pass: display content with enhanced formatting
        in_section = False
        section_items = []
        
        for line in lines:
            if line.startswith('## Date:'):
                current_date = line.replace('## Date:', '').strip()
                
            elif line.startswith('### '):
                if in_section and section_items:  # Close previous section
                    display_section_items(section_items, current_section)
                    st.markdown('</div>', unsafe_allow_html=True)
                    section_items = []
                
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
                """, unsafe_allow_html=True)
                in_section = True
                
            elif line.strip() and line[0].isdigit() and '. **' in line:
                # Parse news item and add to section items
                item_data = parse_news_item(line, references)
                if item_data:
                    section_items.append(item_data)
                        
            elif line.startswith('## References'):
                if in_section and section_items:  # Close current section
                    display_section_items(section_items, current_section)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("""
                <div class="news-container">
                    <div class="section-header">
                        <span class="section-icon">📚</span>
                        <h2 class="section-title">References</h2>
                        <div class="section-count">{} sources</div>
                    </div>
                    <div class="references-section">
                """.format(len(references)), unsafe_allow_html=True)
                in_section = True
                
            elif line.startswith('[Ref') and ']' in line:
                ref_parts = line.split('] ', 1)
                if len(ref_parts) == 2:
                    ref_num = ref_parts[0] + ']'
                    ref_url = ref_parts[1]
                    st.markdown(f'<a href="{ref_url}" target="_blank" class="reference-link"><strong>{ref_num}</strong> {ref_url}</a>', unsafe_allow_html=True)
        
        # Close any open sections
        if in_section:
            if section_items:
                display_section_items(section_items, current_section)
            st.markdown('</div></div>', unsafe_allow_html=True)
            
    except FileNotFoundError:
        st.markdown("""
        <div class="news-container">
            <div style="text-align: center; padding: 3rem; color: #64748b;">
                <h2>📄 No Report Available</h2>
                <p>The enhanced daily AI news report will be automatically generated at 1:00 AM London time.</p>
                <div class="loading-spinner" style="margin: 1rem auto;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown("""
        <div class="news-container">
            <div style="text-align: center; padding: 3rem; color: #64748b;">
                <h2>⚠️ Loading Error</h2>
                <p>Unable to load the enhanced report. Please try again later.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def parse_news_item(line, references):
    """Parse a news item line into structured data"""
    parts = line.split('** - ', 1)
    if len(parts) == 2:
        title_part = parts[0].split('. **', 1)
        if len(title_part) == 2:
            number = title_part[0]
            title = title_part[1]
            content_part = parts[1]
            
            # Extract source and reference
            source_match = content_part.rfind('(Source: ')
            ref_match = re.search(r'\[Ref(\d+)\]', content_part)
            
            if source_match != -1:
                content_text = content_part[:source_match].strip()
                source_text = content_part[source_match:].strip()
            else:
                content_text = content_part
                source_text = ""
            
            # Get the reference URL
            ref_url = "#"
            if ref_match:
                ref_num = ref_match.group(1)
                ref_url = references.get(ref_num, "#")
            
            return {
                'number': number,
                'title': title,
                'content': content_text,
                'source': source_text,
                'url': ref_url
            }
    return None

def display_section_items(items, section_name):
    """Display section items with enhanced formatting"""
    if not items:
        return
    
    # Add section count
    st.markdown(f'<div class="section-count">{len(items)} articles</div>', unsafe_allow_html=True)
    
    # Display all items (no pagination for now, but structure is ready)
    for item in items:
        st.markdown(f"""
        <a href="{item['url']}" target="_blank" class="news-item">
            <div class="news-number">{item['number']}</div>
            <div class="news-title">{item['title']}</div>
            <div class="news-content">{item['content']}</div>
            <div class="news-source">{item['source']}</div>
            <div class="click-hint">🔗 Click to read full article</div>
        </a>
        """, unsafe_allow_html=True)

# Display the enhanced content
parse_and_display_content()

# Enhanced Footer
st.markdown("""
<div class="footer-section">
    <div class="footer-title">🤖 Enhanced AI Intelligence System</div>
    <div class="footer-content">
        Comprehensive automated briefings • Professional analysis • Real-time monitoring<br>
        📧 Newsletter delivery • 🕐 Scheduled updates • 🔗 Direct article access • 📊 25+ sources<br>
        Enhanced with 10-15 articles per section for comprehensive coverage
    </div>
</div>
""", unsafe_allow_html=True)

