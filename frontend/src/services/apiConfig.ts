/**
 * API Configuration
 * Provides centralized API endpoint configuration based on environment
 */

// Get base URL from environment variables, fallback to localhost
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const APP_ENV = import.meta.env.VITE_APP_ENV || 'development';

/**
 * API configuration object
 */
export const apiConfig = {
  baseUrl: API_BASE_URL,
  environment: APP_ENV,
  
  endpoints: {
    upload: `${API_BASE_URL}/api/v1/upload`,
    extract: (fileId: string) => `${API_BASE_URL}/api/v1/extract/${fileId}`,
    verify: `${API_BASE_URL}/api/v1/verify`,
    results: `${API_BASE_URL}/api/v1/results`,
    summary: `${API_BASE_URL}/api/v1/summary`,
  },

  isDevelopment: () => APP_ENV === 'development',
  isProduction: () => APP_ENV === 'production',
};

/**
 * Helper function to get full API URL
 * @param path - API path (e.g., '/api/v1/upload')
 * @returns Full API URL
 */
export const getApiUrl = (path: string): string => {
  // Remove leading slash if present to avoid double slashes
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${API_BASE_URL}${cleanPath}`;
};

export default apiConfig;
