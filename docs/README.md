# Health Resilience Mapping API Documentation

Welcome to the Health Resilience Mapping API documentation. This API serves data about 1,059+ resilient communities across America with dignity and community-first principles.

## 🏘️ About the API

Our API provides access to:
- **Community Data**: Information about unexpectedly resilient communities
- **Community Stories**: Narratives shared with community approval  
- **Research Data**: Aggregated insights for academic research
- **Policy Information**: Data to inform evidence-based policy making

## 📚 API Documentation

### Swagger/OpenAPI Documentation

The complete API documentation is available via Swagger UI:

- **Local Development**: http://localhost:8080/docs
- **Production**: https://api.resilience-mapping.org/docs

### Key Endpoints

#### Health & Status
- `GET /health` - Basic health check
- `GET /health/ready` - Readiness check for Kubernetes
- `GET /health/metrics` - System metrics for monitoring
- `GET /health/status` - Comprehensive system status

#### Communities
- `GET /communities` - List public communities with filtering
- `GET /communities/{id}` - Get specific community details
- `GET /communities/{id}/stories` - Get stories for a community
- `GET /communities/search` - Search communities
- `GET /communities/nearby` - Find nearby communities
- `GET /communities/resilient` - Get unexpectedly resilient communities
- `GET /communities/stats` - Get community statistics

#### Stories
- `GET /stories` - List published stories
- `GET /stories/{id}` - Get specific story details

#### Search
- `GET /search` - Global search across all content

#### Authentication
- `POST /auth/register` - Register new user account
- `POST /auth/login` - Authenticate user

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## 📊 Rate Limiting

To protect community data and ensure reliable service:
- **Public endpoints**: 100 requests per minute per IP
- **Authenticated users**: 1000 requests per minute
- **Search endpoints**: 50 requests per minute per IP

## 🛡️ Privacy & Ethics

### Community-First Principles

This API was built with community dignity and consent at its core:

- **Privacy by Design**: Only public, community-approved data is accessible
- **Consent-Based Access**: Communities control their data sharing
- **Dignity-First Language**: All responses use asset-based, respectful language
- **Transparent Intent**: Clear documentation of data use and purpose

### Data Protection

- All personally identifiable information is protected
- Geographic data is generalized to protect individual privacy
- Community approval is required before any data sharing
- Researcher access requires data use agreements

## 🚀 Getting Started

### 1. Basic API Call

```bash
curl -X GET "https://api.resilience-mapping.org/health" \
  -H "accept: application/json"
```

### 2. Search Communities

```bash
curl -X GET "https://api.resilience-mapping.org/communities?resilient=true&limit=10" \
  -H "accept: application/json"
```

### 3. Search by Location

```bash
curl -X GET "https://api.resilience-mapping.org/communities/nearby?lat=40.7128&lng=-74.0060&radius=50" \
  -H "accept: application/json"
```

## 📖 Response Format

All API responses follow a consistent format:

### Success Response
```json
{
  "communities": [...],
  "total": 150,
  "message": "Celebrating resilient communities across America",
  "note": "Each community shown has given permission to share their story"
}
```

### Error Response
```json
{
  "error": "Technical error message",
  "community_message": "Community-friendly explanation of what happened",
  "timestamp": "2025-01-31T10:30:00Z"
}
```

## 🧪 Testing & Development

### Local Development

1. **Start the API server**:
   ```bash
   go run cmd/server/main.go
   ```

2. **Access Swagger UI**: 
   http://localhost:8080/docs

3. **Check API health**: 
   http://localhost:8080/health

### Testing Endpoints

Use the interactive Swagger UI to test endpoints directly in your browser, or use tools like:
- **Postman**: Import the OpenAPI specification
- **curl**: Command-line testing
- **HTTPie**: User-friendly HTTP client

## 📈 Monitoring & Observability

### Health Checks

- **Health**: Basic API availability
- **Ready**: Database and dependencies status  
- **Metrics**: System performance data

### Logging

All API requests are logged with:
- Request ID for tracing
- Response times
- Error details (without sensitive data)
- Community data access patterns

## 🤝 Community Impact

Every API request serves real communities and real families. Our metrics track:

- **Communities Served**: Number of communities with shared data
- **Stories Shared**: Community narratives with approval
- **Research Impact**: Studies enabled by community data
- **Policy Influence**: Policy decisions informed by our data

## 🔄 API Versioning

- **Current Version**: v1
- **Base URL**: `/v1/`
- **Backward Compatibility**: Maintained for all v1 endpoints
- **Deprecation Policy**: 6-month notice for breaking changes

## 📞 Support & Contact

### Technical Support
- **Email**: support@resilience-mapping.org
- **Documentation**: This site and Swagger UI
- **Status Page**: https://status.resilience-mapping.org

### Community Relations
- **Community Concerns**: community@resilience-mapping.org  
- **Data Privacy**: privacy@resilience-mapping.org
- **Research Partnerships**: research@resilience-mapping.org

### For Researchers
- **Data Use Agreements**: Required for research access
- **Ethics Review**: IRB approval recommended
- **Attribution**: Proper citation of community contributions required

### For Policymakers  
- **Policy Briefs**: Available through the API
- **Impact Reports**: Quarterly analysis of policy outcomes
- **Consultation**: Available for evidence-based policy development

## 🏗️ Development Roadmap

### Upcoming Features
- **Real-time notifications**: Community story updates
- **Advanced analytics**: Deeper insights for researchers  
- **Interactive maps**: Geographic visualization of communities
- **Multi-language support**: Accessible to diverse communities

### Community Feedback
We actively incorporate community feedback into API development:
- **Community Advisory Board**: Guides platform development
- **Regular Surveys**: Direct input from communities
- **Open Source**: Core platform available for community contributions

---

*Built with ❤️ for 1,059+ resilient communities across America*

*"Every data point represents real people with real dignity"*