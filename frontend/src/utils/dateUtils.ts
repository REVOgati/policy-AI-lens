/**
 * Date utility functions for converting between formats
 */

/**
 * Convert DD/MM/YYYY to YYYY-MM-DD (for HTML date input)
 */
export function ddmmyyyyToISO(date: string | null): string {
  if (!date) return '';
  
  // Check if already in ISO format (YYYY-MM-DD)
  if (/^\d{4}-\d{2}-\d{2}$/.test(date)) {
    return date;
  }
  
  // Convert DD/MM/YYYY to YYYY-MM-DD
  const parts = date.split('/');
  if (parts.length === 3) {
    const [day, month, year] = parts;
    return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
  }
  
  return '';
}

/**
 * Convert YYYY-MM-DD to DD/MM/YYYY (for backend)
 */
export function isoToDDMMYYYY(date: string | null): string {
  if (!date) return '';
  
  // Check if already in DD/MM/YYYY format
  if (/^\d{2}\/\d{2}\/\d{4}$/.test(date)) {
    return date;
  }
  
  // Convert YYYY-MM-DD to DD/MM/YYYY
  const parts = date.split('-');
  if (parts.length === 3) {
    const [year, month, day] = parts;
    return `${day}/${month}/${year}`;
  }
  
  return '';
}

/**
 * Format date for display
 */
export function formatDateForDisplay(date: string | null): string {
  if (!date) return 'Not set';
  
  // If in DD/MM/YYYY format, return as is
  if (/^\d{2}\/\d{2}\/\d{4}$/.test(date)) {
    return date;
  }
  
  // If in ISO format, convert to DD/MM/YYYY
  if (/^\d{4}-\d{2}-\d{2}$/.test(date)) {
    return isoToDDMMYYYY(date);
  }
  
  return date;
}
