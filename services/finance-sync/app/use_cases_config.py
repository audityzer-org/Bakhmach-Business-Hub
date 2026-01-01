"""Use-Cases Configuration with enabledLayers
Defines which layers are active by default for each visualization channel
Includes concrete examples for Monobank Finance Sync Service
"""
from typing import List, Dict, Set
from dataclasses import dataclass
from architecture_models import UseCase, ChannelType, ArchitectureModel, Layer, BaseNode, Edge, Flow


@dataclass
class UseCaseConfig:
    """Configuration for a specific use-case"""
    use_case: UseCase
    enabled_layers: Dict[ChannelType, Set[str]]  # channel -> layer_ids
    metadata: Dict = None
    
    def get_enabled_layers(self, channel: ChannelType) -> Set[str]:
        """Get enabled layer IDs for specific channel"""
        return self.enabled_layers.get(channel, set())


# ===== CONCRETE EXAMPLE: MONOBANK FINANCE SYNC ARCHITECTURE =====

MONOBANK_ARCHITECTURE = ArchitectureModel(
    id="monobank-sync-v1",
    name="Monobank Finance Sync Service",
    description="Complete architecture for Monobank API integration and financial data synchronization",
    version="1.0.0",
    stack=["Python", "FastAPI", "SQLite", "MongoDB", "Monobank API", "asyncio"],
    tags=["finance", "banking", "api-integration", "sync-service"]
)

# Layer definitions for Monobank architecture
LAYERS_CONFIG = {
    "api_layer": {
        "id": "api_layer",
        "name": "API Layer",
        "type": "api",
        "description": "REST API endpoints for client interactions",
        "depth": 0,
        "color": "#3498db",
        "nodes": [
            {"id": "sync_endpoint", "name": "POST /sync", "type": "endpoint"},
            {"id": "transactions_endpoint", "name": "GET /transactions", "type": "endpoint"},
            {"id": "balance_endpoint", "name": "GET /balance", "type": "endpoint"},
        ]
    },
    "auth_layer": {
        "id": "auth_layer",
        "name": "Authentication Layer",
        "type": "auth",
        "description": "JWT token validation and authorization",
        "depth": 1,
        "color": "#e74c3c",
        "nodes": [
            {"id": "jwt_validator", "name": "JWT Validator", "type": "component"},
            {"id": "token_manager", "name": "Token Manager", "type": "component"},
        ]
    },
    "service_layer": {
        "id": "service_layer",
        "name": "Service Layer",
        "type": "service",
        "description": "Business logic and orchestration",
        "depth": 2,
        "color": "#f39c12",
        "nodes": [
            {"id": "sync_service", "name": "SyncService", "type": "service"},
            {"id": "monobank_client", "name": "MonobankClient", "type": "service"},
            {"id": "data_processor", "name": "DataProcessor", "type": "service"},
        ]
    },
    "integration_layer": {
        "id": "integration_layer",
        "name": "Integration Layer",
        "type": "integration",
        "description": "External API integrations",
        "depth": 3,
        "color": "#9b59b6",
        "nodes": [
            {"id": "monobank_api", "name": "Monobank API", "type": "external_api"},
        ]
    },
    "database_layer": {
        "id": "database_layer",
        "name": "Database Layer",
        "type": "database",
        "description": "Data persistence",
        "depth": 4,
        "color": "#1abc9c",
        "nodes": [
            {"id": "accounting_db", "name": "Accounting DB (SQLite)", "type": "database"},
            {"id": "cache_db", "name": "Cache (Redis)", "type": "cache"},
        ]
    },
}

# Use-case configurations
PRESENTATION_CONFIG = UseCaseConfig(
    use_case=UseCase.PRESENTATION,
    enabled_layers={
        ChannelType.WEB_VIEW: {"api_layer", "service_layer", "integration_layer", "database_layer"},
        ChannelType.PDF: {"api_layer", "service_layer", "database_layer"},
    }
)

DOCUMENTATION_CONFIG = UseCaseConfig(
    use_case=UseCase.DOCUMENTATION,
    enabled_layers={
        ChannelType.WEB_VIEW: {
            "api_layer", "auth_layer", "service_layer",
            "integration_layer", "database_layer"
        },
        ChannelType.PDF: {
            "api_layer", "auth_layer", "service_layer",
            "integration_layer", "database_layer"
        },
    }
)

DEVELOPER_CONFIG = UseCaseConfig(
    use_case=UseCase.DEVELOPER_REVIEW,
    enabled_layers={
        ChannelType.WEB_VIEW: {
            "api_layer", "auth_layer", "service_layer",
            "integration_layer", "database_layer"
        },
        ChannelType.INTERACTIVE: {
            "api_layer", "auth_layer", "service_layer",
            "integration_layer", "database_layer"
        },
    }
)

INVESTOR_CONFIG = UseCaseConfig(
    use_case=UseCase.INVESTOR_PITCH,
    enabled_layers={
        ChannelType.WEB_VIEW: {"api_layer", "service_layer", "integration_layer"},
        ChannelType.PDF: {"api_layer", "service_layer", "integration_layer"},
    }
)

# Registry of all use-case configurations
USE_CASE_REGISTRY = {
    UseCase.PRESENTATION: PRESENTATION_CONFIG,
    UseCase.DOCUMENTATION: DOCUMENTATION_CONFIG,
    UseCase.DEVELOPER_REVIEW: DEVELOPER_CONFIG,
    UseCase.INVESTOR_PITCH: INVESTOR_CONFIG,
}


def get_config(use_case: UseCase) -> UseCaseConfig:
    """Get configuration for specific use-case"""
    return USE_CASE_REGISTRY.get(use_case)


def get_enabled_layers_for_channel(
    use_case: UseCase,
    channel: ChannelType
) -> Set[str]:
    """Get enabled layer IDs for use-case and channel combination"""
    config = get_config(use_case)
    if config:
        return config.get_enabled_layers(channel)
    return set()
