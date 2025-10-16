# Technical Architecture Decisions
## Health Resilience Mapping Platform

**Decision Date**: January 31, 2025  
**Team Consensus**: Unanimous Approval  
**Review Cycle**: Quarterly

---

## 🎯 Key Architecture Decisions

### 1. Hybrid Deployment: Vercel + Fly.io

**Decision**: Use Vercel for frontend hosting and Fly.io for backend services

**Rationale**:
- Vercel's edge network provides unmatched static site performance
- Fly.io offers container flexibility for persistent services
- Separation of concerns improves reliability
- No vendor lock-in

**Trade-offs**:
- ✅ Best-in-class performance for both frontend and backend
- ✅ Independent scaling and failure domains
- ❌ Slightly more complex deployment orchestration
- ❌ Two platforms to manage

**Team Votes**:
- Marcus (35%): "Perfect separation of concerns"
- Aaliyah (25%): "Gives us control where we need it"
- Jordan (10%): "Vercel's edge performance is unbeatable"

---

### 2. Next.js 14 with App Router

**Decision**: Use Next.js 14 App Router for all three frontend sites

**Rationale**:
- React Server Components reduce client bundle size
- Built-in ISR for fresh content with static performance
- Excellent TypeScript support
- Native Vercel integration

**Trade-offs**:
- ✅ Modern architecture with streaming SSR
- ✅ Automatic code splitting
- ✅ Built-in image optimization
- ❌ App Router is newer, less community resources
- ❌ Learning curve for RSC patterns

**Team Consensus**:
- Jordan: "App Router's streaming SSR is perfect for our performance goals"
- Yuki: "Component-level data fetching simplifies design"

---

### 3. Supabase for Database & Auth

**Decision**: Keep Supabase as our primary database and authentication provider

**Rationale**:
- Already proven with successful data import
- PostGIS support crucial for geographic queries
- Row Level Security provides fine-grained access control
- Real-time subscriptions for live updates
- Open source with self-hosting option

**Trade-offs**:
- ✅ Integrated auth, storage, and realtime
- ✅ PostgreSQL maturity and PostGIS power
- ✅ RLS for security at database level
- ❌ Vendor dependency (mitigated by open source)
- ❌ Limited edge presence (mitigated by caching)

**Critical Requirements Met**:
- Miguel: "PostGIS is non-negotiable for spatial queries"
- Marcus: "RLS gives us security at the deepest level"
- Keisha: "Community data control is guaranteed"

---

### 4. Monorepo with Turborepo

**Decision**: Structure as monorepo with shared packages

**Rationale**:
- Three sites share components and logic
- Consistent design system across sites
- Unified deployment pipeline
- Better code reuse and maintenance

**Structure**:
```
/apps (stories, research, policy, admin)
/packages (ui, utils, types, database)
/services (search, workers, analytics)
```

**Trade-offs**:
- ✅ Single source of truth for shared code
- ✅ Atomic commits across sites
- ✅ Consistent versioning
- ❌ Larger repository size
- ❌ More complex initial setup

---

### 5. Typesense for Search

**Decision**: Deploy Typesense on Fly.io for search functionality

**Rationale**:
- Better for structured data than Elasticsearch
- Lower resource requirements
- Typo tolerance and faceted search
- Easy geographic search integration

**Trade-offs**:
- ✅ Fast faceted search perfect for our data
- ✅ Lower operational overhead than Elastic
- ✅ Built-in typo tolerance
- ❌ Smaller community than Elasticsearch
- ❌ Less flexibility for complex queries

---

### 6. Privacy-First Analytics with Plausible

**Decision**: Self-host Plausible Analytics on Fly.io

**Rationale**:
- No cookies, GDPR/CCPA compliant by design
- Lightweight script (< 1KB)
- Privacy respects our communities
- Self-hosting keeps data under our control

**Trade-offs**:
- ✅ Complete data ownership
- ✅ No impact on performance
- ✅ Respects user privacy
- ❌ Less detailed than Google Analytics
- ❌ Self-hosting maintenance required

**Keisha's Requirement**: "No surveillance, period. This is perfect."

---

### 7. Tailwind + CSS Modules Styling

**Decision**: Tailwind CSS for utility-first styling with CSS Modules for component-specific styles

**Rationale**:
- Tailwind provides consistent design system
- CSS Modules prevent style conflicts
- Both have excellent Next.js integration
- Small bundle size with purging

**Trade-offs**:
- ✅ Rapid development with utilities
- ✅ Type-safe with TypeScript
- ✅ Automatic purging of unused styles
- ❌ Tailwind learning curve
- ❌ Verbose className strings

**Yuki's Direction**: "Utilities for layout, modules for components"

