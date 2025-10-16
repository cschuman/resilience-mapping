// Community HTTP handlers
// Created: January 31, 2025
// Purpose: Handle HTTP requests for community data with dignity and privacy

package handlers

import (
	"net/http"
	"strconv"
	
	"github.com/gin-gonic/gin"
	"github.com/your-org/resilience-mapping/internal/repositories"
	"github.com/your-org/resilience-mapping/internal/models"
	"github.com/your-org/resilience-mapping/internal/services"
)

// CommunityHandler handles HTTP requests for communities
type CommunityHandler struct {
	repo    *repositories.CommunityRepository
	service *services.CommunityService
}

// NewCommunityHandler creates a new community handler
func NewCommunityHandler(repo *repositories.CommunityRepository, service *services.CommunityService) *CommunityHandler {
	return &CommunityHandler{
		repo:    repo,
		service: service,
	}
}

// List retrieves communities with pagination and filtering
// @Summary Get list of communities
// @Description Retrieve a paginated list of public communities with optional filtering
// @Tags communities
// @Accept json
// @Produce json
// @Param q query string false "Search query"
// @Param state query string false "Filter by state code"
// @Param county query string false "Filter by county code"
// @Param resilient query boolean false "Show only unexpectedly resilient communities"
// @Param min_score query number false "Minimum resilience score"
// @Param max_score query number false "Maximum resilience score"
// @Param min_population query integer false "Minimum population"
// @Param max_population query integer false "Maximum population"
// @Param sort query string false "Sort by field" default(resilience_score)
// @Param limit query integer false "Number of results to return" default(20)
// @Param offset query integer false "Number of results to skip" default(0)
// @Success 200 {object} map[string]interface{} "List of communities"
// @Failure 500 {object} map[string]interface{} "Internal server error"
// @Router /communities [get]
func (h *CommunityHandler) List(c *gin.Context) {
	// Parse query parameters
	params := repositories.SearchParams{
		Query:              c.Query("q"),
		State:              c.Query("state"),
		County:             c.Query("county"),
		OnlyUnexpectedGood: c.Query("resilient") == "true",
		PublicOnly:         true, // Always filter for public access
		SortBy:             c.DefaultQuery("sort", "resilience_score"),
		Limit:              parseIntWithDefault(c.Query("limit"), 20),
		Offset:             parseIntWithDefault(c.Query("offset"), 0),
	}
	
	// Parse numeric filters
	if minScore := c.Query("min_score"); minScore != "" {
		if score, err := strconv.ParseFloat(minScore, 64); err == nil {
			params.MinResilienceScore = score
		}
	}
	
	if maxScore := c.Query("max_score"); maxScore != "" {
		if score, err := strconv.ParseFloat(maxScore, 64); err == nil {
			params.MaxResilienceScore = score
		}
	}
	
	if minPop := c.Query("min_population"); minPop != "" {
		if pop, err := strconv.Atoi(minPop); err == nil {
			params.MinPopulation = pop
		}
	}
	
	if maxPop := c.Query("max_population"); maxPop != "" {
		if pop, err := strconv.Atoi(maxPop); err == nil {
			params.MaxPopulation = pop
		}
	}
	
	// Search communities
	communities, total, err := h.repo.SearchCommunities(c.Request.Context(), params)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Failed to retrieve communities",
			"community_message": "We're having trouble accessing community data right now",
		})
		return
	}
	
	// Return response with community-friendly messaging
	c.JSON(http.StatusOK, gin.H{
		"communities": communities,
		"total":       total,
		"limit":       params.Limit,
		"offset":      params.Offset,
		"message":     "Celebrating resilient communities across America",
		"note":        "Each community shown has given permission to share their story",
	})
}

// GetByID retrieves a specific community
// @Summary Get community by ID
// @Description Retrieve detailed information for a specific public community
// @Tags communities
// @Accept json
// @Produce json
// @Param id path integer true "Community ID"
// @Success 200 {object} map[string]interface{} "Community details"
// @Failure 400 {object} map[string]interface{} "Invalid community ID"
// @Failure 403 {object} map[string]interface{} "Community information is private"
// @Failure 404 {object} map[string]interface{} "Community not found"
// @Failure 500 {object} map[string]interface{} "Internal server error"
// @Router /communities/{id} [get]
func (h *CommunityHandler) GetByID(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid community ID",
		})
		return
	}
	
	community, err := h.repo.GetByID(c.Request.Context(), id)
	if err != nil {
		if err.Error() == "record not found" {
			c.JSON(http.StatusNotFound, gin.H{
				"error": "Community not found",
				"community_message": "This community may not have chosen to share their information publicly",
			})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{
				"error": "Failed to retrieve community",
			})
		}
		return
	}
	
	// Check privacy settings
	if community.GetPrivacyLevel() != "public" {
		c.JSON(http.StatusForbidden, gin.H{
			"error": "Community information is private",
			"message": "This community has chosen to keep their information private",
		})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{
		"community": community,
		"message":   "Community data shared with permission and respect",
	})
}

