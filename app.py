import streamlit as st
import subprocess
import os
from datetime import datetime
import time

st.set_page_config(
    page_title="Daily AI News Report",
    page_icon="🤖",
    layout="wide"
)

# Add custom CSS for better styling
st.markdown("""
<style>
.refresh-button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    margin: 10px 0;
}
.refresh-button:hover {
    background-color: #45a049;
}
.last-updated {
    color: #666;
    font-style: italic;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Header with refresh functionality
col1, col2 = st.columns([3, 1])

with col1:
    st.title("🤖 Daily AI News Report")

with col2:
    # Add refresh button
    if st.button("🔄 Refresh News", type="primary", help="Click to fetch the latest AI news"):
        with st.spinner("Fetching latest AI news... This may take a moment."):
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
                    st.success("✅ News updated successfully! The page will refresh automatically.")
                    time.sleep(2)  # Give a moment for the success message to be seen
                    st.rerun()  # Refresh the page to show new content
                else:
                    st.error(f"❌ Error updating news: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                st.error("⏰ Update timed out. Please try again later.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Show last updated time
try:
    # Get the modification time of the report file
    report_path = "/home/ubuntu/AINews/daily_ai_news_report.md"
    if os.path.exists(report_path):
        mod_time = os.path.getmtime(report_path)
        last_updated = datetime.fromtimestamp(mod_time).strftime("%B %d, %Y at %I:%M %p")
        st.markdown(f'<p class="last-updated">Last updated: {last_updated}</p>', unsafe_allow_html=True)
except:
    pass

# Load and display the report content
try:
    with open("/home/ubuntu/AINews/daily_ai_news_report.md", "r") as f:
        report_content = f.read()
    
    # Display the content
    st.markdown(report_content)
    
except FileNotFoundError:
    st.error("❌ Report file not found. Please click 'Refresh News' to generate the latest report.")
except Exception as e:
    st.error(f"❌ Error loading report: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 14px;'>
    <p>🤖 Automated AI News Report | Updates daily at 1:00 AM London time</p>
    <p>📧 Email newsletter sent to raphael.treffny@teleplanforsberg.com</p>
    <p>🔄 Use the refresh button above to get the latest news anytime</p>
</div>
""", unsafe_allow_html=True)

