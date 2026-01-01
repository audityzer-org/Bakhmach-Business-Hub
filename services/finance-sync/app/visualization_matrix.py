"""Visualization Matrix Template - Use-Case × Channel Mapping
Defines what data to include and how to render for each combination
"""
from typing import Set, Dict, List
from enum import Enum


class VisualizationMatrix:
    """
    Matrix defining field inclusion and rendering logic for:
    - Use-cases: presentation, documentation, dev, investor
    - Channels: web, xr, pdf, interactive
    """
    
    FIELD_REQUIREMENTS = {
        "presentation": {
            "web": {
                "node_fields": {"id", "name", "type", "color", "icon", "description"},
                "edge_fields": {"id", "source_id", "target_id", "label", "color"},
                "layer_fields": {"id", "name", "type", "color", "nodes"},
                "flow_fields": {"id", "name", "description", "edges", "color"},
                "rendering": {
                    "show_metadata": False,
                    "show_coordinates": True,
                    "animation": True,
                    "zoom_levels": [0.5, 1.0, 2.0],
                    "highlight_flows": True,
                    "interaction_level": "medium"
                }
            },
            "pdf": {
                "node_fields": {"id", "name", "type", "icon", "description"},
                "edge_fields": {"id", "source_id", "target_id", "label"},
                "layer_fields": {"id", "name", "type", "nodes"},
                "flow_fields": {"id", "name", "description", "edges"},
                "rendering": {
                    "page_layout": "landscape",
                    "resolution": 300,
                    "include_legend": True,
                    "page_breaks": True
                }
            }
        },
        "documentation": {
            "web": {
                "node_fields": {"id", "name", "type", "description", "metadata", "tags"},
                "edge_fields": {"id", "source_id", "target_id", "label", "metadata"},
                "layer_fields": {"id", "name", "type", "description", "nodes"},
                "flow_fields": {"id", "name", "description", "edges", "flow_type"},
                "rendering": {
                    "show_metadata": True,
                    "code_blocks": True,
                    "api_endpoints": True,
                    "table_format": "detailed"
                }
            }
        },
        "dev": {
            "web": {
                "node_fields": {"id", "name", "type", "description", "metadata", "tags"},
                "edge_fields": {"id", "source_id", "target_id", "label", "metadata"},
                "layer_fields": {"id", "name", "type", "description", "metadata"},
                "flow_fields": {"id", "name", "edges", "flow_type", "metadata"},
                "rendering": {
                    "show_metadata": True,
                    "show_ids": True,
                    "debug_mode": True,
                    "api_endpoints": True
                }
            }
        },
        "investor": {
            "web": {
                "node_fields": {"id", "name", "type", "description", "icon"},
                "edge_fields": {"id", "source_id", "target_id", "label"},
                "layer_fields": {"id", "name", "type", "nodes"},
                "flow_fields": {"id", "name", "edges"},
                "rendering": {
                    "minimalist": True,
                    "brand_colors": True,
                    "highlight_features": True,
                    "interaction_level": "low"
                }
            },
            "pdf": {
                "node_fields": {"id", "name", "type", "description"},
                "edge_fields": {"id", "source_id", "target_id", "label"},
                "layer_fields": {"id", "name", "type"},
                "flow_fields": {"id", "name"},
                "rendering": {
                    "format": "executive",
                    "page_limit": 10,
                    "high_level_only": True
                }
            }
        }
    }
    
    @staticmethod
    def get_fields_for_usecase_channel(
        usecase: str, 
        channel: str, 
        component_type: str
    ) -> Set[str]:
        """Get required fields for specific use-case and channel combination"""
        return VisualizationMatrix.FIELD_REQUIREMENTS.get(
            usecase, {}
        ).get(channel, {}).get(f"{component_type}_fields", set())
    
    @staticmethod
    def get_rendering_config(usecase: str, channel: str) -> Dict:
        """Get rendering configuration for use-case and channel"""
        return VisualizationMatrix.FIELD_REQUIREMENTS.get(
            usecase, {}
        ).get(channel, {}).get("rendering", {})
    
    @staticmethod
    def filter_fields(data: Dict, required_fields: Set[str]) -> Dict:
        """Filter dictionary to only include required fields"""
        return {k: v for k, v in data.items() if k in required_fields}