---

### 8. Progressive Enhancement Strategy

**Decision**: Build with progressive enhancement - works without JavaScript

**Rationale**:
- Critical for accessibility
- Improves performance on slow devices
- Better SEO
- Respects users with JS disabled

**Implementation**:
- Server-side rendering for all content
- Forms work without JavaScript
- Navigation works without JavaScript
- Enhancements added when JS available

**David's Mandate**: "If it doesn't work without JS, it doesn't work"

---

### 9. Multi-Region Disaster Recovery

**Decision**: Primary in us-east-1 with standby in us-west-2

**Rationale**:
- Communities depend on platform availability
- Geographic redundancy prevents total outage
- Automated failover minimizes downtime
- Cost justified by critical nature

**Trade-offs**:
- ✅ 99.99% availability target achievable
- ✅ Disaster recovery under 1 hour
- ✅ No data loss with streaming replication
- ❌ Higher infrastructure costs
- ❌ More complex deployment

**Aaliyah's Requirement**: "Zero excuse for extended downtime"

---

### 10. Component Library Architecture

**Decision**: Build on Radix UI primitives with custom design system

**Rationale**:
- Radix provides accessible primitives
- Unstyled allows complete design control
- Composable architecture
- Production-tested in major apps

**Trade-offs**:
- ✅ Accessibility built-in
- ✅ Complete styling control
- ✅ Well-maintained
- ❌ More initial setup than styled libraries
- ❌ Need to build design layer

---

## 🔒 Security Architecture Decisions

### Defense in Depth
```yaml
Perimeter: Cloudflare (DDoS, WAF, rate limiting)
    ↓
Edge: Vercel (Edge middleware validation)
    ↓
Application: Next.js (Input validation, CORS)
    ↓
Database: Supabase (RLS, encryption)
    ↓
Audit: Every access logged
```

### Data Classification
```typescript
enum DataSensitivity {
  PUBLIC,        // Community stories, aggregate data
  REGISTERED,    // Detailed research data
  PRIVATE,       // PII, contact information
  RESTRICTED     // Never exposed via API
}
```

---

## 📊 Performance Decisions

### Static Generation Strategy
- **Build Time**: Generate all community pages
- **Revalidation**: ISR every hour for fresh content
- **Fallback**: Generate on-demand for new content
- **Cache**: Edge cache with stale-while-revalidate

### Bundle Size Budgets
```javascript
{
  main: 50,      // KB - Main bundle
  vendor: 100,   // KB - Vendor bundle
  total: 200,    // KB - Total initial load
  perRoute: 30   // KB - Per route chunk
}
```

---

## ♿ Accessibility Decisions

### Non-Negotiable Standards
1. WCAG AAA compliance (7:1 contrast ratio)
2. Full keyboard navigation
3. Screen reader tested (NVDA, JAWS, VoiceOver)
4. Works at 200% zoom
5. No auto-playing media
6. Reduced motion support

### Testing Requirements
- Automated testing in CI (axe-core)
- Manual testing with disabled users
- Quarterly accessibility audits
- Bug priority: a11y bugs = critical

---

## 🌍 Data Architecture Decisions

### Geographic Data Handling
```sql
-- Store multiple representations for different use cases
full_precision    GEOGRAPHY  -- Accurate calculations
display_geometry  GEOMETRY   -- Fast rendering
centroid         POINT       -- Distance queries
bounding_box     BOX2D       -- Initial filtering
```

### Privacy Levels
```typescript
interface PrivacyControl {
  dataSharing: 'none' | 'aggregate' | 'research' | 'public'
  storySharing: boolean
  contactSharing: 'none' | 'verified' | 'all'
  immediateDelete: boolean  // GDPR right to erasure
}
```

---

## 📝 Documentation Decisions

### Documentation Requirements
1. **Code**: JSDoc for all public APIs
2. **Components**: Storybook for UI library
3. **Architecture**: ADRs for decisions
4. **API**: OpenAPI specification
5. **User**: Markdown in docs/ folder

### Documentation Tools
- Storybook for components
- TypeDoc for API documentation
- Docusaurus for user documentation
- Mermaid for diagrams
- README.md for quick start

---

## 🚀 Deployment Decisions

### Environment Strategy
```yaml
Production:  main branch → production URLs
Staging:     staging branch → staging URLs
Preview:     PR → preview-*.vercel.app
Local:       Docker Compose for all services
```

### Feature Flags
```typescript
// Using Vercel Edge Config for feature flags
const features = {
  newMapView: { enabled: false, rollout: 0 },
  aiSearch: { enabled: true, rollout: 0.1 },
  storyVideo: { enabled: true, rollout: 1.0 },
}
```

---

