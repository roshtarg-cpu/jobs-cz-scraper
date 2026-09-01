# Jobs.cz Scraper 🇨🇿

Extract job listings from Jobs.cz, the leading Czech job board. Get job titles, companies, locations, salaries, and full descriptions for recruitment intelligence, market research, and talent sourcing across Czech Republic.

## 🎯 Features

- **Comprehensive Job Data**: Titles, companies, locations, salaries, job types, and descriptions
- **Flexible Search**: Search by keyword, location, category, or scrape all listings
- **AI-Ready Output**: Clean structured JSON compatible with Claude, ChatGPT, and MCP agents
- **Geographic Coverage**: Complete Czech Republic job market (50,000+ active listings)
- **Real-time Data**: Fresh listings updated hourly

## 📊 What You Get

Each job listing contains:
- `title` - Job position title
- `company` - Employer name
- `location` - City/region in Czech Republic
- `salary` - Salary range (if disclosed)
- `jobType` - Full-time, part-time, contract, etc.
- `url` - Direct link to full job posting
- `description` - Full job description text
- `postedDate` - When the job was listed
- `category` - Job category/industry
- `scrapedAt` - ISO timestamp

## 🚀 Quick Start

### For AI Agents (Claude, ChatGPT, etc.)

When connected via Apify MCP:
```
Get me 50 software engineering jobs from Czech Republic
```

### Via Apify API

```javascript
{
  "searchKeyword": "python developer",
  "location": "Praha",
  "maxResults": 100
}
```

## 🤖 AI Integration

This actor is optimized for AI agents using Apify MCP. Works seamlessly with:
- **Claude** (via Claude Desktop MCP)
- **ChatGPT** (via GPT Actions or custom plugins)
- **AI Automation tools** (n8n, Make, Zapier with MCP support)

Ask your AI agent: *"Find senior developer jobs in Prague with salaries above 80k CZK"*

## 💡 Use Cases

- **Recruitment Intelligence**: Monitor competitor hiring, identify talent pools
- **Market Research**: Track salary trends, in-demand skills
- **Lead Generation**: Find companies actively hiring (sales leads)
- **Career Research**: Discover opportunities, benchmark salaries
- **Data Analysis**: Job market trends, skills gap analysis

## 📋 Input Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `searchKeyword` | string | Job title or skill keyword | (all jobs) |
| `location` | string | City or region filter | (all locations) |
| `category` | string | Job category/industry | (all categories) |
| `maxResults` | integer | Maximum jobs to scrape | 50 |
| `proxyConfiguration` | object | Apify proxy settings | RESIDENTIAL |

## 📤 Example Output

```json
[
  {
    "title": "Senior Python Developer",
    "company": "ACME Tech s.r.o.",
    "location": "Praha",
    "salary": "80,000 - 120,000 CZK/month",
    "jobType": "Full-time",
    "url": "https://www.jobs.cz/rpd/...",
    "description": "We are looking for an experienced Python developer...",
    "postedDate": "2026-09-01",
    "category": "IT & Software Development",
    "scrapedAt": "2026-09-02T01:45:00.000Z"
  }
]
```

## 🏷️ Tags

`jobs` `recruitment` `czech-republic` `job-scraper` `employment` `talent-sourcing` `hr-tech` `market-research` `ai-agents` `mcp-compatible`

---

**Compatible with Claude, ChatGPT & AI agents via Apify MCP** • Zero Apify competition • Fresh Czech job market data • Perfect for recruitment and market intelligence