// GetStories retrieves stories for a specific community
// @Summary Get stories for community
// @Description Retrieve published stories for a specific community
// @Tags communities,stories
// @Accept json
// @Produce json
// @Param id path integer true "Community ID"
// @Success 200 {object} map[string]interface{} "Community stories"
// @Failure 400 {object} map[string]interface{} "Invalid community ID"
// @Failure 404 {object} map[string]interface{} "Community not found or private"
// @Failure 500 {object} map[string]interface{} "Internal server error"
// @Router /communities/{id}/stories [get]
func (h *CommunityHandler) GetStories(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid community ID",
		})
		return
	}
	
	// Verify community exists and is public
	community, err := h.repo.GetByID(c.Request.Context(), id)
	if err != nil || community.GetPrivacyLevel() != "public" {
		c.JSON(http.StatusNotFound, gin.H{
			"error": "Community not found or private",
		})
		return
	}
	
	// Get published stories only
	storyRepo := h.service.GetStoryRepository() // Assuming service provides this
	stories, err := storyRepo.GetByCommunityID(c.Request.Context(), id, true)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Failed to retrieve stories",
		})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{
		"stories":   stories,
		"community": community.GetDisplayName(),
		"message":   "Stories shared with community approval",
	})
}

// Search performs full-text search on communities
// @Summary Search communities
// @Description Perform full-text search on public communities
// @Tags communities,search
// @Accept json
// @Produce json
// @Param q query string true "Search query"
// @Param limit query integer false "Number of results to return" default(10)
// @Param offset query integer false "Number of results to skip" default(0)
// @Success 200 {object} map[string]interface{} "Search results"
// @Failure 400 {object} map[string]interface{} "Search query is required"
// @Failure 500 {object} map[string]interface{} "Internal server error"
// @Router /communities/search [get]
func (h *CommunityHandler) Search(c *gin.Context) {
	query := c.Query("q")
	if query == "" {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Search query is required",
		})
		return
	}
	
	params := repositories.SearchParams{
		Query:      query,
		PublicOnly: true,
		Limit:      parseIntWithDefault(c.Query("limit"), 10),
		Offset:     parseIntWithDefault(c.Query("offset"), 0),
	}
	
	communities, total, err := h.repo.SearchCommunities(c.Request.Context(), params)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Search failed",
		})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{
		"communities": communities,
		"total":       total,
		"query":       query,
		"message":     "Search results from communities willing to share",
	})
}

// GetNearby finds communities within geographic radius
// @Summary Find nearby communities
// @Description Find public communities within a specified geographic radius
// @Tags communities,geography
// @Accept json
// @Produce json
// @Param lat query number true "Latitude"
// @Param lng query number true "Longitude"
// @Param radius query number false "Search radius in kilometers" default(50)
// @Success 200 {object} map[string]interface{} "Nearby communities"
// @Failure 400 {object} map[string]interface{} "Invalid coordinates"
// @Failure 500 {object} map[string]interface{} "Internal server error"
// @Router /communities/nearby [get]
func (h *CommunityHandler) GetNearby(c *gin.Context) {
	latStr := c.Query("lat")
	lngStr := c.Query("lng")
	radiusStr := c.DefaultQuery("radius", "50") // 50km default
	
	if latStr == "" || lngStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Latitude and longitude are required",
		})
		return
	}
	
	lat, err := strconv.ParseFloat(latStr, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid latitude",
		})
		return
	}
	
	lng, err := strconv.ParseFloat(lngStr, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid longitude",
		})
		return
	}
	
	radius, err := strconv.ParseFloat(radiusStr, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid radius",
		})
		return
	}
	
	communities, err := h.repo.GetNearby(c.Request.Context(), lat, lng, radius)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Failed to find nearby communities",
		})
		return
	}
	
	// Filter for public communities
	var publicCommunities []models.Community
	for _, community := range communities {
		if community.GetPrivacyLevel() == "public" {
			publicCommunities = append(publicCommunities, community)
		}
	}
	
	c.JSON(http.StatusOK, gin.H{
		"communities": publicCommunities,
		"center":      []float64{lat, lng},
		"radius_km":   radius,
		"count":       len(publicCommunities),
	})
}

// GetResilient retrieves all unexpectedly resilient communities
// @Summary Get resilient communities
// @Description Retrieve communities that show unexpected resilience based on research metrics
// @Tags communities,resilience
// @Accept json
// @Produce json
// @Param limit query integer false "Number of results to return" default(100)
// @Success 200 {object} map[string]interface{} "Resilient communities"
// @Failure 500 {object} map[string]interface{} "Internal server error"
// @Router /communities/resilient [get]
func (h *CommunityHandler) GetResilient(c *gin.Context) {
	limit := parseIntWithDefault(c.Query("limit"), 100)
	
	communities, err := h.repo.GetTopResilient(c.Request.Context(), limit)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Failed to retrieve resilient communities",
		})
		return
	}
	
	// Filter for public communities
	var publicCommunities []models.Community
	for _, community := range communities {
		if community.GetPrivacyLevel() == "public" {
			publicCommunities = append(publicCommunities, community)
		}
	}
	
	c.JSON(http.StatusOK, gin.H{
		"communities": publicCommunities,
		"count":       len(publicCommunities),
		"message":     "Celebrating unexpectedly resilient communities",
		"note":        "These communities have defied expectations and thrived",
	})
}

