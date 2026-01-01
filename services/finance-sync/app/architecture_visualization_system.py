"""Augmented Architecture Visualization System
Comprehensive visualization generator for complex architecture across multiple channels.
Channels: Web (interactive), XR (immersive), PDF (documentation), Presentation
"""

from typing import Dict, List, Any, Optional, Tuple, Callable, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
import json
from datetime import datetime
from abc import ABC, abstractmethod


# ===== DATA MODELS =====

class LayerType(Enum):
    """Architecture layer classification"""
    PRESENTATION = "presentation"
    APPLICATION = "application"
    DOMAIN = "domain"
    INFRASTRUCTURE = "infrastructure"
    DATA = "data"
    EXTERNAL = "external"


class ChannelType(Enum):
    """Supported visualization channels"""
    WEB = "web"
    XR = "xr"
    PDF = "pdf"
    PRESENTATION = "presentation"
    DEV_REVIEW = "dev_review"


class UseCaseType(Enum):
    """Use case categories"""
    INVESTOR_PITCH = "investor_pitch"
    TECHNICAL_REVIEW = "technical_review"
    PRODUCT_OVERVIEW = "product_overview"
    DOCUMENTATION = "documentation"
    TRAINING = "training"


@dataclass
class Node:
    """Architecture node (component, service, domain)"""
    id: str
    label: str
    layer: LayerType
    description: str
    details: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    icon: Optional[str] = None
    color: Optional[str] = None
    url: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Edge:
    """Connection between nodes"""
    id: str
    source: str
    target: str
    relationship: str
    weight: float = 1.0
    label: Optional[str] = None
    description: Optional[str] = None
    data_flow: Optional[str] = None
    protocol: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Layer:
    """Architecture layer container"""
    type: LayerType
    nodes: List[Node] = field(default_factory=list)
    description: str = ""
    responsibilities: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "nodes": [node.to_dict() for node in self.nodes],
            "description": self.description,
            "responsibilities": self.responsibilities
        }


@dataclass
class ArchitectureModel:
    """Complete architecture model with layers and connections"""
    id: str
    name: str
    description: str
    nodes: List[Node] = field(default_factory=list)
    edges: List[Edge] = field(default_factory=list)
    layers: List[Layer] = field(default_factory=list)
    key_domains: List[str] = field(default_factory=list)
    tech_stack: Dict[str, List[str]] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "layers": [layer.to_dict() for layer in self.layers],
            "key_domains": self.key_domains,
            "tech_stack": self.tech_stack,
            "metrics": self.metrics,
            "timestamp": self.timestamp
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# ===== RENDERING TEMPLATES =====

class RenderingTemplate(ABC):
    """Base class for rendering templates"""
    
    @abstractmethod
    def render(self, model: ArchitectureModel) -> Any:
        pass


class WebRenderingTemplate(RenderingTemplate):
    """Web-based interactive visualization"""
    
    def render(self, model: ArchitectureModel) -> Dict[str, Any]:
        return {
            "format": "html",
            "engine": "d3.js",
            "interactive": True,
            "features": [
                "zoom_pan",
                "hover_details",
                "search",
                "filter_by_layer",
                "export_svg"
            ],
            "model": model.to_dict()
        }


class XRRenderingTemplate(RenderingTemplate):
    """XR (VR/AR) immersive visualization"""
    
    def render(self, model: ArchitectureModel) -> Dict[str, Any]:
        return {
            "format": "glb_gltf",
            "engine": "three.js",
            "immersive": True,
            "features": [
                "3d_navigation",
                "spatial_audio",
                "gesture_control",
                "teleportation",
                "annotations"
            ],
            "model": model.to_dict()
        }


class PDFRenderingTemplate(RenderingTemplate):
    """PDF documentation rendering"""
    
    def render(self, model: ArchitectureModel) -> Dict[str, Any]:
        return {
            "format": "pdf",
            "engine": "reportlab",
            "sections": [
                "executive_summary",
                "architecture_diagram",
                "component_specs",
                "data_flows",
                "technology_stack",
                "deployment_guide"
            ],
            "model": model.to_dict()
        }


