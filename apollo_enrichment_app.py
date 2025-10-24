import gradio as gr
import requests
import json
import os
from typing import Dict, Any, Optional
import re

class ApolloAPI:
    """Apollo API integration for data enrichment"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.apollo.io/api/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": api_key
        }
    
    def enrich_company(self, domain: str, linkedin_url: str = None, 
                      company_name: str = None, country_code: str = None) -> Dict[str, Any]:
        """
        Enrich company data using Apollo API
        """
        try:
            url = f"{self.base_url}/organizations/enrich"
            params = {
                "domain": domain
            }
            
            # Add optional parameters if provided
            if linkedin_url:
                params["linkedin_url"] = linkedin_url
            if company_name:
                params["name"] = company_name
            if country_code:
                params["country"] = country_code
            
            response = requests.post(url, json=params, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "data": data.get('organization', {}),
                    "message": "Company data enriched successfully"
                }
            else:
                return {
                    "status": "error",
                    "data": {},
                    "message": f"API Error: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "data": {},
                "message": f"Request failed: {str(e)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "data": {},
                "message": f"Unexpected error: {str(e)}"
            }
    
    def enrich_contact(self, email: str, linkedin_url: str = None,
                      first_name: str = None, last_name: str = None) -> Dict[str, Any]:
        """
        Enrich contact data using Apollo API
        """
        try:
            url = f"{self.base_url}/people/match"
            params = {
                "email": email
            }
            
            # Add optional parameters if provided
            if linkedin_url:
                params["linkedin_url"] = linkedin_url
            if first_name:
                params["first_name"] = first_name
            if last_name:
                params["last_name"] = last_name
            
            response = requests.post(url, json=params, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "data": data.get('person', {}),
                    "message": "Contact data enriched successfully"
                }
            else:
                return {
                    "status": "error",
                    "data": {},
                    "message": f"API Error: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "data": {},
                "message": f"Request failed: {str(e)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "data": {},
                "message": f"Unexpected error: {str(e)}"
            }

def validate_domain(domain: str) -> bool:
    """Validate domain format"""
    if not domain:
        return False
    domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]?\.([a-zA-Z]{2,})$'
    return bool(re.match(domain_pattern, domain))

def validate_email(email: str) -> bool:
    """Validate email format"""
    if not email:
        return False
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))

def validate_linkedin_url(url: str) -> bool:
    """Validate LinkedIn URL format"""
    if not url:
        return True  # Optional field
    # Pattern for both /in/ and /company/ LinkedIn URLs
    linkedin_pattern = r'^https?://(www\.)?linkedin\.com/(in|company)/[a-zA-Z0-9-]+/?$'
    return bool(re.match(linkedin_pattern, url))

def enrich_company_data(api_key: str, domain: str, linkedin_url: str, 
                       company_name: str, country_code: str) -> str:
    """
    Enrich company data and return formatted result
    """
    if not api_key.strip():
        return "❌ Error: Please enter your Apollo API key"
    
    if not domain.strip():
        return "❌ Error: Company domain is required"
    
    if not validate_domain(domain):
        return "❌ Error: Please enter a valid domain (e.g., example.com)"
    
    if linkedin_url and not validate_linkedin_url(linkedin_url):
        return "❌ Error: Please enter a valid LinkedIn URL (e.g., https://linkedin.com/company/example)"
    
    apollo = ApolloAPI(api_key)
    result = apollo.enrich_company(
        domain=domain.strip(),
        linkedin_url=linkedin_url.strip() if linkedin_url else None,
        company_name=company_name.strip() if company_name else None,
        country_code=country_code.strip() if country_code else None
    )
    
    if result["status"] == "success":
        data = result["data"]
        formatted_result = f"✅ {result['message']}\n\n"
        formatted_result += "📊 **Enriched Company Data:**\n"
        formatted_result += f"• **Name:** {data.get('name', 'N/A')}\n"
        formatted_result += f"• **Domain:** {data.get('domain', 'N/A')}\n"
        formatted_result += f"• **Website:** {data.get('website_url', 'N/A')}\n"
        formatted_result += f"• **LinkedIn:** {data.get('linkedin_url', 'N/A')}\n"
        formatted_result += f"• **Industry:** {data.get('industry', 'N/A')}\n"
        formatted_result += f"• **Company Size:** {data.get('estimated_num_employees', 'N/A')}\n"
        formatted_result += f"• **Location:** {data.get('city', 'N/A')}, {data.get('state', 'N/A')}, {data.get('country', 'N/A')}\n"
        formatted_result += f"• **Founded:** {data.get('founded_year', 'N/A')}\n"
        formatted_result += f"• **Description:** {data.get('short_description', 'N/A')}\n"
        return formatted_result
    else:
        return f"❌ {result['message']}"

def enrich_contact_data(api_key: str, email: str, linkedin_url: str,
                       first_name: str, last_name: str) -> str:
    """
    Enrich contact data and return formatted result
    """
    if not api_key.strip():
        return "❌ Error: Please enter your Apollo API key"
    
    if not email.strip():
        return "❌ Error: Email address is required"
    
    if not validate_email(email):
        return "❌ Error: Please enter a valid email address"
    
    if linkedin_url and not validate_linkedin_url(linkedin_url):
        return "❌ Error: Please enter a valid LinkedIn URL (e.g., https://linkedin.com/in/username)"
    
    apollo = ApolloAPI(api_key)
    result = apollo.enrich_contact(
        email=email.strip(),
        linkedin_url=linkedin_url.strip() if linkedin_url else None,
        first_name=first_name.strip() if first_name else None,
        last_name=last_name.strip() if last_name else None
    )
    
    if result["status"] == "success":
        data = result["data"]
        formatted_result = f"✅ {result['message']}\n\n"
        formatted_result += "👤 **Enriched Contact Data:**\n"
        formatted_result += f"• **Name:** {data.get('first_name', 'N/A')} {data.get('last_name', 'N/A')}\n"
        formatted_result += f"• **Email:** {data.get('email', 'N/A')}\n"
        formatted_result += f"• **LinkedIn:** {data.get('linkedin_url', 'N/A')}\n"
        formatted_result += f"• **Title:** {data.get('title', 'N/A')}\n"
        formatted_result += f"• **Company:** {data.get('organization', {}).get('name', 'N/A') if data.get('organization') else 'N/A'}\n"
        formatted_result += f"• **Location:** {data.get('city', 'N/A')}, {data.get('state', 'N/A')}, {data.get('country', 'N/A')}\n"
        formatted_result += f"• **Phone:** {data.get('phone_numbers', [{}])[0].get('raw_number', 'N/A') if data.get('phone_numbers') else 'N/A'}\n"
        formatted_result += f"• **Twitter:** {data.get('twitter_url', 'N/A')}\n"
        formatted_result += f"• **Bio:** {data.get('headline', 'N/A')}\n"
        return formatted_result
    else:
        return f"❌ {result['message']}"

# Create Gradio interface
def create_interface():
    with gr.Blocks(title="Apollo Data Enrichment Tool", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🚀 Apollo Data Enrichment Tool
        
        Enrich your company and contact data using Apollo's powerful database. 
        Get comprehensive information about companies and contacts with just a few clicks!
        
        **Note:** You'll need a free Apollo API key to use this tool. Get yours at [Apollo.io](https://apollo.io)
        """)
        
        # API Key input (shared between both forms)
        with gr.Row():
            api_key = gr.Textbox(
                label="🔑 Apollo API Key",
                placeholder="Enter your Apollo API key here...",
                type="password",
                info="Get your free API key from Apollo.io"
            )
        
        # Company Enrichment Section
        with gr.Tab("🏢 Company Enrichment"):
            gr.Markdown("""
            ### Company Data Enrichment
            Enter company details to get comprehensive information about the organization.
            **Domain is required** - all other fields are optional but help improve accuracy.
            """)
            
            with gr.Row():
                with gr.Column():
                    company_domain = gr.Textbox(
                        label="🌐 Company Domain *",
                        placeholder="example.com",
                        info="Required: Enter the company's website domain"
                    )
                    company_linkedin = gr.Textbox(
                        label="💼 LinkedIn URL",
                        placeholder="https://linkedin.com/company/example",
                        info="Optional: Company's LinkedIn page URL"
                    )
                
                with gr.Column():
                    company_name = gr.Textbox(
                        label="🏢 Company Name",
                        placeholder="Example Corp",
                        info="Optional: Company name"
                    )
                    company_country = gr.Textbox(
                        label="🌍 Country Code",
                        placeholder="US",
                        info="Optional: Two-letter country code (e.g., US, UK, CA)"
                    )
            
            company_button = gr.Button("🔍 Enrich Company Data", variant="primary")
            company_output = gr.Markdown(label="📊 Company Enrichment Results")
            
            company_button.click(
                fn=enrich_company_data,
                inputs=[api_key, company_domain, company_linkedin, company_name, company_country],
                outputs=company_output
            )
        
        # Contact Enrichment Section
        with gr.Tab("👤 Contact Enrichment"):
            gr.Markdown("""
            ### Contact Data Enrichment
            Enter contact details to get comprehensive information about the person.
            **Email is required** - all other fields are optional but help improve accuracy.
            """)
            
            with gr.Row():
                with gr.Column():
                    contact_email = gr.Textbox(
                        label="📧 Email Address *",
                        placeholder="john.doe@example.com",
                        info="Required: Person's email address"
                    )
                    contact_linkedin = gr.Textbox(
                        label="💼 LinkedIn URL",
                        placeholder="https://linkedin.com/in/johndoe",
                        info="Optional: Person's LinkedIn profile URL"
                    )
                
                with gr.Column():
                    contact_first_name = gr.Textbox(
                        label="👤 First Name",
                        placeholder="John",
                        info="Optional: Person's first name"
                    )
                    contact_last_name = gr.Textbox(
                        label="👤 Last Name",
                        placeholder="Doe",
                        info="Optional: Person's last name"
                    )
            
            contact_button = gr.Button("🔍 Enrich Contact Data", variant="primary")
            contact_output = gr.Markdown(label="👤 Contact Enrichment Results")
            
            contact_button.click(
                fn=enrich_contact_data,
                inputs=[api_key, contact_email, contact_linkedin, contact_first_name, contact_last_name],
                outputs=contact_output
            )
        
        # Instructions Section
        with gr.Tab("📖 Instructions"):
            gr.Markdown("""
            ## How to Use This Tool
            
            ### Getting Started
            1. **Get an Apollo API Key**: Visit [Apollo.io](https://apollo.io) and sign up for a free account
            2. **Enter your API Key**: Paste your API key in the field at the top
            3. **Choose your enrichment type**: Use either Company or Contact enrichment tabs
            
            ### Company Enrichment
            - **Required**: Company domain (e.g., "example.com")
            - **Optional**: LinkedIn URL, company name, country code
            - The tool will fetch comprehensive company data including industry, size, location, etc.
            
            ### Contact Enrichment
            - **Required**: Email address
            - **Optional**: LinkedIn URL, first name, last name
            - The tool will fetch comprehensive contact data including job title, company, location, etc.
            
            ### Tips for Better Results
            - Use complete, accurate information for better matching
            - LinkedIn URLs should be full URLs (e.g., https://linkedin.com/company/example)
            - Country codes should be two-letter codes (US, UK, CA, etc.)
            - Email addresses should be valid and active
            
            ### API Limits
            - Free Apollo accounts have rate limits
            - If you hit limits, wait a few minutes before trying again
            - Consider upgrading to a paid plan for higher limits
            
            ### Troubleshooting
            - **"API Error"**: Check your API key and internet connection
            - **"No data found"**: Try with different or more complete information
            - **"Invalid format"**: Check that your domain/email format is correct
            """)
        
        # Footer
        gr.Markdown("""
        ---
        **Built with ❤️ using Gradio and Apollo API**
        
        *This tool is for educational and business purposes. Please respect Apollo's terms of service.*
        """)
    
    return demo

if __name__ == "__main__":
    # Create and launch the interface
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
