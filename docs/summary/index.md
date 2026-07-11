# teslajsonpy Documentation Index

## For AI Assistants: How to Use This Documentation

This index is designed to help AI coding assistants quickly locate relevant information when answering questions about teslajsonpy. Each documentation file contains specific types of information organized for easy navigation.

### Quick Reference

- **Q: How do I use the library?** → See [interfaces.md](#interfaces-apis)
- **Q: What are the components?** → See [components.md](#components)
- **Q: How does authentication work?** → See [workflows.md](#workflows)
- **Q: What's the system design?** → See [architecture.md](#architecture)
- **Q: What classes/functions exist?** → See [components.md](#components)
- **Q: What data structures are used?** → See [data_models.md](#data-models)
- **Q: What are the dependencies?** → See [dependencies.md](#dependencies)

---

## Documentation Files

### codebase_info.md {#codebase-info}

**Purpose**: High-level overview and orientation guide

**Contains**:
- Project metadata (version, license, language)
- Codebase statistics and size
- Core architecture at 30,000 ft view
- Technology stack summary
- Key components list
- Supported features summary
- Architecture patterns overview
- Integration points
- Testing structure
- Development workflow
- File organization
- API design principles

**Use when**: Getting oriented, understanding project scope, explaining what the project does

**Key sections**:
- Codebase Statistics: Files, LOC, classes, functions
- Technology Stack: Dependencies table
- Key Components: Brief descriptions
- Architecture Patterns: Design approaches used
- File Organization: Directory structure

---

### architecture.md {#architecture}

**Purpose**: Detailed system design and how components interact

**Contains**:
- Layered architecture diagram
- Component responsibilities (detailed)
- Data flow patterns (user → controller → car → API)
- Command execution flow
- WebSocket flow
- Caching strategy details
- Error handling strategy
- Integration points with Home Assistant and Fleet API
- Performance considerations

**Use when**: Understanding how components fit together, debugging architectural issues, explaining system design

**Key diagrams**:
- Architecture Layers (mermaid)
- Component Interactions (mermaid)
- Vehicle Update Flow (sequence diagram)
- Command Execution Flow (sequence diagram)
- WebSocket Flow (sequence diagram)

**Key sections**:
- System Overview: Architecture diagram
- Component Responsibilities: Detailed for each component
- Data Flow Patterns: 3 key patterns with sequence diagrams
- Caching Strategy: Multi-level cache description
- Error Handling Strategy: Retry logic and error mapping
- Performance Considerations: Polling, batching, connections

---

### components.md {#components}

**Purpose**: Component API reference and interface documentation

**Contains**:
- 7 primary components detailed:
  1. Connection (HTTP/OAuth)
  2. Controller (orchestration)
  3. TeslaCar (vehicle model)
  4. EnergySite (energy models)
  5. Exceptions (error handling)
  6. TeslaProxy (OAuth proxy)
  7. Constants (configuration)
- For each: Responsibilities, key methods, state properties
- Class signatures
- Method signatures
- Polling strategy specifics
- Component dependencies

**Use when**: Need specific method signatures, understanding what a component does, finding which component to use

**Key sections**:
- For each component:
  - File location
  - Purpose
  - Scope (LOC)
  - Responsibilities (bullet points)
  - Key Classes (with code)
  - Key Methods (table format)
  - State (if applicable)

**Cross-references**:
- "See architecture.md for system design"
- "See interfaces.md for usage examples"

---

### interfaces.md {#interfaces-apis}

**Purpose**: Public API documentation with usage examples

**Contains**:
- Controller API (initialization, connection, vehicle management)
- Vehicle properties (read-only, organized by category)
- Vehicle commands (async methods, organized by feature)
- Energy site properties and commands
- Real-time updates (WebSocket)
- Data access methods (cached params)
- Connection API (low-level, for advanced use)
- Exception handling patterns
- Polling integration
- OAuth/token management
- Fleet API usage
- Typical usage pattern
- Import surface

**Use when**: Writing code to use the library, need examples, API reference, error handling

**Code examples**: Each section has practical examples

**Key sections**:
- Initialization: Connection setup
- Authentication: OAuth flow
- Vehicle Management: Getting and updating vehicles
- Vehicle Properties: Full list with types
- Vehicle Commands: Full list with parameter types
- Energy Sites: Properties and commands
- Real-Time Updates: WebSocket integration
- Data Access: Cached parameters

---

### data_models.md {#data-models}

**Purpose**: Data structure documentation - what data looks like

**Contains**:
- Vehicle root object structure
- Vehicle data structure (from `/vehicles/{id}/data`)
- Nested objects:
  - charge_state (battery/charging)
  - climate_state (temperature/HVAC)
  - drive_state (position/motion)
  - vehicle_state (doors/windows/physical state)
  - vehicle_config (capabilities)
  - gui_settings (display preferences)
- Energy data model
- Energy site data
- Command response structure
- OAuth token structure

**Use when**: Understanding data structure, debugging data parsing, working with raw API responses

**Format**: JSON structures with field descriptions, types, and value ranges

**Key sections**:
- Vehicle Data Model: All nested structures explained
- Energy Data Model: Solar/Powerwall data
- Command Response: Success/failure format
- OAuth Token: Token structure

---

### workflows.md {#workflows}

**Purpose**: Key processes, workflows, and usage patterns

**Contains**:
- 12 major workflows with diagrams and code:
  1. Initial Authentication (OAuth flow)
  2. Token Refresh (automatic expiration handling)
  3. Vehicle Discovery (finding cars)
  4. Vehicle State Polling (periodic updates)
  5. Command Execution (sending commands)
  6. WebSocket Real-Time Updates
  7. Climate Control (example workflow)
  8. Charging Sequence (start and monitor)
  9. Energy Site Monitoring
  10. Error Recovery (handling errors)
  11. Multi-Vehicle Coordination
  12. Scheduled Operations

**Use when**: Understanding typical usage patterns, learning how to build features, debugging workflow issues

**Format**: 
- Mermaid diagrams showing flow
- Code examples
- Detailed steps

**Key workflows**:
- Authentication: Step-by-step OAuth
- Polling: Interval selection logic
- Commands: Retry and wake logic
- WebSocket: Real-time message handling
- Error Recovery: Error → solution mappings

---

### dependencies.md {#dependencies}

**Purpose**: External dependencies and integrations

**Contains**:
- Runtime dependencies (8 packages, why chosen)
- Development dependencies (organized by category)
- External systems (Tesla API, OAuth, WebSocket)
- Fleet API (HTTP Proxy)
- Dependency graph (mermaid)
- Dependency compatibility
- Python version support
- Installation instructions
- Updating dependencies
- License compatibility
- Performance characteristics
- Troubleshooting

**Use when**: Understanding external libraries, dependency versions, integration points

**Key sections**:
- Runtime Dependencies: Table with why chosen
- External Systems: API endpoints and formats
- Dependency Graph: Visual relationships
- Optional Dependencies: Fleet API setup
- License Compatibility: License table

---

## Navigation Guide for Common Questions

### "How do I integrate this into my project?"

1. Start with **interfaces.md** - Typical usage pattern section
2. Reference **components.md** - Controller class
3. Look at **workflows.md** - Initial Authentication workflow

### "What's the data structure for vehicles?"

1. Go to **data_models.md** - Vehicle Data Model section
2. See specific nested objects (charge_state, climate_state, etc.)
3. Reference **interfaces.md** for property names on TeslaCar object

### "How does authentication work?"

1. Start with **architecture.md** - see Connection component
2. Go to **workflows.md** - Initial Authentication workflow (with diagram)
3. Reference **interfaces.md** - Authentication section
4. See **dependencies.md** - External Systems > OAuth

### "What commands can I send?"

1. Go to **interfaces.md** - Vehicle Commands section
2. Lists all 35+ commands organized by feature
3. Shows parameter types and return values
4. Reference **components.md** for TeslaCar class details

### "How does polling work?"

1. See **architecture.md** - Polling Strategy section
2. Reference **workflows.md** - Vehicle State Polling workflow
3. Look at **components.md** - Controller Polling Strategy subsection
4. See interval constants in **dependencies.md** - External Systems

### "How do I handle errors?"

1. Go to **architecture.md** - Error Handling Strategy
2. See **exceptions.md** in components.md for exception classes
3. Reference **workflows.md** - Error Recovery workflow
4. Look at **interfaces.md** - Exception Handling section

### "What are the key components?"

1. Start with **codebase_info.md** - Key Components table
2. Go to **components.md** for detailed information on each
3. See **architecture.md** for how they interact
4. Reference **dependencies.md** for inter-component dependencies

### "How do I enable real-time updates?"

1. See **workflows.md** - WebSocket Real-Time Updates
2. Go to **interfaces.md** - Real-Time Updates section
3. Reference **architecture.md** - WebSocket Flow diagram

### "What's the Fleet API support?"

1. See **dependencies.md** - Fleet API (HTTP Proxy) section
2. Reference **interfaces.md** - Fleet API usage section
3. Look at **architecture.md** - Integration Points

### "How do I set up development?"

1. See **codebase_info.md** - Development Workflow section
2. Reference **dependencies.md** - Development Installation
3. Look at original DEVELOPERS.md for contribution guidelines

---

## Cross-Reference Map

```
codebase_info.md
├── Technology Stack → dependencies.md
├── Key Components → components.md
├── Architecture → architecture.md
└── File Organization → components.md (directory structure)

architecture.md
├── Component Descriptions → components.md
├── Data Flow → workflows.md
├── External Systems → dependencies.md
└── Caching/Error Handling → components.md

components.md
├── Classes → interfaces.md (usage examples)
├── Methods → interfaces.md (API reference)
└── Architecture → architecture.md

interfaces.md
├── Data Structures → data_models.md
├── Authentication → workflows.md
├── Commands → components.md (TeslaCar)
└── Properties → data_models.md

data_models.md
├── Vehicle Data → interfaces.md (TeslaCar properties)
├── Energy Data → interfaces.md (EnergySite properties)
└── Command Responses → workflows.md

workflows.md
├── OAuth Flow → interfaces.md (Authentication)
├── Polling → architecture.md (Polling Strategy)
├── Commands → components.md (TeslaCar.send_command)
└── Errors → architecture.md (Error Handling)

dependencies.md
├── External APIs → architecture.md (Integration Points)
├── Library Usage → components.md (specific components)
└── Installation → codebase_info.md (Development Workflow)
```

---

## Documentation Statistics

| File | Purpose | Sections | Length |
|------|---------|----------|--------|
| codebase_info.md | Orientation & overview | 15 | 251 lines |
| architecture.md | System design | 12 | 421 lines |
| components.md | Component reference | 10 | 555 lines |
| interfaces.md | Public API & examples | 14 | 460 lines |
| data_models.md | Data structures | 8 | 551 lines |
| workflows.md | Usage patterns | 12 | 565 lines |
| dependencies.md | External integrations | 14 | 387 lines |
| **Total** | | **85** | **3,190 lines** |

---

## Key Concepts by Category

### Authentication & Security
- **Files**: workflows.md (Auth flow), components.md (Connection), interfaces.md (OAuth setup)
- **Key concepts**: OAuth2 PKCE, token refresh, authorization code flow
- **Usage**: See Initial Authentication workflow in workflows.md

### Vehicle Control
- **Files**: interfaces.md (Commands), components.md (TeslaCar), workflows.md (Command Execution)
- **Key concepts**: 35+ command methods, async/await, retry logic
- **Usage**: See Vehicle Commands in interfaces.md

### Vehicle State
- **Files**: data_models.md (structures), interfaces.md (properties), architecture.md (caching)
- **Key concepts**: 100+ read-only properties, caching, polling
- **Usage**: See Vehicle Properties in interfaces.md

### Polling & Updates
- **Files**: architecture.md (strategy), workflows.md (polling loop), components.md (Controller)
- **Key concepts**: Adaptive intervals, WebSocket real-time, caching
- **Usage**: See Vehicle State Polling in workflows.md

### Energy Systems
- **Files**: interfaces.md (Energy Site API), data_models.md (Energy Data), components.md (EnergySite)
- **Key concepts**: Solar/Powerwall/combined sites, power monitoring, configuration
- **Usage**: See Energy Site Monitoring in workflows.md

### Error Handling
- **Files**: architecture.md (strategy), workflows.md (recovery), components.md (Exceptions)
- **Key concepts**: Retry decorators, error codes, vehicle wake-up
- **Usage**: See Error Recovery in workflows.md

---

## Tips for Effective Navigation

1. **Start with use cases**: Read relevant workflow first
2. **Then go to API**: Reference interfaces.md for specific calls
3. **Check data**: See data_models.md for structure
4. **Understand design**: Consult architecture.md for "why"
5. **See examples**: All workflows.md sections have code

2. **For debugging**:
   - Data format issues → data_models.md
   - Wrong endpoint → interfaces.md or dependencies.md
   - Integration problems → architecture.md
   - Dependency issues → dependencies.md

3. **For implementation**:
   - Feature: workflow template in workflows.md
   - API details: interfaces.md + components.md
   - Error cases: architecture.md + workflows.md

---

## Version & Updates

- **Documentation Generated**: July 11, 2026
- **teslajsonpy Version**: 3.13.2
- **Documentation Status**: Complete coverage of all components
- **Last Updated**: Aligned with current codebase

This documentation provides comprehensive coverage for implementing, integrating, and maintaining teslajsonpy applications.
