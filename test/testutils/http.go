// HTTP test utilities
// Created: January 31, 2025
// Purpose: HTTP testing utilities for API endpoints

package testutils

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/your-org/resilience-mapping/pkg/auth"
	"github.com/your-org/resilience-mapping/internal/config"
)

// TestClient provides HTTP testing utilities
type TestClient struct {
	router     *gin.Engine
	jwtManager *auth.JWTManager
}

// NewTestClient creates a new HTTP test client
func NewTestClient(router *gin.Engine) *TestClient {
	// Set Gin to test mode
	gin.SetMode(gin.TestMode)

	// Create JWT manager for testing
	jwtManager := auth.NewJWTManager("test-secret-key", "test-issuer")

	return &TestClient{
		router:     router,
		jwtManager: jwtManager,
	}
}

// Request makes an HTTP request and returns the response
func (tc *TestClient) Request(method, path string, body interface{}, headers map[string]string) *httptest.ResponseRecorder {
	var reqBody io.Reader
	
	if body != nil {
		jsonBody, err := json.Marshal(body)
		if err != nil {
			panic(fmt.Sprintf("Failed to marshal request body: %v", err))
		}
		reqBody = bytes.NewReader(jsonBody)
	}

	req := httptest.NewRequest(method, path, reqBody)
	
	// Set default headers
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Accept", "application/json")
	
	// Add custom headers
	for key, value := range headers {
		req.Header.Set(key, value)
	}

	w := httptest.NewRecorder()
	tc.router.ServeHTTP(w, req)

	return w
}

// GET makes a GET request
func (tc *TestClient) GET(path string, headers map[string]string) *httptest.ResponseRecorder {
	return tc.Request("GET", path, nil, headers)
}

// POST makes a POST request
func (tc *TestClient) POST(path string, body interface{}, headers map[string]string) *httptest.ResponseRecorder {
	return tc.Request("POST", path, body, headers)
}

// PUT makes a PUT request
func (tc *TestClient) PUT(path string, body interface{}, headers map[string]string) *httptest.ResponseRecorder {
	return tc.Request("PUT", path, body, headers)
}

// DELETE makes a DELETE request
func (tc *TestClient) DELETE(path string, headers map[string]string) *httptest.ResponseRecorder {
	return tc.Request("DELETE", path, nil, headers)
}

// AuthenticatedRequest makes a request with JWT authentication
func (tc *TestClient) AuthenticatedRequest(method, path string, body interface{}, userID int, userType, role string) *httptest.ResponseRecorder {
	token, err := tc.jwtManager.GenerateToken(
		userID,
		fmt.Sprintf("test%d@example.com", userID),
		userType,
		role,
		nil,
		24*3600, // 24 hours
	)
	if err != nil {
		panic(fmt.Sprintf("Failed to generate test token: %v", err))
	}

	headers := map[string]string{
		"Authorization": "Bearer " + token,
	}

	return tc.Request(method, path, body, headers)
}

// AdminRequest makes a request as admin user
func (tc *TestClient) AdminRequest(method, path string, body interface{}) *httptest.ResponseRecorder {
	return tc.AuthenticatedRequest(method, path, body, 1, "admin", "admin")
}

// MemberRequest makes a request as community member
func (tc *TestClient) MemberRequest(method, path string, body interface{}) *httptest.ResponseRecorder {
	return tc.AuthenticatedRequest(method, path, body, 2, "community_member", "member")
}

// ResearcherRequest makes a request as researcher
func (tc *TestClient) ResearcherRequest(method, path string, body interface{}) *httptest.ResponseRecorder {
	return tc.AuthenticatedRequest(method, path, body, 3, "researcher", "researcher")
}

// Response helpers

// AssertStatusCode checks if response has expected status code
func (tc *TestClient) AssertStatusCode(t *testing.T, resp *httptest.ResponseRecorder, expectedStatus int) {
	if resp.Code != expectedStatus {
		t.Errorf("Expected status code %d, got %d. Body: %s", 
			expectedStatus, resp.Code, resp.Body.String())
	}
}

// AssertJSON checks if response is valid JSON and unmarshals it
func (tc *TestClient) AssertJSON(t *testing.T, resp *httptest.ResponseRecorder, dest interface{}) {
	if resp.Header().Get("Content-Type") != "application/json; charset=utf-8" {
		t.Errorf("Expected JSON content type, got: %s", resp.Header().Get("Content-Type"))
	}

	if err := json.NewDecoder(resp.Body).Decode(dest); err != nil {
		t.Errorf("Failed to decode JSON response: %v. Body: %s", err, resp.Body.String())
	}
}

