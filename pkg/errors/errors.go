// Shared error types and handling
// Created: January 31, 2025
// Purpose: Community-friendly error messages and types

package errors

import (
	"errors"
	"fmt"
	"net/http"
)

// Common error types
var (
	ErrNotFound          = errors.New("resource not found")
	ErrUnauthorized      = errors.New("unauthorized access")
	ErrForbidden         = errors.New("access forbidden")
	ErrValidation        = errors.New("validation failed")
	ErrCommunityPrivate  = errors.New("community data is private")
	ErrStoryNotApproved  = errors.New("story requires community approval")
	ErrInvalidInput      = errors.New("invalid input provided")
	ErrServiceUnavailable = errors.New("service temporarily unavailable")
)

// AppError represents an application-specific error
type AppError struct {
	Code             string `json:"code"`
	Message          string `json:"message"`
	CommunityMessage string `json:"community_message,omitempty"`
	HTTPStatus       int    `json:"-"`
	InternalError    error  `json:"-"`
}

func (e *AppError) Error() string {
	if e.InternalError != nil {
		return fmt.Sprintf("%s: %v", e.Message, e.InternalError)
	}
	return e.Message
}

// NewAppError creates a new application error
func NewAppError(code, message string, httpStatus int) *AppError {
	return &AppError{
		Code:       code,
		Message:    message,
		HTTPStatus: httpStatus,
	}
}

// WithCommunityMessage adds a community-friendly message
func (e *AppError) WithCommunityMessage(message string) *AppError {
	e.CommunityMessage = message
	return e
}

// WithInternalError adds internal error details
func (e *AppError) WithInternalError(err error) *AppError {
	e.InternalError = err
	return e
}

// Common error constructors

func NotFound(resource string) *AppError {
	return NewAppError(
		"NOT_FOUND",
		fmt.Sprintf("%s not found", resource),
		http.StatusNotFound,
	).WithCommunityMessage("The information you're looking for isn't available right now")
}

func Unauthorized() *AppError {
	return NewAppError(
		"UNAUTHORIZED",
		"Authentication required",
		http.StatusUnauthorized,
	).WithCommunityMessage("Please log in to access this feature")
}

func Forbidden(reason string) *AppError {
	return NewAppError(
		"FORBIDDEN",
		reason,
		http.StatusForbidden,
	).WithCommunityMessage("You don't have permission to access this information")
}

func ValidationError(details string) *AppError {
	return NewAppError(
		"VALIDATION_ERROR",
		fmt.Sprintf("Validation failed: %s", details),
		http.StatusBadRequest,
	).WithCommunityMessage("Please check your information and try again")
}

func CommunityPrivate() *AppError {
	return NewAppError(
		"COMMUNITY_PRIVATE",
		"Community has chosen to keep their data private",
		http.StatusForbidden,
	).WithCommunityMessage("This community has chosen to keep their information private")
}

func StoryRequiresApproval() *AppError {
	return NewAppError(
		"STORY_PENDING",
		"Story is pending community approval",
		http.StatusForbidden,
	).WithCommunityMessage("This story is waiting for community approval before being shared")
}

func ServiceUnavailable() *AppError {
	return NewAppError(
		"SERVICE_UNAVAILABLE",
		"Service is temporarily unavailable",
		http.StatusServiceUnavailable,
	).WithCommunityMessage("We're having trouble right now, but we're working to fix it")
}

func InternalError() *AppError {
	return NewAppError(
		"INTERNAL_ERROR",
		"An internal error occurred",
		http.StatusInternalServerError,
	).WithCommunityMessage("Something went wrong on our end. Our team has been notified.")
}