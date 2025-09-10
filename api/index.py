#!/usr/bin/env python3
"""
Vercel-optimized FastAPI Server for N8N Workflow Documentation
Ultra-simplified version for serverless deployment.
"""

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
import json
import os

# Initialize FastAPI app
app = FastAPI(
    title="N8N Workflow Documentation API",
    description="Fast API for browsing and searching workflow documentation",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data for Vercel deployment
MOCK_CATEGORIES = [
    "AI Agent Development",
    "Business Process Automation",
    "CRM & Sales",
    "Cloud Storage & File Management",
    "Communication & Messaging",
    "Creative Content & Video Automation",
    "Creative Design Automation",
    "Data Processing & Analysis",
    "E-commerce & Retail",
    "Financial & Accounting",
    "Marketing & Advertising Automation",
    "Project Management",
    "Social Media Management",
    "Technical Infrastructure & DevOps",
    "Uncategorized",
    "Web Scraping & Data Extraction"
]

MOCK_WORKFLOWS = [
    {
        "id": 1,
        "filename": "telegram_webhook_automation.json",
        "name": "Telegram Webhook Automation",
        "active": True,
        "description": "Webhook-triggered automation that integrates Telegram for messaging. Uses 8 nodes and integrates with 3 services.",
        "trigger_type": "Webhook",
        "complexity": "medium",
        "node_count": 8,
        "integrations": ["Telegram", "Webhook", "HTTP Request"],
        "tags": [],
        "created_at": "",
        "updated_at": ""
    },
    {
        "id": 2,
        "filename": "google_sheets_automation.json", 
        "name": "Google Sheets Data Processing",
        "active": True,
        "description": "Scheduled automation that processes Google Sheets data. Uses 12 nodes and integrates with 4 services.",
        "trigger_type": "Scheduled",
        "complexity": "medium",
        "node_count": 12,
        "integrations": ["Google Sheets", "Gmail", "Slack", "HTTP Request"],
        "tags": [],
        "created_at": "",
        "updated_at": ""
    }
]

# Root route with language detection
@app.get("/")
async def root(request: Request, lang: Optional[str] = Query(None)):
    """Serve the main documentation page with language preference."""
    
    # Determine language preference
    chosen_lang = lang or request.cookies.get("lang")
    
    if not chosen_lang:
        # Try to detect from headers
        accept_language = request.headers.get("Accept-Language", "")
        if "zh" in accept_language.lower():
            chosen_lang = "zh"
        else:
            chosen_lang = "en"
    
    # For Vercel, serve static HTML content
    index_file_name = "index-zh.html" if chosen_lang == "zh" else "index.html"
    
    try:
        with open(f"static/{index_file_name}", "r", encoding="utf-8") as f:
            content = f.read()
        
        response = HTMLResponse(content)
        response.set_cookie(key="lang", value=chosen_lang, httponly=True, max_age=3600 * 24 * 30)
        return response
    except FileNotFoundError:
        return HTMLResponse(f"""
        <html><body>
        <h1>N8N Workflow Documentation</h1>
        <p>Welcome to the N8N Workflow Documentation platform.</p>
        <p>This is a serverless deployment on Vercel.</p>
        <p>Language: {chosen_lang}</p>
        <p>Static files not found, serving basic content.</p>
        </body></html>
        """)

# API Routes
@app.get("/api/stats")
async def get_stats():
    """Get workflow statistics."""
    return {
        "total": 2055,
        "active": 1847,
        "total_nodes": 29445,
        "unique_integrations": 365
    }

@app.get("/api/categories")
async def get_categories(lang: str = Query("en")):
    """Get available workflow categories."""
    categories = MOCK_CATEGORIES.copy()
    
    if lang == "zh":
        # Simple translation mapping
        translations = {
            "AI Agent Development": "AI 智能体开发",
            "Business Process Automation": "业务流程自动化",
            "CRM & Sales": "客户关系管理与销售",
            "Cloud Storage & File Management": "云存储与文件管理",
            "Communication & Messaging": "通信与消息传递",
            "Creative Content & Video Automation": "创意内容与视频自动化",
            "Creative Design Automation": "创意设计自动化",
            "Data Processing & Analysis": "数据处理与分析",
            "E-commerce & Retail": "电子商务与零售",
            "Financial & Accounting": "金融与会计",
            "Marketing & Advertising Automation": "营销与广告自动化",
            "Project Management": "项目管理",
            "Social Media Management": "社交媒体管理",
            "Technical Infrastructure & DevOps": "技术基础设施与运维",
            "Uncategorized": "未分类",
            "Web Scraping & Data Extraction": "网页抓取与数据提取"
        }
        categories = [translations.get(cat, cat) for cat in categories]
    
    return {"categories": categories}

@app.get("/api/category-mappings")
async def get_category_mappings():
    """Get filename to category mappings."""
    return {"mappings": {}}

@app.get("/api/workflows")
async def search_workflows(
    q: str = Query("", description="Search query"),
    trigger: str = Query("all", description="Filter by trigger type"),
    complexity: str = Query("all", description="Filter by complexity"),
    active_only: bool = Query(False, description="Show only active workflows"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    lang: str = Query("en", description="Language for translation")
):
    """Search and filter workflows with pagination."""
    
    workflows = MOCK_WORKFLOWS.copy()
    
    # Apply basic filtering
    if active_only:
        workflows = [w for w in workflows if w["active"]]
    
    if q:
        workflows = [w for w in workflows if q.lower() in w["name"].lower() or q.lower() in w["description"].lower()]
    
    # Apply translations for Chinese
    if lang == "zh":
        for workflow in workflows:
            # Translate descriptions (basic example)
            desc = workflow["description"]
            desc = desc.replace("Webhook-triggered automation that", "Webhook触发的自动化流程，")
            desc = desc.replace("Scheduled automation that", "定时自动化流程，")
            desc = desc.replace("nodes", "个节点")
            desc = desc.replace("services", "个服务")
            workflow["description"] = desc
    
    total = len(workflows)
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    page_workflows = workflows[start:end]
    
    return {
        "workflows": page_workflows,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": total_pages,
        "query": q,
        "filters": {
            "trigger": trigger,
            "complexity": complexity,
            "active_only": active_only
        }
    }

# SEO files
@app.get("/sitemap.xml")
async def get_sitemap():
    """Serve sitemap.xml for search engines."""
    try:
        return FileResponse("static/sitemap.xml", media_type="application/xml")
    except FileNotFoundError:
        return HTTPException(status_code=404, detail="Sitemap not found")

@app.get("/robots.txt")
async def get_robots():
    """Serve robots.txt for web crawlers."""
    try:
        return FileResponse("static/robots.txt", media_type="text/plain")
    except FileNotFoundError:
        return HTTPException(status_code=404, detail="Robots.txt not found")

@app.get("/llms.txt")
async def get_llms():
    """Serve llms.txt for Large Language Models."""
    try:
        return FileResponse("static/llms.txt", media_type="text/plain")
    except FileNotFoundError:
        return HTTPException(status_code=404, detail="LLMs.txt not found")

# Health check
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "N8N Workflow API is running on Vercel"}

# For Vercel - this is the entry point
def handler(request):
    """Vercel serverless function handler."""
    return app(request)
