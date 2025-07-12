# Valuation Summary Builder

A Streamlit application that generates valuation summaries for public and private companies using market data and GPT-4.

## Features

- Public company analysis using yfinance data
- Private company manual input support
- GPT-4 powered valuation summaries
- Export to PDF or Word document
- Clean, formatted output

## Setup

1. Clone the repository

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your OpenAI API key:

   ```bash
   cp .env.example .env
   ```

4. Run the application:

   ```bash
   streamlit run app.py
   ```

## Usage

1. Choose between public or private company analysis
2. For public companies:
   - Enter the stock ticker
   - Review automatically fetched data
3. For private companies:
   - Enter company details manually
   - Provide financial metrics
4. Generate valuation summary
5. Export to PDF or Word format

## Project Structure

```plaintext
.
├── app.py                 # Main Streamlit application
├── utils/
│   ├── company_data.py    # Data fetching and processing
│   ├── gpt.py            # GPT-4 integration
│   └── export.py         # PDF/Word export functionality
├── templates/            # Document templates
└── requirements.txt      # Project dependencies
```
