from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class BlogMeta(BaseModel):

    title: str = Field(..., description="Blog post title")
    description: str = Field(..., description="SEO meta description")
    tags: List[str] = Field(default_factory=list, description="Blog tags")
    reading_time: int = Field(..., description="Reading time in minutes")
    word_count: int = Field(..., description="Total word count")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "How to Build a Blog Writing Agent",
                "description": "Learn how to create an AI-powered blog writing system",
                "tags": ["ai", "automation", "blog", "langgraph"],
                "reading_time": 5,
                "word_count": 1200
            }
        }


class AgentState(BaseModel):

    topic: str
    session_id: str
    search_results: List[str] = Field(default_factory=list)
    needs_search: bool = True
    draft: str = ""
    final_blog: str = ""
    meta: Optional[BlogMeta] = None
    error: Optional[str] = None


class GenerateBlogRequest(BaseModel):

    topic: str = Field(..., min_length=3, max_length=500, description="Blog topic")
    session_id: str = Field(..., description="Session ID")

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "How to build serverless applications",
                "session_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class CreateSessionRequest(BaseModel):

    pass


class SessionInfo(BaseModel):

    session_id: str = Field(..., description="Unique session ID")
    title: str = Field(..., description="Session title")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: datetime = Field(..., description="Last update time")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Blog Writing Session",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:35:00Z"
            }
        }


class GenerateBlogResponse(BaseModel):

    success: bool = Field(..., description="Operation success status")
    content: Optional[str] = Field(None, description="Generated blog content")
    meta: Optional[BlogMeta] = Field(None, description="Blog metadata")
    session_id: str = Field(..., description="Session ID")
    error: Optional[str] = Field(None, description="Error message if failed")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "content": "# How to Build Serverless Apps\n\n...",
                "meta": {
                    "title": "How to Build Serverless Applications",
                    "description": "Learn best practices for serverless development",
                    "tags": ["serverless", "aws", "cloud"],
                    "reading_time": 8,
                    "word_count": 1600
                },
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "error": None
            }
        }


class CreateSessionResponse(BaseModel):

    session_id: str = Field(..., description="New session ID")
    created_at: datetime = Field(..., description="Creation time")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "created_at": "2024-01-15T10:30:00Z"
            }
        }
