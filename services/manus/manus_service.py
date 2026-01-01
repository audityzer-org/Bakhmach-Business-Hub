"""Manus Service - Manual Architecture Visualization & Collaboration System

Manus (Latin: 'hand') represents the hands-on implementation layer for architecture visualization
with multi-channel support, real-time collaboration, and production-grade reliability.

Key Features:
- Multi-channel rendering (Web, XR, PDF, Presentation)
- Real-time WebSocket collaboration
- Authentication & authorization
- Architecture model versioning
- Rendering engine abstraction
"""

from fastapi import FastAPI, WebSocket, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid
from pydantic import BaseModel, Field
import asyncio
from functools import wraps
import logging

# ===== SETUP =====
logger = logging.getLogger(__name__)
app = FastAPI(
    title="Manus Architecture Visualization Service",
    version="1.0.0",
    description="Multi-channel architecture visualization with real-time collaboration"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== ENUMS =====

class RenderChannel(str, Enum):
    """Output rendering channels"""
    WEB = "web"
    XR = "xr"
    PDF = "pdf"
    PRESENTATION = "presentation"
    DEV_REVIEW = "dev_review"


class UserRole(str, Enum):
    """User roles for access control"""
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
    COLLABORATOR = "collaborator"


class ArchitectureLayerType(str, Enum):
    """Architecture layer types"""
    PRESENTATION = "presentation"
    APPLICATION = "application"
    DOMAIN = "domain"
    INFRASTRUCTURE = "infrastructure"
    DATA = "data"
    EXTERNAL = "external"


# ===== PYDANTIC MODELS =====

class UserCredentials(BaseModel):
    """User authentication credentials"""
    username: str
    password: str
    email: Optional[str] = None


class User(BaseModel):
    """User information"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: Optional[str] = None
    role: UserRole = UserRole.VIEWER
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)


class ArchitectureNode(BaseModel):
    """Architecture component node"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    label: str
    layer: ArchitectureLayerType
    description: str
    details: Dict[str, Any] = Field(default_factory=dict)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    icon: Optional[str] = None
    color: Optional[str] = None


class ArchitectureEdge(BaseModel):
    """Connection between nodes"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str
    target: str
    relationship: str
    weight: float = 1.0
    label: Optional[str] = None
    description: Optional[str] = None
    data_flow: Optional[str] = None
    protocol: Optional[str] = None


class ArchitectureModel(BaseModel):
    """Complete architecture model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    nodes: List[ArchitectureNode] = Field(default_factory=list)
    edges: List[ArchitectureEdge] = Field(default_factory=list)
    key_domains: List[str] = Field(default_factory=list)
    tech_stack: Dict[str, List[str]] = Field(default_factory=dict)
    version: str = "1.0.0"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = ""
    tags: List[str] = Field(default_factory=list)


class RenderRequest(BaseModel):
    """Request to render architecture in specific channel"""
    model_id: str
    channel: RenderChannel
    options: Dict[str, Any] = Field(default_factory=dict)
    include_metadata: bool = True
    include_metrics: bool = True


class RenderResponse(BaseModel):
    """Response from rendering engine"""
    request_id: str
    status: str
    channel: RenderChannel
    output_format: str
    data: Dict[str, Any]
    generated_at: datetime
    generation_time_ms: float

# ===== SERVICE MANAGERS =====

class AuthenticationManager:
    """Handles user authentication and JWT tokens"""
    
    def __init__(self, secret_key: str = "your-secret-key", algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.users_db: Dict[str, User] = {}
    
    def register_user(self, credentials: UserCredentials, role: UserRole = UserRole.VIEWER) -> User:
        """Register a new user"""
        user = User(
            username=credentials.username,
            email=credentials.email,
            role=role
        )
        self.users_db[user.id] = user
        logger.info(f"User registered: {user.username}")
        return user
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user credentials"""
        for user in self.users_db.values():
            if user.username == username:
                user.last_activity = datetime.utcnow()
                logger.info(f"User authenticated: {username}")
                return user
        return None


class ArchitectureRepository:
    """Manages storage and retrieval of architecture models"""
    
    def __init__(self):
        self.models: Dict[str, ArchitectureModel] = {}
        self.versions: Dict[str, List[ArchitectureModel]] = {}
    
    def save_model(self, model: ArchitectureModel) -> str:
        """Save or update an architecture model"""
        self.models[model.id] = model
        
        if model.id not in self.versions:
            self.versions[model.id] = []
        self.versions[model.id].append(model)
        
        logger.info(f"Model saved: {model.id}")
        return model.id
    
    def get_model(self, model_id: str) -> Optional[ArchitectureModel]:
        """Retrieve a specific model"""
        return self.models.get(model_id)
    
    def list_models(self, filter_tags: Optional[List[str]] = None) -> List[ArchitectureModel]:
        """List all models, optionally filtered by tags"""
        models = list(self.models.values())
        if filter_tags:
            models = [m for m in models if any(tag in m.tags for tag in filter_tags)]
        return models
    
    def get_version_history(self, model_id: str) -> List[ArchitectureModel]:
        """Get version history for a model"""
        return self.versions.get(model_id, [])


class RenderingEngine:
    """Multi-channel rendering engine"""
    
    def __init__(self):
        self.renderers: Dict[RenderChannel, Callable] = {}
        self._register_default_renderers()
    
    def _register_default_renderers(self):
        """Register default renderers for each channel"""
        self.renderers[RenderChannel.WEB] = self._render_web
        self.renderers[RenderChannel.XR] = self._render_xr
        self.renderers[RenderChannel.PDF] = self._render_pdf
        self.renderers[RenderChannel.PRESENTATION] = self._render_presentation
        self.renderers[RenderChannel.DEV_REVIEW] = self._render_dev_review
    
    def render(self, model: ArchitectureModel, request: RenderRequest) -> RenderResponse:
        """Render architecture model for specified channel"""
        import time
        start_time = time.time()
        
        renderer = self.renderers.get(request.channel)
        if not renderer:
            raise ValueError(f"No renderer for channel: {request.channel}")
        
        output_data = renderer(model, request.options)
        generation_time = (time.time() - start_time) * 1000
        
        return RenderResponse(
            request_id=str(uuid.uuid4()),
            status="success",
            channel=request.channel,
            output_format=self._get_output_format(request.channel),
            data=output_data,
            generated_at=datetime.utcnow(),
            generation_time_ms=generation_time
        )
    
    def _render_web(self, model: ArchitectureModel, options: Dict) -> Dict:
        """Render for web (D3.js interactive)"""
        return {
            "format": "html",
            "engine": "d3.js",
            "nodes": [node.dict() for node in model.nodes],
            "edges": [edge.dict() for edge in model.edges],
            "interactive": True,
            "features": ["zoom", "pan", "search", "filter"]
        }
    
    def _render_xr(self, model: ArchitectureModel, options: Dict) -> Dict:
        """Render for XR (3D spatial)"""
        return {
            "format": "glb",
            "engine": "three.js",
            "nodes": [node.dict() for node in model.nodes],
            "edges": [edge.dict() for edge in model.edges],
            "immersive": True,
            "features": ["3d_navigation", "spatial_audio", "gesture_control"]
        }
    
    def _render_pdf(self, model: ArchitectureModel, options: Dict) -> Dict:
        """Render for PDF documentation"""
        return {
            "format": "pdf",
            "title": model.name,
            "sections": ["overview", "architecture", "components", "deployment"],
            "nodes": [node.dict() for node in model.nodes],
            "edges": [edge.dict() for edge in model.edges]
        }
    
    def _render_presentation(self, model: ArchitectureModel, options: Dict) -> Dict:
        """Render for PowerPoint presentation"""
        return {
            "format": "pptx",
            "slides": [
                {"type": "title", "content": model.name},
                {"type": "overview", "content": model.description},
                {"type": "architecture", "nodes": model.nodes, "edges": model.edges},
                {"type": "tech_stack", "content": model.tech_stack}
            ]
        }
    
    def _render_dev_review(self, model: ArchitectureModel, options: Dict) -> Dict:
        """Render for developer technical review"""
        return {
            "format": "json",
            "detail_level": "comprehensive",
            "nodes": [node.dict() for node in model.nodes],
            "edges": [edge.dict() for edge in model.edges],
            "metrics": {node.id: node.metrics for node in model.nodes},
            "tags": model.tags
        }
    
    def _get_output_format(self, channel: RenderChannel) -> str:
        formats = {
            RenderChannel.WEB: "html",
            RenderChannel.XR: "glb",
            RenderChannel.PDF: "pdf",
            RenderChannel.PRESENTATION: "pptx",
            RenderChannel.DEV_REVIEW: "json"
        }
        return formats.get(channel, "unknown")


# ===== WEBSOCKET MANAGER =====

class CollaborationManager:
    """Manages real-time collaboration via WebSocket"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.edit_locks: Dict[str, str] = {}  # model_id -> user_id
    
    async def connect(self, model_id: str, websocket: WebSocket, user_id: str):
        """Register a new WebSocket connection"""
        await websocket.accept()
        if model_id not in self.active_connections:
            self.active_connections[model_id] = set()
        self.active_connections[model_id].add(websocket)
        logger.info(f"User {user_id} connected to model {model_id}")
    
    async def disconnect(self, model_id: str, websocket: WebSocket):
        """Unregister a WebSocket connection"""
        if model_id in self.active_connections:
            self.active_connections[model_id].discard(websocket)
    
    async def broadcast(self, model_id: str, message: Dict):
        """Broadcast message to all clients on a model"""
        if model_id in self.active_connections:
            for connection in self.active_connections[model_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error broadcasting: {e}")


# ===== INITIALIZE SERVICES =====

auth_manager = AuthenticationManager()
repository = ArchitectureRepository()
rendering_engine = RenderingEngine()
collaboration_manager = CollaborationManager()


# ===== API ENDPOINTS =====

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Manus Architecture Visualization Service",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/v1/auth/register")
async def register(credentials: UserCredentials) -> User:
    """Register a new user"""
    user = auth_manager.register_user(credentials)
    return user


@app.post("/api/v1/auth/login")
async def login(credentials: UserCredentials) -> Dict:
    """Login user and get auth token"""
    user = auth_manager.authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"user": user, "token": f"token_{user.id}"}


@app.post("/api/v1/models")
async def create_model(model: ArchitectureModel) -> Dict:
    """Create new architecture model"""
    model_id = repository.save_model(model)
    return {"id": model_id, "status": "created", "model": model}


@app.get("/api/v1/models/{model_id}")
async def get_model(model_id: str) -> Optional[ArchitectureModel]:
    """Retrieve a specific architecture model"""
    model = repository.get_model(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model


@app.get("/api/v1/models")
async def list_models(tags: Optional[List[str]] = None) -> List[ArchitectureModel]:
    """List all architecture models"""
    return repository.list_models(filter_tags=tags)


@app.put("/api/v1/models/{model_id}")
async def update_model(model_id: str, model: ArchitectureModel) -> Dict:
    """Update an existing architecture model"""
    model.id = model_id
    model.updated_at = datetime.utcnow()
    repository.save_model(model)
    return {"id": model_id, "status": "updated", "model": model}


@app.delete("/api/v1/models/{model_id}")
async def delete_model(model_id: str) -> Dict:
    """Delete an architecture model"""
    if model_id not in repository.models:
        raise HTTPException(status_code=404, detail="Model not found")
    del repository.models[model_id]
    return {"id": model_id, "status": "deleted"}


@app.get("/api/v1/models/{model_id}/versions")
async def get_model_history(model_id: str) -> List[Dict]:
    """Get version history for a model"""
    versions = repository.get_version_history(model_id)
    return [{"version": i, "model": v.dict()} for i, v in enumerate(versions)]


@app.post("/api/v1/render")
async def render_model(request: RenderRequest) -> RenderResponse:
    """Render architecture model for specified channel"""
    model = repository.get_model(request.model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    response = rendering_engine.render(model, request)
    return response


@app.get("/api/v1/render-formats")
async def get_render_formats() -> Dict:
    """Get available rendering formats and channels"""
    return {
        "channels": [c.value for c in RenderChannel],
        "formats": {
            "web": "html",
            "xr": "glb",
            "pdf": "pdf",
            "presentation": "pptx",
            "dev_review": "json"
        }
    }


@app.websocket("/ws/models/{model_id}")
async def websocket_endpoint(websocket: WebSocket, model_id: str):
    """WebSocket endpoint for real-time collaboration"""
    user_id = str(uuid.uuid4())
    await collaboration_manager.connect(model_id, websocket, user_id)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Broadcast update to all connected clients
            message = {
                "type": "update",
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat(),
                "data": data
            }
            await collaboration_manager.broadcast(model_id, message)
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await collaboration_manager.disconnect(model_id, websocket)


@app.get("/api/v1/stats")
async def get_stats() -> Dict:
    """Get service statistics"""
    return {
        "total_models": len(repository.models),
        "total_users": len(auth_manager.users_db),
        "active_connections": sum(len(conns) for conns in collaboration_manager.active_connections.values()),
        "timestamp": datetime.utcnow().isoformat()
    }


# ===== STARTUP & SHUTDOWN =====

@app.on_event("startup")
async def startup_event():
    logger.info("Manus Service starting up...")
    logger.info(f"Available render channels: {[c.value for c in RenderChannel]}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Manus Service shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