class PresentationTemplate(RenderingTemplate):
    """Presentation slide generation"""
    
    def render(self, model: ArchitectureModel) -> Dict[str, Any]:
        return {
            "format": "pptx",
            "engine": "python-pptx",
            "slides": [
                {"type": "title", "title": model.name},
                {"type": "overview", "content": model.description},
                {"type": "architecture_diagram"},
                {"type": "key_domains"},
                {"type": "tech_stack"},
                {"type": "deployment"},
                {"type": "q_and_a"}
            ],
            "model": model.to_dict()
        }

# ===== USE-CASE × CHANNEL MATRIX =====

class UsesCaseChannelMatrix:
    """Matrix defining which fields and rendering options for use-case × channel combinations"""
    
    # Define what fields are included for each use-case × channel combination
    MATRIX = {
        UseCaseType.INVESTOR_PITCH: {
            ChannelType.WEB: {
                "fields": ["name", "description", "key_domains", "tech_stack", "metrics"],
                "rendering": "simplified_diagram",
                "emphasis": ["business_value", "market_position"],
                "exclude": ["technical_details", "data_models"],
                "color_scheme": "corporate"
            },
            ChannelType.PRESENTATION: {
                "fields": ["name", "description", "key_domains", "metrics"],
                "rendering": "executive_summary",
                "emphasis": ["roi", "competitive_advantage"],
                "exclude": ["implementation_details"],
                "color_scheme": "corporate"
            },
            ChannelType.PDF: {
                "fields": ["name", "description", "key_domains", "tech_stack"],
                "rendering": "formal_document",
                "sections": ["executive_summary", "business_case", "market_analysis"],
                "color_scheme": "professional"
            }
        },
        UseCaseType.TECHNICAL_REVIEW: {
            ChannelType.WEB: {
                "fields": ["all"],
                "rendering": "detailed_diagram",
                "emphasis": ["data_flows", "component_interactions"],
                "include_details": True,
                "color_scheme": "technical"
            },
            ChannelType.DEV_REVIEW: {
                "fields": ["nodes", "edges", "layers", "metrics"],
                "rendering": "code_review_diagram",
                "include_code_references": True,
                "color_scheme": "developer"
            },
            ChannelType.XR: {
                "fields": ["all"],
                "rendering": "3d_spatial_diagram",
                "include_annotations": True,
                "color_scheme": "technical"
            }
        },
        UseCaseType.PRODUCT_OVERVIEW: {
            ChannelType.WEB: {
                "fields": ["name", "description", "key_domains"],
                "rendering": "interactive_overview",
                "emphasis": ["user_journeys", "feature_highlights"],
                "color_scheme": "product"
            },
            ChannelType.PRESENTATION: {
                "fields": ["name", "description", "key_domains", "tech_stack"],
                "rendering": "feature_slides",
                "include_animations": True,
                "color_scheme": "product"
            }
        },
        UseCaseType.DOCUMENTATION: {
            ChannelType.PDF: {
                "fields": ["all"],
                "rendering": "comprehensive_guide",
                "sections": ["overview", "architecture", "components", "apis", "deployment"],
                "color_scheme": "documentation"
            },
            ChannelType.WEB: {
                "fields": ["all"],
                "rendering": "searchable_wiki",
                "include_examples": True,
                "color_scheme": "documentation"
            }
        }
    }
    
    @classmethod
    def get_render_config(cls, use_case: UseCaseType, channel: ChannelType) -> Dict[str, Any]:
        """Get rendering configuration for a specific use-case × channel combination"""
        if use_case in cls.MATRIX and channel in cls.MATRIX[use_case]:
            return cls.MATRIX[use_case][channel]
        return {"error": f"No configuration for {use_case} × {channel}"}


# ===== RENDERER ENGINE =====

class ArchitectureRenderer:
    """Main renderer that applies use-case × channel configurations"""
    
    def __init__(self):
        self.templates = {
            ChannelType.WEB: WebRenderingTemplate(),
            ChannelType.XR: XRRenderingTemplate(),
            ChannelType.PDF: PDFRenderingTemplate(),
            ChannelType.PRESENTATION: PresentationTemplate()
        }
    
    def render(self, model: ArchitectureModel, use_case: UseCaseType, 
               channel: ChannelType) -> Dict[str, Any]:
        """Render architecture with specific use-case and channel"""
        
        # Get configuration from matrix
        config = UsesCaseChannelMatrix.get_render_config(use_case, channel)
        
        # Get appropriate template
        template = self.templates.get(channel)
        if not template:
            return {"error": f"No template for channel {channel}"}
        
        # Apply configuration to model
        filtered_model = self._apply_config(model, config)
        
        # Render using template
        return {
            "use_case": use_case.value,
            "channel": channel.value,
            "config": config,
            "output": template.render(filtered_model)
        }
    
    def _apply_config(self, model: ArchitectureModel, config: Dict[str, Any]) -> ArchitectureModel:
        """Apply configuration to filter and transform model"""
        # Implementation would filter fields based on config
        return model


