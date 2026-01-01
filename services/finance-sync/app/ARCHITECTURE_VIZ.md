# Augmented Architecture Visualization System
## Monobank Finance Sync Service

### Overview

This comprehensive architecture visualization system enables multi-channel representation of complex software architectures. It supports presentation, documentation, developer review, and investor pitch scenarios across web, XR, PDF, and interactive formats.

### Components

#### 1. `architecture_models.py` - Core Data Models

**Purpose**: Defines Pydantic models for architecture visualization.

**Key Classes**:
- `BaseNode`: Represents services, endpoints, databases, and components
- `Edge`: Models connections and data flows between nodes
- `Layer`: Groups nodes into architectural layers (API, Service, Database, etc.)
- `Flow`: Represents sequences of operations (request/response/event)
- `ArchitectureModel`: Complete architecture with all components
- `VersionSnapshot`: Point-in-time architecture snapshot

**Enumerations**:
- `LayerType`: API, SERVICE, DATABASE, INTEGRATION, AUTHENTICATION, CACHE, QUEUE
- `NodeType`: SERVICE, ENDPOINT, DATABASE, QUEUE, EXTERNAL_API, CACHE, COMPONENT
- `UseCase`: PRESENTATION, DOCUMENTATION, DEVELOPER_REVIEW, INVESTOR_PITCH
- `ChannelType`: WEB_VIEW, XR, PDF, INTERACTIVE

#### 2. `visualization_matrix.py` - Use-Case × Channel Mapping

**Purpose**: Defines what data fields to include and how to render for each use-case and output channel combination.

**Matrix Structure**:
```
Use-Cases: presentation, documentation, dev, investor
Channels: web, xr, pdf, interactive
```

**Key Methods**:
- `get_fields_for_usecase_channel()`: Get required JSON fields
- `get_rendering_config()`: Get rendering parameters
- `filter_fields()`: Extract only relevant fields

**Example Configurations**:
- Presentation → Web: Shows UI-friendly fields, animations, minimal metadata
- Documentation → Web/PDF: Full details, code blocks, API endpoints
- Developer → Web/Interactive: Debug mode, all fields, real-time updates
- Investor → Web/PDF: High-level overview, minimalist design

#### 3. `versioning_system.py` - Independent Component Versioning

**Purpose**: Enables separate version control for architecture components (layers, flows, nodes, edges).

**Key Classes**:
- `ComponentChange`: Records individual changes (added/removed/modified)
- `ComponentVersion`: Single version of a component type
- `VersionHistory`: Complete version timeline for a component
- `ArchitectureVersionManager`: Manages all component versions and snapshots

**Features**:
- Semantic versioning (major.minor.patch)
- Change tracking with commit messages
- Ability to compare versions and retrieve change history
- Complete architecture snapshots at specific versions

#### 4. `use_cases_config.py` - Configuration & Examples

**Purpose**: Defines which layers are active for each use-case/channel combination.

**Monobank Architecture Example**:

```
API Layer (depth: 0)
  - POST /sync
  - GET /transactions
  - GET /balance

Authentication Layer (depth: 1)
  - JWT Validator
  - Token Manager

Service Layer (depth: 2)
  - SyncService
  - MonobankClient
  - DataProcessor

Integration Layer (depth: 3)
  - Monobank API

Database Layer (depth: 4)
  - Accounting DB (SQLite)
  - Cache (Redis)
```

**Use-Case Configurations**:

1. **PRESENTATION** (for sales/demos)
   - Web: All layers (API → Database)
   - PDF: Core layers only (API, Service, Database)

2. **DOCUMENTATION** (for developers)
   - Web: All layers including auth
   - PDF: All layers with detail

3. **DEVELOPER_REVIEW** (for engineering)
   - Web: All layers with debug info
   - Interactive: Real-time updates

4. **INVESTOR_PITCH** (for funding)
   - Web: High-level layers only
   - PDF: Executive summary

### Usage Examples

#### Create Architecture Model

```python
from architecture_models import ArchitectureModel, BaseNode, Layer, LayerType, NodeType

arch = ArchitectureModel(
    id="my-arch",
    name="My System",
    version="1.0.0",
    stack=["Python", "FastAPI", "PostgreSQL"]
)
```

#### Get Visualization Fields

```python
from visualization_matrix import VisualizationMatrix
from architecture_models import UseCase, ChannelType

fields = VisualizationMatrix.get_fields_for_usecase_channel(
    usecase="presentation",
    channel="web",
    component_type="node"
)
```

#### Track Versions

```python
from versioning_system import ArchitectureVersionManager, ComponentType

manager = ArchitectureVersionManager()
manager.create_snapshot(
    model=arch,
    version="1.0.0",
    author="John Doe",
    commit_message="Initial architecture"
)
```

#### Get Configuration

```python
from use_cases_config import get_enabled_layers_for_channel
from architecture_models import UseCase, ChannelType

layers = get_enabled_layers_for_channel(
    usecase=UseCase.PRESENTATION,
    channel=ChannelType.WEB_VIEW
)
```

### Features

✅ **Multi-Channel Rendering**: Web, XR, PDF, Interactive
✅ **Use-Case Driven**: Presentation, Documentation, Developer, Investor
✅ **Independent Versioning**: Separate version history for components
✅ **Field-Based Filtering**: Show only relevant data per channel
✅ **Concrete Examples**: Monobank Finance Sync Service
✅ **Type Safety**: Full Pydantic validation
✅ **Extensible**: Easy to add new layers, nodes, and flows

### Architecture for Monobank Finance Sync

**Tech Stack**: Python 3.9+, FastAPI, SQLite/MongoDB, Monobank API, asyncio

**Layers**:
1. **API Layer**: FastAPI REST endpoints
2. **Authentication**: JWT token validation
3. **Service Layer**: Business logic and orchestration
4. **Integration**: Monobank API client
5. **Database**: SQLite for accounting, optional MongoDB

### Files

- `architecture_models.py` (127 lines): Core data models
- `visualization_matrix.py` (122 lines): Use-case × channel matrix
- `versioning_system.py` (154 lines): Version management
- `use_cases_config.py` (163 lines): Configuration and examples
- `ARCHITECTURE_VIZ.md`: This documentation

### Next Steps

1. Implement rendering functions for each channel format
2. Create REST API endpoints to expose visualization
3. Build frontend visualizers for web and XR
4. Add PDF export functionality
5. Integrate with existing database.py and sync_service.py

### Author

Created as part of augmented architecture visualization for Bakhmach-Business-Hub.
