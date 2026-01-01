"""Rendering Engines for Different Output Channels
Converts architecture models to different formats
"""
from typing import Dict, Any
import json
from architecture_models import ArchitectureModel, UseCase, ChannelType
from visualization_matrix import VisualizationMatrix
from use_cases_config import get_enabled_layers_for_channel


class BaseRenderer:
    """Base renderer interface"""
    
    def render(self, arch: ArchitectureModel, use_case: UseCase, channel: ChannelType) -> Any:
        raise NotImplementedError


class JSONRenderer(BaseRenderer):
    """Renders architecture as JSON"""
    
    def render(self, arch: ArchitectureModel, use_case: UseCase, channel: ChannelType) -> str:
        """Render architecture as formatted JSON"""
        enabled_layers = get_enabled_layers_for_channel(use_case, channel)
        
        filtered_layers = [
            layer for layer in arch.layers
            if layer.id in enabled_layers
        ]
        
        data = {
            "architecture": {
                "id": arch.id,
                "name": arch.name,
                "version": arch.version,
                "layers": [layer.model_dump() for layer in filtered_layers],
                "nodes": [node.model_dump() for node in arch.nodes],
                "edges": [edge.model_dump() for edge in arch.edges],
            },
            "metadata": {
                "use_case": use_case.value,
                "channel": channel.value,
            }
        }
        
        return json.dumps(data, default=str, indent=2)


class WebHTMLRenderer(BaseRenderer):
    """Renders architecture as interactive HTML for web"""
    
    def render(self, arch: ArchitectureModel, use_case: UseCase, channel: ChannelType) -> str:
        """Render architecture as HTML"""
        enabled_layers = get_enabled_layers_for_channel(use_case, channel)
        config = VisualizationMatrix.get_rendering_config(use_case.value, channel.value)
        
        filtered_layers = [
            layer for layer in arch.layers
            if layer.id in enabled_layers
        ]
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{arch.name} - Architecture Visualization</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .layer {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .node {{ margin: 10px; padding: 10px; background: {config.get('node_color', '#e8f4f8')}; border-radius: 3px; }}
        h1 {{ color: #333; }}
    </style>
</head>
<body>
    <h1>{arch.name} (v{arch.version})</h1>
    <p>{arch.description}</p>
    <h2>Layers</h2>
"""
        
        for layer in filtered_layers:
            html += f'<div class="layer" style="background-color: {layer.color};">'  
            html += f'<h3>{layer.name}</h3>'
            html += f'<p>{layer.description}</p>'
            for node in layer.nodes:
                html += f'<div class="node">{node.name} ({node.type.value})</div>'
            html += '</div>'
        
        html += """</body>
</html>"""
        
        return html


class TextRenderer(BaseRenderer):
    """Renders architecture as plain text"""
    
    def render(self, arch: ArchitectureModel, use_case: UseCase, channel: ChannelType) -> str:
        """Render architecture as text"""
        enabled_layers = get_enabled_layers_for_channel(use_case, channel)
        
        text = f"\n{'='*60}\n"
        text += f"{arch.name} (v{arch.version})\n"
        text += f"{'='*60}\n\n"
        text += f"Description: {arch.description}\n\n"
        
        text += "LAYERS:\n"
        for layer in arch.layers:
            if layer.id in enabled_layers:
                text += f"  [{layer.type.value}] {layer.name}\n"
                text += f"    Description: {layer.description}\n"
                text += f"    Nodes: {len(layer.nodes)}\n"
                for node in layer.nodes:
                    text += f"      - {node.name} ({node.type.value})\n"
        
        text += f"\n{'='*60}\n"
        text += f"Use Case: {use_case.value}\n"
        text += f"Channel: {channel.value}\n"
        text += f"{'='*60}\n"
        
        return text


class RenderingEngine:
    """Main rendering engine that delegates to specific renderers"""
    
    def __init__(self):
        self.renderers = {
            ChannelType.WEB_VIEW: WebHTMLRenderer(),
            ChannelType.PDF: TextRenderer(),  # Can be upgraded to real PDF
            ChannelType.INTERACTIVE: JSONRenderer(),
            ChannelType.XR: JSONRenderer(),
        }
    
    def render(
        self,
        arch: ArchitectureModel,
        use_case: UseCase,
        channel: ChannelType,
        format: str = None
    ) -> str:
        """Render architecture using appropriate engine"""
        if format is None:
            format = channel.value
        
        if channel in self.renderers:
            renderer = self.renderers[channel]
            return renderer.render(arch, use_case, channel)
        
        # Default to JSON
        return JSONRenderer().render(arch, use_case, channel)