## 📊 Monitoring Decisions

### Observability Stack
```yaml
Errors: Sentry
Performance: Web Vitals → Prometheus
Uptime: Better Stack
Logs: Fly.io → Grafana Loki
Traces: OpenTelemetry → Jaeger
Analytics: Plausible (privacy-first)
```

### Alert Priorities
- **P0**: Site down, data breach (immediate)
- **P1**: Degraded performance, errors spike (15 min)
- **P2**: Failed deployments, high latency (1 hour)
- **P3**: Anomalies, trends (daily)

---

## ⚡ Performance Optimization Decisions

### Image Strategy
1. Next.js Image component for all images
2. WebP with JPEG fallback
3. AVIF for supporting browsers
4. Responsive images with srcset
5. Lazy loading with native loading="lazy"
6. Blur placeholder for above-fold images

### Caching Strategy
```yaml
Static Assets: 1 year (immutable)
HTML Pages: 1 hour (s-maxage=3600)
API Responses: 5 minutes (community data)
Search Results: 1 minute
User-specific: No cache
```

---

## 🔄 State Management Decisions

### Client State: Zustand
- Simple API
- TypeScript support
- DevTools integration
- Small bundle (8KB)

### Server State: React Query + Supabase
- Cache management
- Optimistic updates
- Real-time subscriptions
- Automatic refetching

### Form State: React Hook Form + Zod
- Performance (uncontrolled)
- Validation with Zod
- TypeScript inference
- Accessibility built-in

---

## 🎨 Design System Decisions

### Token Structure
```typescript
const tokens = {
  colors: {},      // Semantic, not hex values
  typography: {},   // Scale, not specific sizes
  spacing: {},      // Consistent scale
  breakpoints: {},  // Mobile-first
  motion: {}        // Duration and easing
}
```

### Component Principles
1. Composable over configurable
2. Accessible by default
3. Responsive without media queries
4. Theme-able via CSS variables
5. Zero runtime CSS-in-JS

---

## 📱 Mobile Decisions

### Mobile-First Development
- Design at 375px width first
- Enhance for larger screens
- Touch targets minimum 44px
- Thumb-friendly navigation
- Offline-first architecture

### PWA Features
```json
{
  "name": "Resilience Mapping",
  "short_name": "Resilience",
  "start_url": "/",
  "display": "standalone",
  "orientation": "portrait",
  "theme_color": "#2563eb",
  "background_color": "#ffffff"
}
```

---

## 🌐 Internationalization Decisions

### i18n Strategy
- Next.js built-in i18n routing
- Locale detection from browser
- Content negotiation via Accept-Language
- Static generation per locale
- Fallback to English

### Translation Management
- JSON files in public/locales
- Namespace per feature
- Community-contributed translations
- Professional translation for legal content

---

## 🔐 Authentication Decisions

### Auth Flow
1. Supabase Auth for identity
2. JWT for session management
3. Refresh tokens in httpOnly cookies
4. Access tokens in memory only
5. Role-based access control (RBAC)

### Session Management
```typescript
const sessionConfig = {
  access_token_ttl: 15 * 60,        // 15 minutes
  refresh_token_ttl: 7 * 24 * 60,   // 7 days
  idle_timeout: 30 * 60,             // 30 minutes
  absolute_timeout: 24 * 60          // 24 hours
}
```

---

## 📈 Scaling Decisions

### Horizontal Scaling Points
- Frontend: Vercel auto-scales
- Database: Read replicas for research site
- Search: Multiple Typesense nodes
- Workers: Fly.io auto-scaling
- Storage: Supabase Storage (S3)

### Performance Targets
```yaml
Concurrent Users: 10,000
Requests/Second: 1,000
Database Connections: 100 pooled
Search QPS: 500
Page Generation: 100/second
```

---

## 🤝 Team Agreements

### Code Quality Standards
- TypeScript strict mode
- 80% test coverage minimum
- No any types without comment
- Prettier + ESLint enforced
- PR requires 2 approvals

### Development Workflow
- Feature branches from main
- Conventional commits
- Squash merge to main
- Automated changelog
- Semantic versioning

### Communication
- Daily standup async in Slack
- Weekly architecture review
- Monthly retrospective
- Quarterly planning
- All decisions documented

---

## 📅 Review Schedule

### Weekly Reviews
- Performance metrics
- Error rates
- Security alerts
- Community feedback

### Monthly Reviews
- Architecture decisions
- Technical debt
- Dependency updates
- Team velocity

### Quarterly Reviews
- Full architecture review
- Technology radar update
- Team skill assessment
- Platform evolution

---

*These decisions reflect team consensus as of January 31, 2025. Changes require team discussion and documentation.*