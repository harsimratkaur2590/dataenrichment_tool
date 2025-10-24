---
title: Company Information Tool
emoji: 🏢
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
short_description: Enrich company data using Apollo API
---

# 🏢 Company Information Tool

A powerful Gradio application that enriches company data using the Apollo API. Get comprehensive information about companies with just a few clicks!

## Features

### 🏢 Company Enrichment (Free Plan)
- **Required**: Company domain (e.g., "microsoft.com")
- **Optional**: LinkedIn URL, company name, country code
- **Returns**: Comprehensive company data including:
  - Company name and domain
  - Industry and company size
  - Location (city, state, country)
  - Founded year and description
  - LinkedIn URL and website
  - And much more!

### 👤 People Search (Paid Plan Required)
- **Required**: Search query (e.g., "john smith", "software engineer")
- **Note**: Requires a paid Apollo plan
- **Returns**: List of matching people with contact information

## How to Use

1. **Get your Apollo API key**: Visit [Apollo.io](https://apollo.io) and sign up for a free account
2. **Enter your API key**: Paste your API key in the Company API key field
3. **Start enriching**: Use the Company Enrichment tab to get company data

## Demo Examples

### Tech Companies:
- `microsoft.com` - Microsoft Corporation
- `google.com` - Google LLC
- `apple.com` - Apple Inc.
- `amazon.com` - Amazon.com Inc.
- `tesla.com` - Tesla Inc.

### Other Industries:
- `nike.com` - Nike Inc.
- `coca-cola.com` - The Coca-Cola Company
- `mcdonalds.com` - McDonald's Corporation
- `walmart.com` - Walmart Inc.
- `starbucks.com` - Starbucks Corporation

## Getting Your API Key

1. Visit [Apollo.io](https://apollo.io)
2. Sign up for a free account
3. Go to your account settings
4. Find the API section
5. Generate a new API key
6. Copy the key and paste it into the application

## Built With

- **Gradio**: Web interface framework
- **Apollo API**: Data enrichment service
- **Python**: Backend logic

## License

MIT License - see LICENSE file for details.

---

**Built with ❤️ using Gradio and Apollo API**