# ===== SIMPLIFIED SCHEMA VARIANT =====

@dataclass
class SimplifiedArchitectureModel:
    """Compact variant of ArchitectureModel for lightweight use cases"""
    id: str
    name: str
    description: str
    components: Dict[str, str]  # {component_name: brief_description}
    connections: List[Tuple[str, str, str]]  # [(source, target, relationship)]
    domains: List[str]
    tech_stack: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "components": self.components,
            "connections": self.connections,
            "domains": self.domains,
            "tech_stack": self.tech_stack
        }


# ===== DOMAIN-SPECIFIC RENDERERS =====

class FinanceDomainRenderer:
    """Specialized renderer for finance/banking domain (Monobank integration)"""
    
    FINANCE_SPECIFIC_FIELDS = {
        "transaction_flows": "Real-time transaction processing",
        "settlement": "Trade settlement and clearing",
        "reconciliation": "Account reconciliation",
        "compliance": "Regulatory compliance tracking",
        "audit_trails": "Complete transaction audit trails",
        "forex_integration": "Currency exchange rates",
        "liquidity_management": "Cash flow optimization",
        "risk_assessment": "Financial risk metrics"
    }
    
    def render(self, model: ArchitectureModel) -> Dict[str, Any]:
        """Render architecture with finance-specific emphasis"""
        return {
            "domain": "finance",
            "specialized_fields": self.FINANCE_SPECIFIC_FIELDS,
            "emphasis_nodes": self._identify_finance_nodes(model),
            "data_flows": self._extract_finance_flows(model),
            "compliance_nodes": self._identify_compliance_nodes(model)
        }
    
    def _identify_finance_nodes(self, model: ArchitectureModel) -> List[str]:
        return [n.id for n in model.nodes if "finance" in n.tags or "payment" in n.tags]
    
    def _extract_finance_flows(self, model: ArchitectureModel) -> List[Dict[str, Any]]:
        return [
            {"from": e.source, "to": e.target, "data": e.data_flow}
            for e in model.edges if e.data_flow and "transaction" in e.data_flow
        ]
    
    def _identify_compliance_nodes(self, model: ArchitectureModel) -> List[str]:
        return [n.id for n in model.nodes if "compliance" in n.tags or "audit" in n.tags]


# ===== EXAMPLE USAGE =====

if __name__ == "__main__":
    # Create a sample architecture model
    finance_model = ArchitectureModel(
        id="monobank-integration",
        name="Monobank Finance Sync System",
        description="Real-time financial data synchronization from Monobank API",
        key_domains=["payments", "transactions", "reconciliation", "reporting"],
        tech_stack={
            "backend": ["Python", "FastAPI", "PostgreSQL"],
            "integrations": ["Monobank API", "WebSocket"],
            "frontend": ["React", "D3.js"],
            "deployment": ["Docker", "Kubernetes"]
        }
    )
    
    # Create renderer
    renderer = ArchitectureRenderer()
    
    # Render for investor pitch on web
    investor_web = renderer.render(
        finance_model,
        UseCaseType.INVESTOR_PITCH,
        ChannelType.WEB
    )
    
    # Render for technical review
    tech_review = renderer.render(
        finance_model,
        UseCaseType.TECHNICAL_REVIEW,
        ChannelType.DEV_REVIEW
    )
    
    # Finance domain specific rendering
    finance_renderer = FinanceDomainRenderer()
    finance_focused = finance_renderer.render(finance_model)
    
    print("Architecture Visualization System initialized successfully")
    print(f"Model: {finance_model.name}")
    print(f"Available renderers: Web, XR, PDF, Presentation")
    print(f"Use-cases: {', '.join([uc.value for uc in UseCaseType])}")
