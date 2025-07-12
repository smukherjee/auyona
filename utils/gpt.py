import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check for API key in environment variables
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError(
        "GROQ_API_KEY is not set in environment variables. "
        "Please add your Groq API key to the .env file"
    )

# Initialize Groq client
groq_client = Groq(api_key=groq_api_key)

def generate_valuation_summary(company_data):
    """
    Generate a valuation summary using GPT-4.
    """
    # Construct the prompt
    prompt = f"""Generate a concise (150-200 words) valuation summary for {company_data['name']}.
    
Key metrics:
- Revenue: ${company_data['revenue']:.2f}B
- Revenue Growth: {company_data['revenue_growth']:.1f}%
- Profit Margin: {company_data['profit_margin']:.1f}%
- Industry: {company_data['industry']}

Focus on:
1. Company's market position and competitive advantages
2. Financial performance and growth trends
3. Key valuation drivers and metrics
4. Risks and opportunities
5. Overall valuation perspective

Please provide a professional, balanced analysis that would be suitable for investors."""

    try:
        response = groq_client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": "You are an experienced financial analyst specializing in company valuations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return "Error generating valuation summary. Please check your Groq API key and try again."
