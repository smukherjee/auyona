import streamlit as st
import os
from dotenv import load_dotenv
from utils.company_data import get_public_company_data, process_private_company_data
from utils.gpt import generate_valuation_summary
from utils.export import export_to_pdf, export_to_word

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(page_title="Valuation Summary Builder", layout="wide")

def main():
    st.title("Valuation Summary Builder")
    
    # Company type selection
    company_type = st.radio("Select Company Type:", ["Public", "Private"])
    
    company_data = {}
    
    if company_type == "Public":
        # Public company input
        ticker = st.text_input("Enter Stock Ticker:", help="e.g., AAPL for Apple Inc.")
        
        if ticker:
            # Reset summary when new ticker is entered
            st.session_state.summary = None
            
            with st.spinner("Fetching company data..."):
                company_data = get_public_company_data(ticker)
                
            if company_data:
                st.subheader("Company Data")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Market Cap", f"${company_data['market_cap']:,.2f}B")
                    st.metric("Revenue", f"${company_data['revenue']:,.2f}B")
                    st.metric("Net Income", f"${company_data['net_income']:,.2f}B")
                
                with col2:
                    st.metric("P/E Ratio", f"{company_data['pe_ratio']:.2f}")
                    st.metric("Revenue Growth", f"{company_data['revenue_growth']:.1f}%")
                    st.metric("Profit Margin", f"{company_data['profit_margin']:.1f}%")
    
    else:
        # Private company input
        st.subheader("Company Information")
        col1, col2 = st.columns(2)
        
        with col1:
            company_data['name'] = st.text_input("Company Name:")
            company_data['industry'] = st.text_input("Industry:")
            company_data['revenue'] = st.number_input("Revenue (in millions $):", min_value=0.0)
            company_data['revenue_growth'] = st.number_input("Revenue Growth (%):", min_value=-100.0, max_value=1000.0)
        
        with col2:
            company_data['profit_margin'] = st.number_input("Profit Margin (%):", min_value=-100.0, max_value=100.0)
            company_data['ebitda_margin'] = st.number_input("EBITDA Margin (%):", min_value=-100.0, max_value=100.0)
            company_data['competitors'] = st.text_input("Key Competitors (comma-separated):")
        
        if all(company_data.values()):
            company_data = process_private_company_data(company_data)
    
    # Initialize session state for summary
    if 'summary' not in st.session_state:
        st.session_state.summary = None

    # Generate summary
    if company_data:
        if st.button("Generate Valuation Summary"):
            with st.spinner("Generating summary..."):
                st.session_state.summary = generate_valuation_summary(company_data)
        
        # Display summary if available
        if st.session_state.summary:
            st.subheader("Valuation Summary")
            st.write(st.session_state.summary)
            
            # Export options
            st.subheader("Export Options")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Export to PDF", key="pdf_button"):
                    try:
                        with st.spinner("Generating PDF..."):
                            pdf_path = export_to_pdf(company_data, st.session_state.summary)
                            st.success(f"PDF exported successfully!")
                            # Create a download button for the PDF
                            with open(pdf_path, "rb") as file:
                                st.download_button(
                                    label="Download PDF",
                                    data=file,
                                    file_name=os.path.basename(pdf_path),
                                    mime="application/pdf",
                                )
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")
            
            with col2:
                if st.button("Export to Word", key="word_button"):
                    try:
                        with st.spinner("Generating Word document..."):
                            docx_path = export_to_word(company_data, st.session_state.summary)
                            st.success(f"Word document exported successfully!")
                            # Create a download button for the Word document
                            with open(docx_path, "rb") as file:
                                st.download_button(
                                    label="Download Word Document",
                                    data=file,
                                    file_name=os.path.basename(docx_path),
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                )
                    except Exception as e:
                        st.error(f"Error generating Word document: {str(e)}")

if __name__ == "__main__":
    main()
