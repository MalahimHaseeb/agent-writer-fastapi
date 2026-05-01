# Blog Writing Agent - FastAPI Backend

A FastAPI backend for generating blog posts using AI agents. Combines workflow orchestration with **Gemini AI** for text generation and **Tavily** for web research.

🌐 **[Live Preview](https://contentagent.malahim.dev)** | 📖 **[Read the Blog Post](https://blog.malahim.dev/ai-agents/contentagent-i-built-a-multi-agent-blog-writer-in-a-day)**

## 📋 Architecture

### Workflow (Agent Graph)

The agent processes blog generation through a sequential workflow:

```
Router → Search (Conditional) → Writer → Critic → Formatter → Output
```

1. **Router**: Analyzes topic and decides if web search is needed
2. **Search**: Performs web research if decision is SEARCH
3. **Writer**: Generates initial blog draft
4. **Critic**: Reviews and improves the draft
5. **Formatter**: Extracts metadata (title, tags, reading time, word count)

### Project Structure

```
agent-writer-fastapi/
├── main.py
├── config.py
├── logger.py
├── responses.py
├── schemas.py
├── requirements.txt
├── .env.example
├── agent/
│   ├── __init__.py
│   ├── graph.py
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── search.py
│   │   ├── writer.py
│   │   ├── critic.py
│   │   └── formatter.py
│   └── tools/
│       ├── __init__.py
│       └── search.py
└── api/
    └── __init__.py
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Gemini API key (get from [Google AI Studio](https://aistudio.google.com/))
- Tavily API key (get from [Tavily](https://tavily.com/))

### Installation

1. **Clone and navigate to the backend directory**:
```bash
cd agent-writer-fastapi
```

2. **Create virtual environment** (Linux/Ubuntu):
```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
```bash
cp .env.example .env
```
Edit `.env` and add your API keys

5. **Run the server**:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Endpoints

### Blog Generation

#### POST /api/generate-blog
Generate a blog post about a topic.

**Request:**
```json
{
  "topic": "How to build serverless applications",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Blog post generated successfully",
  "data": {
    "success": true,
    "content": "# How to Build Serverless Applications\n\n...",
    "meta": {
      "title": "How to Build Serverless Applications",
      "description": "Learn best practices for serverless development",
      "tags": ["serverless", "aws", "cloud"],
      "reading_time": 8,
      "word_count": 1600
    },
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  },
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

### Session Management

#### POST /api/session
Create a new session.

**Response:**
```json
{
  "status": "success",
  "message": "Session created successfully",
  "data": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2024-01-15T10:30:00.000000"
  },
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

#### GET /api/sessions
Retrieve all sessions.

#### GET /api/session/{session_id}
Retrieve a specific session.

#### DELETE /api/session/{session_id}
Delete a session.

### Health Check

#### GET /api/health
Check if the service is running.

## 🏗️ Code Organization

### Response Format

All API responses follow this structure:

```python
{
  "status": "success" | "error",
  "message": "Message",
  "data": <data>,
  "timestamp": "ISO 8601 timestamp"
}
```

## 🔧 Configuration

### Environment Variables

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_ENV=development

# Gemini API
GEMINI_API_KEY=your_key_here

# Tavily API
TAVILY_API_KEY=your_key_here

# Optional
DEBUG=True
APP_NAME=Blog Writer Agent
MIN_TOPIC_LENGTH=3
MIN_BLOG_WORD_COUNT=600
```

## 🔌 Integration Examples

### Using with cURL

```bash
# Generate a blog post
curl -X POST http://localhost:8000/api/generate-blog \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI and Machine Learning",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }'

# Create a session
curl -X POST http://localhost:8000/api/session \
  -H "Content-Type: application/json" \
  -d '{}'

# Check health
curl http://localhost:8000/api/health
```

### Using with Python

```python
import httpx
import asyncio

async def generate_blog():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/generate-blog",
            json={
                "topic": "FastAPI Best Practices",
                "session_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        )
        return response.json()

# Run
result = asyncio.run(generate_blog())
print(result)
```

### Using with JavaScript/Fetch

```javascript
async function generateBlog() {
  const response = await fetch('http://localhost:8000/api/generate-blog', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      topic: 'Next.js Best Practices',
      session_id: '550e8400-e29b-41d4-a716-446655440000'
    })
  });
  return response.json();
}

generateBlog().then(console.log);
```



## 🧪 Testing (Optional)

To add tests, create a `tests/` directory:

```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
```

Run tests with: `pytest`

## 📊 Performance Considerations

- **Caching**: API clients are cached as singletons
- **Concurrency**: Async/await throughout
- **Logging**: Minimal overhead logging
- **Error Handling**: Fails fast with clear errors
- **Timeouts**: Configurable LLM timeout

## 🔐 Security Notes

- Always use `.env` for sensitive keys (never commit)
- Validate all input with Pydantic
- Add authentication middleware for production
- Implement rate limiting
- Use HTTPS in production
- Escape user inputs in prompts

## 🐛 Troubleshooting

### "GEMINI_API_KEY not configured"
- Ensure `.env` file exists
- Add your Gemini API key to `.env`

### "Web search failed"
- Check Tavily API key in `.env`
- Verify internet connectivity

### Slow responses
- Gemini generation can take 10-30 seconds
- Consider adding request timeouts
- Check API rate limits from dashboard

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic V2 Docs](https://docs.pydantic.dev/latest/)
- [Google Generative AI Python SDK](https://github.com/google/generative-ai-python)
- [Tavily Python SDK](https://github.com/torantulino/tavily-python)

## 🌐 Live Demo & Blog Post

- **Live Preview**: https://contentagent.malahim.dev
- **Read the Full Story**: https://blog.malahim.dev/ai-agents/contentagent-i-built-a-multi-agent-blog-writer-in-a-day

Check out the blog post to learn how this multi-agent blog writer was built in a day!

## 👤 About

Built by [Malahim Haseeb](https://malahim.dev)

## 📝 License

This project is provided as-is for education and commercial use.

## 🤝 Contributing

Feel free to extend this backend with:
- Database persistence
- Authentication
- Caching layer
- Rate limiting
- Additional LLM models
- Custom prompt templates
- Session management
- Blog storage and retrieval