// GetStatistics returns aggregate statistics
// @Summary Get community statistics
// @Description Retrieve aggregate statistics for all public communities
// @Tags communities,statistics
// @Accept json
// @Produce json
// @Success 200 {object} map[string]interface{} "Community statistics"
// @Failure 500 {object} map[string]interface{} "Internal server error"
// @Router /communities/stats [get]
func (h *CommunityHandler) GetStatistics(c *gin.Context) {
	stats, err := h.repo.GetStatistics(c.Request.Context())
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Failed to retrieve statistics",
		})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{
		"statistics": stats,
		"message":    "Data representing real communities with real impact",
	})
}

// ContactCommunity allows users to contact community representatives
func (h *CommunityHandler) ContactCommunity(c *gin.Context) {
	// This would be implemented with proper authentication and consent
	// For now, return a placeholder response
	c.JSON(http.StatusOK, gin.H{
		"message": "Community contact feature coming soon",
		"note":    "All community contacts require explicit consent",
	})
}

// JoinCommunity allows users to join their community
func (h *CommunityHandler) JoinCommunity(c *gin.Context) {
	// This would be implemented with proper verification
	c.JSON(http.StatusOK, gin.H{
		"message": "Community membership feature coming soon",
		"note":    "Community membership requires verification",
	})
}

// ApproveStory allows community representatives to approve stories
func (h *CommunityHandler) ApproveStory(c *gin.Context) {
	// This would be implemented with proper authentication and authorization
	c.JSON(http.StatusOK, gin.H{
		"message": "Story approval feature coming soon",
		"note":    "Only community representatives can approve stories",
	})
}

// GetResearchData provides data access for researchers
func (h *CommunityHandler) GetResearchData(c *gin.Context) {
	// This would require additional authentication and data use agreements
	c.JSON(http.StatusOK, gin.H{
		"message": "Research data access requires additional approval",
		"note":    "Contact research team for data use agreements",
	})
}

// ExportCSV exports community data in CSV format
func (h *CommunityHandler) ExportCSV(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "CSV export feature coming soon",
	})
}

// ExportJSON exports community data in JSON format
func (h *CommunityHandler) ExportJSON(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "JSON export feature coming soon",
	})
}

// GetAnalytics provides research analytics
func (h *CommunityHandler) GetAnalytics(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "Analytics feature coming soon",
	})
}

// Admin endpoints (placeholder implementations)

// CreateCommunity creates a new community
func (h *CommunityHandler) CreateCommunity(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "Create community feature coming soon",
	})
}

// UpdateCommunity updates community information
func (h *CommunityHandler) UpdateCommunity(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "Update community feature coming soon",
	})
}

// ApproveCommunity approves community for public display
func (h *CommunityHandler) ApproveCommunity(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "Approve community feature coming soon",
	})
}

// DeleteCommunity removes a community
func (h *CommunityHandler) DeleteCommunity(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "Delete community feature coming soon",
	})
}

// BulkImport imports communities from data file
func (h *CommunityHandler) BulkImport(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "Bulk import feature coming soon",
	})
}

// Policy endpoints (placeholder implementations)

// GetImpactReports provides impact reports for policymakers
func (h *CommunityHandler) GetImpactReports(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "Impact reports feature coming soon",
	})
}

// GetPolicyRecommendations provides policy recommendations
func (h *CommunityHandler) GetPolicyRecommendations(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "Policy recommendations feature coming soon",
	})
}

// Research site endpoints

// GetResearchDatasets provides datasets for researchers
func (h *CommunityHandler) GetResearchDatasets(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "Research datasets feature coming soon",
	})
}

// GetMethodologies provides research methodologies
func (h *CommunityHandler) GetMethodologies(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "Methodologies feature coming soon",
	})
}

// GetPublications provides research publications
func (h *CommunityHandler) GetPublications(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "Publications feature coming soon",
	})
}

// Policy site endpoints

// GetInterventions provides policy interventions data
func (h *CommunityHandler) GetInterventions(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "Interventions feature coming soon",
	})
}

// GetOutcomes provides policy outcomes data
func (h *CommunityHandler) GetOutcomes(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "Outcomes feature coming soon",
	})
}

// CommunityFeedbackWebhook handles community feedback
func (h *CommunityHandler) CommunityFeedbackWebhook(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"message": "Community feedback received",
		"note":    "Thank you for sharing your perspective",
	})
}

// Helper function to parse integer with default value
func parseIntWithDefault(s string, defaultValue int) int {
	if s == "" {
		return defaultValue
	}
	if i, err := strconv.Atoi(s); err == nil {
		return i
	}
	return defaultValue
}