// AssertContains checks if response body contains expected text
func (tc *TestClient) AssertContains(t *testing.T, resp *httptest.ResponseRecorder, expected string) {
	body := resp.Body.String()
	if !strings.Contains(body, expected) {
		t.Errorf("Expected response to contain '%s', got: %s", expected, body)
	}
}

// AssertNotContains checks if response body does not contain text
func (tc *TestClient) AssertNotContains(t *testing.T, resp *httptest.ResponseRecorder, unexpected string) {
	body := resp.Body.String()
	if strings.Contains(body, unexpected) {
		t.Errorf("Expected response to not contain '%s', but it did. Body: %s", unexpected, body)
	}
}

// AssertHeader checks if response has expected header value
func (tc *TestClient) AssertHeader(t *testing.T, resp *httptest.ResponseRecorder, header, expected string) {
	actual := resp.Header().Get(header)
	if actual != expected {
		t.Errorf("Expected header %s to be '%s', got '%s'", header, expected, actual)
	}
}

// AssertCommunityMessage checks for community-friendly error messages
func (tc *TestClient) AssertCommunityMessage(t *testing.T, resp *httptest.ResponseRecorder) {
	var response map[string]interface{}
	tc.AssertJSON(t, resp, &response)
	
	if _, exists := response["community_message"]; !exists {
		t.Errorf("Expected community-friendly message in response: %v", response)
	}
}

// Test data helpers

// CreateTestRequestBody creates a JSON request body from struct
func CreateTestRequestBody(data interface{}) map[string]interface{} {
	jsonData, err := json.Marshal(data)
	if err != nil {
		panic(fmt.Sprintf("Failed to marshal test data: %v", err))
	}
	
	var result map[string]interface{}
	if err := json.Unmarshal(jsonData, &result); err != nil {
		panic(fmt.Sprintf("Failed to unmarshal test data: %v", err))
	}
	
	return result
}

// ParseJSONResponse parses JSON response into struct
func ParseJSONResponse(resp *httptest.ResponseRecorder, dest interface{}) error {
	return json.NewDecoder(resp.Body).Decode(dest)
}

// Community-specific test helpers

// AssertCommunityInResponse checks if community data is present in response
func (tc *TestClient) AssertCommunityInResponse(t *testing.T, resp *httptest.ResponseRecorder, tractID string) {
	var response map[string]interface{}
	tc.AssertJSON(t, resp, &response)
	
	// Check for community data
	if community, exists := response["community"]; exists {
		if communityMap, ok := community.(map[string]interface{}); ok {
			if id, exists := communityMap["tract_id"]; !exists || id != tractID {
				t.Errorf("Expected community with tract_id %s in response", tractID)
			}
		}
	} else if communities, exists := response["communities"]; exists {
		if communitiesArray, ok := communities.([]interface{}); ok {
			found := false
			for _, item := range communitiesArray {
				if communityMap, ok := item.(map[string]interface{}); ok {
					if id, exists := communityMap["tract_id"]; exists && id == tractID {
						found = true
						break
					}
				}
			}
			if !found {
				t.Errorf("Expected community with tract_id %s in communities array", tractID)
			}
		}
	} else {
		t.Errorf("Expected community data in response: %v", response)
	}
}

// AssertStoryInResponse checks if story data is present in response
func (tc *TestClient) AssertStoryInResponse(t *testing.T, resp *httptest.ResponseRecorder, slug string) {
	var response map[string]interface{}
	tc.AssertJSON(t, resp, &response)
	
	// Check for story data
	if story, exists := response["story"]; exists {
		if storyMap, ok := story.(map[string]interface{}); ok {
			if storySlug, exists := storyMap["slug"]; !exists || storySlug != slug {
				t.Errorf("Expected story with slug %s in response", slug)
			}
		}
	} else if stories, exists := response["stories"]; exists {
		if storiesArray, ok := stories.([]interface{}); ok {
			found := false
			for _, item := range storiesArray {
				if storyMap, ok := item.(map[string]interface{}); ok {
					if storySlug, exists := storyMap["slug"]; exists && storySlug == slug {
						found = true
						break
					}
				}
			}
			if !found {
				t.Errorf("Expected story with slug %s in stories array", slug)
			}
		}
	} else {
		t.Errorf("Expected story data in response: %v", response)
	}
}

