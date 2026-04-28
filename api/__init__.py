from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from uuid import uuid4

from schemas import (
    GenerateBlogRequest,
    GenerateBlogResponse,
    CreateSessionRequest,
    CreateSessionResponse,
    SessionInfo,
    BlogMeta as SchemaBlogMeta,
)
from responses import APIResponse, StatusCode
from config import get_settings
from logger import setup_logger
from agent.graph import run_agent

logger = setup_logger(__name__)

router = APIRouter(prefix="/api", tags=["blog"])


@router.post("/session", response_model=APIResponse[CreateSessionResponse])
async def create_session(request: CreateSessionRequest):
    try:
        session_id = str(uuid4())
        response_data = CreateSessionResponse(
            session_id=session_id,
            created_at=datetime.utcnow()
        )
        logger.info(f"[API] Session created: {session_id}")
        return APIResponse.success(
            data=response_data,
            message="Session created successfully"
        )
    except Exception as e:
        logger.error(f"[API] Error creating session: {str(e)}")
        return APIResponse.error(
            message="Failed to create session",
            error=str(e),
            status=StatusCode.INTERNAL_ERROR
        )


@router.get("/sessions", response_model=APIResponse[list[SessionInfo]])
async def get_sessions():
    try:
        logger.info("[API] Retrieving sessions")
        return APIResponse.success(
            data=[],
            message="Sessions retrieved successfully"
        )
    except Exception as e:
        logger.error(f"[API] Error retrieving sessions: {str(e)}")
        return APIResponse.error(
            message="Failed to retrieve sessions",
            error=str(e),
            status=StatusCode.INTERNAL_ERROR
        )


@router.get("/session/{session_id}", response_model=APIResponse[dict])
async def get_session(session_id: str):
    try:
        logger.info(f"[API] Retrieving session: {session_id}")
        return APIResponse.success(
            data={"session_id": session_id, "messages": []},
            message="Session retrieved successfully"
        )
    except Exception as e:
        logger.error(f"[API] Error retrieving session {session_id}: {str(e)}")
        return APIResponse.error(
            message="Failed to retrieve session",
            error=str(e),
            status=StatusCode.NOT_FOUND
        )


@router.delete("/session/{session_id}", response_model=APIResponse[dict])
async def delete_session(session_id: str):
    try:
        logger.info(f"[API] Deleting session: {session_id}")
        return APIResponse.success(
            message="Session deleted successfully"
        )
    except Exception as e:
        logger.error(f"[API] Error deleting session {session_id}: {str(e)}")
        return APIResponse.error(
            message="Failed to delete session",
            error=str(e),
            status=StatusCode.INTERNAL_ERROR
        )


@router.post("/generate-blog", response_model=APIResponse[GenerateBlogResponse])
async def generate_blog(request: GenerateBlogRequest):
    try:
        settings = get_settings()
        topic = request.topic.strip()

        if len(topic) < settings.MIN_TOPIC_LENGTH:
            logger.warning(f"[API] Topic too short: {topic}")
            return APIResponse.error(
                message="Topic is too short",
                error=f"Topic must be at least {settings.MIN_TOPIC_LENGTH} characters",
                status=StatusCode.VALIDATION_ERROR
            )

        logger.info(f"[API] Generating blog for topic: '{topic}'")

        result = await run_agent(topic, request.session_id)

        if result.error and not result.final_blog:
            logger.error(f"[API] Blog generation failed: {result.error}")
            return APIResponse.error(
                message="Blog generation failed",
                error=result.error,
                status=StatusCode.INTERNAL_ERROR
            )

        meta_dict = None
        if result.meta:
            meta_dict = SchemaBlogMeta(
                title=result.meta.title,
                description=result.meta.description,
                tags=result.meta.tags,
                reading_time=result.meta.reading_time,
                word_count=result.meta.word_count,
            )

        response_data = GenerateBlogResponse(
            success=True,
            content=result.final_blog,
            meta=meta_dict,
            session_id=request.session_id,
            error=None,
        )

        logger.info(f"[API] Blog generated successfully ({result.meta.word_count if result.meta else 0} words)")
        return APIResponse.success(
            data=response_data,
            message="Blog post generated successfully"
        )

    except Exception as e:
        logger.error(f"[API] Unexpected error: {str(e)}")
        return APIResponse.error(
            message="Internal server error",
            error=str(e),
            status=StatusCode.INTERNAL_ERROR
        )


@router.get("/health", response_model=APIResponse[dict])
async def health_check():
    return APIResponse.success(
        data={"status": "ok"},
        message="Service is healthy"
    )
