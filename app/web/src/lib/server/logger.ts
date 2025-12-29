/**
 * Structured logger for observability.
 *
 * Outputs JSON logs for easy parsing by log aggregation services.
 * In production, these would be sent to a service like Datadog, Grafana, etc.
 */

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogContext {
	[key: string]: unknown;
}

interface LogEntry {
	timestamp: string;
	level: LogLevel;
	message: string;
	context?: LogContext;
	correlationId?: string;
}

/**
 * Generate a short correlation ID for request tracing.
 */
function generateCorrelationId(): string {
	return crypto.randomUUID().slice(0, 8);
}

/**
 * Format log entry as JSON.
 */
function formatLogEntry(entry: LogEntry): string {
	return JSON.stringify(entry);
}

/**
 * Create a logger instance.
 */
function createLogger() {
	const log = (level: LogLevel, message: string, context?: LogContext): void => {
		const entry: LogEntry = {
			timestamp: new Date().toISOString(),
			level,
			message,
			...(context && { context })
		};

		const formatted = formatLogEntry(entry);

		switch (level) {
			case 'error':
				console.error(formatted);
				break;
			case 'warn':
				console.warn(formatted);
				break;
			case 'debug':
				console.debug(formatted);
				break;
			default:
				console.log(formatted);
		}
	};

	return {
		debug: (message: string, context?: LogContext) => log('debug', message, context),
		info: (message: string, context?: LogContext) => log('info', message, context),
		warn: (message: string, context?: LogContext) => log('warn', message, context),
		error: (message: string, context?: LogContext) => log('error', message, context),

		/**
		 * Create a child logger with a correlation ID for request tracing.
		 */
		withCorrelationId: (correlationId?: string) => {
			const id = correlationId || generateCorrelationId();
			return {
				debug: (message: string, context?: LogContext) =>
					log('debug', message, { ...context, correlationId: id }),
				info: (message: string, context?: LogContext) =>
					log('info', message, { ...context, correlationId: id }),
				warn: (message: string, context?: LogContext) =>
					log('warn', message, { ...context, correlationId: id }),
				error: (message: string, context?: LogContext) =>
					log('error', message, { ...context, correlationId: id }),
				correlationId: id
			};
		},

		generateCorrelationId
	};
}

export const logger = createLogger();