// AssertPrivacyProtection checks that private data is not leaked
func (tc *TestClient) AssertPrivacyProtection(t *testing.T, resp *httptest.ResponseRecorder) {
	body := resp.Body.String()
	
	// Check for common sensitive fields that should not be exposed
	sensitiveFields := []string{
		"password_hash",
		"two_factor_secret", 
		"recovery_tokens",
		"private_email",
		"ssn",
		"phone_private",
	}
	
	for _, field := range sensitiveFields {
		if strings.Contains(body, field) {
			t.Errorf("Response contains sensitive field '%s': %s", field, body)
		}
	}
}

// AssertRateLimited checks if request was rate limited
func (tc *TestClient) AssertRateLimited(t *testing.T, resp *httptest.ResponseRecorder) {
	tc.AssertStatusCode(t, resp, http.StatusTooManyRequests)
	tc.AssertContains(t, resp, "rate limit")
}

// AssertAuthRequired checks if authentication is required
func (tc *TestClient) AssertAuthRequired(t *testing.T, resp *httptest.ResponseRecorder) {
	tc.AssertStatusCode(t, resp, http.StatusUnauthorized)
	tc.AssertContains(t, resp, "Authorization")
}

// AssertPermissionDenied checks if permission is denied
func (tc *TestClient) AssertPermissionDenied(t *testing.T, resp *httptest.ResponseRecorder) {
	tc.AssertStatusCode(t, resp, http.StatusForbidden)
	tc.AssertContains(t, resp, "permission")
}

// Benchmark helpers

// BenchmarkEndpoint benchmarks an API endpoint
func (tc *TestClient) BenchmarkEndpoint(b *testing.B, method, path string, body interface{}) {
	headers := map[string]string{}
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		resp := tc.Request(method, path, body, headers)
		if resp.Code >= 400 {
			b.Errorf("Request failed with status %d: %s", resp.Code, resp.Body.String())
		}
	}
}

// Performance test helpers

// TestResponseTime checks if response time is within acceptable range
func (tc *TestClient) TestResponseTime(t *testing.T, method, path string, maxDuration int64) {
	start := time.Now()
	resp := tc.Request(method, path, nil, nil)
	duration := time.Since(start)
	
	if duration.Milliseconds() > maxDuration {
		t.Errorf("Response took too long: %v (max: %dms)", duration, maxDuration)
	}
	
	if resp.Code >= 500 {
		t.Errorf("Server error: %d %s", resp.Code, resp.Body.String())
	}
}

// Community values testing

// AssertCommunityFirst checks that responses follow community-first principles
func (tc *TestClient) AssertCommunityFirst(t *testing.T, resp *httptest.ResponseRecorder) {
	// Check for dignity-first language
	body := resp.Body.String()
	
	// Should not contain deficit-based language
	deficitTerms := []string{"struggling", "failing", "broken", "disadvantaged"}
	for _, term := range deficitTerms {
		if strings.Contains(strings.ToLower(body), term) {
			t.Errorf("Response contains deficit language '%s': %s", term, body)
		}
	}
	
	// Should contain asset-based language
	if resp.Code == http.StatusOK {
		assetTerms := []string{"resilient", "strength", "community", "dignity"}
		hasAssetLanguage := false
		for _, term := range assetTerms {
			if strings.Contains(strings.ToLower(body), term) {
				hasAssetLanguage = true
				break
			}
		}
		
		if !hasAssetLanguage {
			t.Logf("Consider adding asset-based language to response: %s", body[:100])
		}
	}
}

// AssertAccessibility checks basic accessibility compliance
func (tc *TestClient) AssertAccessibility(t *testing.T, resp *httptest.ResponseRecorder) {
	// For JSON responses, check structure supports screen readers
	if strings.Contains(resp.Header().Get("Content-Type"), "json") {
		var response map[string]interface{}
		if err := json.NewDecoder(resp.Body).Decode(&response); err == nil {
			// Check for descriptive field names
			if message, exists := response["message"]; exists {
				if msg, ok := message.(string); ok && len(msg) > 0 {
					// Good - has descriptive message
				} else {
					t.Logf("Consider adding descriptive messages for accessibility")
				}
			}
		}
	}
}