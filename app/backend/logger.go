// Package middleware contains HTTP middleware for the API server
// Created: January 31, 2025
// Purpose: Request logging middleware with community-focused messaging

package middleware

import (
	"fmt"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

// Logger returns a gin.HandlerFunc for request logging
func Logger() gin.HandlerFunc {
	// Create logger instance
	logger := logrus.New()
	logger.SetFormatter(&logrus.JSONFormatter{
		TimestampFormat: time.RFC3339,
		FieldMap: logrus.FieldMap{
			logrus.FieldKeyTime:  "timestamp",
			logrus.FieldKeyLevel: "level",
			logrus.FieldKeyMsg:   "message",
		},
	})

	return gin.LoggerWithFormatter(func(param gin.LogFormatterParams) string {
		// Log to structured logger for production use
		entry := logger.WithFields(logrus.Fields{
			"method":      param.Method,
			"path":        param.Path,
			"status":      param.StatusCode,
			"latency":     param.Latency,
			"client_ip":   param.ClientIP,
			"user_agent":  param.Request.UserAgent(),
			"request_id":  param.Request.Header.Get("X-Request-ID"),
			"referer":     param.Request.Referer(),
		})

		// Add different log levels based on status code
		switch {
		case param.StatusCode >= 500:
			entry.Error("Server error")
		case param.StatusCode >= 400:
			entry.Warn("Client error")
		case param.StatusCode >= 300:
			entry.Info("Redirect")
		default:
			entry.Info("Request completed")
		}

		// Return formatted log line for Gin's console output
		var statusColor, methodColor, resetColor string
		if param.IsOutputColor() {
			statusColor = param.StatusCodeColor()
			methodColor = param.MethodColor()
			resetColor = param.ResetColor()
		}

		return fmt.Sprintf("[COMMUNITY-API] %v |%s %3d %s| %13v | %15s |%s %-7s %s %#v\n%s",
			param.TimeStamp.Format("2006/01/02 - 15:04:05"),
			statusColor, param.StatusCode, resetColor,
			param.Latency,
			param.ClientIP,
			methodColor, param.Method, resetColor,
			param.Path,
			param.ErrorMessage,
		)
	})
}