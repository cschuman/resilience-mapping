// Community service layer
// Created: January 31, 2025
// Purpose: Business logic for community operations with dignity-first approach

package services

import (
	"context"
	"github.com/your-org/resilience-mapping/internal/repositories"
)

// CommunityService handles business logic for communities
type CommunityService struct {
	communityRepo *repositories.CommunityRepository
	storyRepo     *repositories.StoryRepository
	userRepo      *repositories.UserRepository
}

// NewCommunityService creates a new community service
func NewCommunityService(
	communityRepo *repositories.CommunityRepository,
	storyRepo *repositories.StoryRepository,
	userRepo *repositories.UserRepository,
) *CommunityService {
	return &CommunityService{
		communityRepo: communityRepo,
		storyRepo:     storyRepo,
		userRepo:      userRepo,
	}
}

// GetStoryRepository returns the story repository for handler access
func (s *CommunityService) GetStoryRepository() *repositories.StoryRepository {
	return s.storyRepo
}

// ValidateCommunityAccess checks if a user can access community data
func (s *CommunityService) ValidateCommunityAccess(ctx context.Context, communityID int, userID int) (bool, error) {
	// Get community
	community, err := s.communityRepo.GetByID(ctx, communityID)
	if err != nil {
		return false, err
	}
	
	// Check if community is public
	if community.GetPrivacyLevel() == "public" {
		return true, nil
	}
	
	// Check if user is a member of the community
	if userID > 0 {
		user, err := s.userRepo.GetByID(ctx, userID)
		if err != nil {
			return false, err
		}
		
		if user.CommunityID != nil && *user.CommunityID == communityID {
			return true, nil
		}
	}
	
	return false, nil
}

// Additional business logic methods would be implemented here
// For example:
// - Community approval workflows
// - Data quality validation
// - Privacy level management
// - Community engagement tracking