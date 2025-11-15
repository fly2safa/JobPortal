/**
 * Utility functions for handling API errors from FastAPI backend
 */

/**
 * Extract a user-friendly error message from an API error response
 * 
 * FastAPI can return errors in different formats:
 * 1. String: "Error message"
 * 2. Array of validation errors: [{type, loc, msg, input, ctx}]
 * 3. Object with detail field
 * 
 * @param err - The error object from axios/fetch
 * @param fallbackMessage - Default message if error can't be parsed
 * @returns User-friendly error message string
 */
export function getErrorMessage(err: any, fallbackMessage: string = 'An error occurred. Please try again.'): string {
  // Try to get the detail field from response
  const detail = err?.response?.data?.detail || err?.detail;
  
  if (!detail) {
    // Check for other error fields
    if (err?.response?.data?.error) {
      return err.response.data.error;
    }
    if (err?.response?.data?.message) {
      return err.response.data.message;
    }
    if (err?.message) {
      return err.message;
    }
    return fallbackMessage;
  }
  
  // Handle array of validation errors (FastAPI validation)
  if (Array.isArray(detail)) {
    const errorMessages = detail
      .map((e: any) => {
        // Extract field name from loc array if available
        const field = e.loc && e.loc.length > 1 ? e.loc[e.loc.length - 1] : '';
        const msg = e.msg || e.message || 'Invalid value';
        return field ? `${field}: ${msg}` : msg;
      })
      .join('; ');
    
    return errorMessages || 'Validation failed. Please check your input.';
  }
  
  // Handle string detail
  if (typeof detail === 'string') {
    return detail;
  }
  
  // Handle object detail
  if (typeof detail === 'object' && detail.message) {
    return detail.message;
  }
  
  return fallbackMessage;
}

/**
 * Check if the error is a network error (no response from server)
 */
export function isNetworkError(err: any): boolean {
  return !err?.response && err?.request;
}

/**
 * Check if the error is an authentication error (401)
 */
export function isAuthError(err: any): boolean {
  return err?.response?.status === 401;
}

/**
 * Check if the error is a validation error (422)
 */
export function isValidationError(err: any): boolean {
  return err?.response?.status === 422;
}

/**
 * Check if the error is a not found error (404)
 */
export function isNotFoundError(err: any): boolean {
  return err?.response?.status === 404;
}

