# Comparison Report: Delegated CA Operational Guidelines vs. RFC 8181

## Executive Summary

This report analyzes the essential differences between our proposed "Operational Guidelines for RPKI Delegated Certification Authorities" and RFC 8181 "A Publication Protocol for the Resource Public Key Infrastructure (RPKI)", clarifying scope boundaries and complementary objectives.

## RFC 8181 Objectives and Scope

### Primary Objectives of RFC 8181

**RFC 8181 defines:**
1. **Publication Protocol Specification**: Technical protocol between RPKI CAs and Publication Servers
2. **Message Format Standards**: XML schema and message structures for publish/withdraw operations  
3. **Transport Mechanisms**: HTTPS-based protocol for secure communication
4. **Error Handling**: Standardized error codes and exception handling
5. **Security Framework**: Authentication and authorization mechanisms for publication operations

### Technical Scope of RFC 8181

**What RFC 8181 Covers:**
- Protocol message definitions (publish, withdraw, list, query)
- XML schema specifications for publication requests/responses
- HTTPS transport requirements and security considerations
- Publisher-server authentication mechanisms
- Error response formats and semantics
- Basic operational assumptions about CA-server relationships

**What RFC 8181 Does NOT Cover:**
- CA operational requirements or lifecycle management
- Publication server performance or availability standards
- Monitoring and alerting frameworks
- Registry operator oversight responsibilities
- Enforcement mechanisms for problematic CAs
- Community coordination and communication procedures

## Essential Differences Between Our Proposal and RFC 8181

### 1. Protocol vs. Operations Focus

| Aspect | RFC 8181 | Our Proposal |
|--------|----------|--------------|
| **Primary Focus** | Technical protocol specification | Operational guidelines and lifecycle management |
| **Target Audience** | Protocol implementers | CA operators, registry operators, ecosystem participants |
| **Scope** | Message formats and transport | End-to-end operational practices |
| **Abstraction Level** | Low-level technical details | High-level operational policies |

### 2. Lifecycle Coverage

| Lifecycle Phase | RFC 8181 Coverage | Our Proposal Coverage |
|----------------|-------------------|---------------------|
| **Pre-delegation** | Not addressed | Comprehensive requirements and validation |
| **Initial Setup** | Basic protocol handshake | Infrastructure readiness, monitoring setup |
| **Ongoing Operations** | Message exchange mechanics | Performance standards, publication discipline |
| **Problem Detection** | Protocol error handling | Behavioral monitoring, flapping detection |
| **Enforcement** | Not addressed | Progressive enforcement, revocation procedures |
| **Shutdown** | Not addressed | Graceful termination, migration support |

### 3. Stakeholder Responsibilities

**RFC 8181 Assumptions:**
- CAs and Publication Servers exist and are properly configured
- Publishers have appropriate credentials and authorization
- Basic operational competency is assumed

**Our Proposal Specifications:**
- Detailed requirements for CA infrastructure and monitoring
- Registry operator oversight and enforcement responsibilities  
- Community coordination and communication procedures
- Validator operator feedback mechanisms

### 4. Problem Domain Coverage

| Problem Category | RFC 8181 Approach | Our Proposal Approach |
|-----------------|-------------------|---------------------|
| **Dead CAs** | Protocol timeouts only | Comprehensive detection, notification, revocation |
| **Flapping CAs** | Not addressed | Behavioral analysis, circuit breakers, penalties |
| **Performance Issues** | Not addressed | Response time requirements, load management |
| **Publication Quality** | Message validation only | Content discipline, consistency requirements |
| **Ecosystem Impact** | Not considered | Validator burden, resource waste prevention |

## RFC 8181 Objectives We Don't Address

### 1. Technical Protocol Specifications

**Our proposal explicitly does NOT cover:**
- Message format definitions or XML schema modifications
- Protocol security mechanisms or authentication procedures  
- Transport layer specifications or HTTPS requirements
- Low-level error handling or exception processing
- Protocol versioning or compatibility considerations

**Rationale**: These are well-established technical standards that don't require operational guidance.

### 2. Implementation Details

**Areas left to RFC 8181 and implementers:**
- Software architecture decisions
- Database schema or storage implementations
- Specific cryptographic implementations
- Performance optimization techniques at the protocol level
- Backward compatibility mechanisms

### 3. Basic Protocol Mechanics

**Core RFC 8181 functions we assume work correctly:**
- publish/withdraw message processing
- List query operations and responses
- Authentication and authorization mechanisms
- Basic error reporting and handling
- Session management and connection handling

## Complementary Relationship

### How Our Proposal Builds on RFC 8181

**Our work assumes RFC 8181 compliance and adds:**
1. **Operational Layer**: Guidelines for using RFC 8181 effectively in production
2. **Quality Assurance**: Standards for ensuring RFC 8181 implementations serve ecosystem needs
3. **Lifecycle Management**: Comprehensive operational procedures around RFC 8181 usage
4. **Community Coordination**: Mechanisms for managing RFC 8181 deployments at scale

### Integration Points

**Where our proposal references RFC 8181:**
- Publisher repository synchronization procedures (Section 4.5 of publication-server-bcp)
- Authentication and authorization assumptions
- Basic protocol error handling expectations
- Message exchange patterns for operational procedures

**Where RFC 8181 implementations benefit from our guidelines:**
- Operational requirements inform implementation priorities
- Performance standards guide system design decisions
- Monitoring requirements influence logging and metrics design
- Lifecycle procedures inform feature development

## Recommendations

### 1. Clear Scope Boundaries
- **RFC 8181**: Protocol specification and technical standards
- **Our Proposal**: Operational guidelines and lifecycle management
- **Publication Server BCP**: Infrastructure best practices

### 2. Normative References
Our document should include RFC 8181 as a normative reference while clearly stating we don't modify or extend the protocol itself.

### 3. Implementation Coordination
CA and Publication Server implementers should consider both RFC 8181 technical requirements and our operational guidelines during system design.

### 4. Community Engagement
Present our work as complementing rather than competing with existing technical standards, showing how operational excellence enhances protocol effectiveness.

## Conclusion

Our proposed operational guidelines address a completely different layer of the RPKI ecosystem than RFC 8181. While RFC 8181 provides the essential technical foundation for CA-Publication Server communication, our work provides the operational framework for ensuring that communication serves the broader ecosystem effectively.

The two efforts are highly complementary:
- **RFC 8181** ensures CAs can technically publish objects
- **Our proposal** ensures CAs publish objects in ways that serve the ecosystem well
- **Together** they provide both technical capability and operational excellence

This clear differentiation allows us to proceed with confidence that we're addressing genuine gaps in RPKI operational guidance rather than duplicating existing technical standards.