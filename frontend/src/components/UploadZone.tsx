import React, { useState, useCallback } from 'react';
import { Upload, FileText, AlertCircle } from 'lucide-react';
import { apiConfig } from '../services/apiConfig';
import logoImage from '../assets/images/totality-insurance-agency-logo.png';

interface UploadZoneProps {
  onUploadSuccess: (fileId: string, filename: string) => void;
  onUploadError: (error: string) => void;
}

const UploadZone: React.FC<UploadZoneProps> = ({ onUploadSuccess, onUploadError }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const validateFile = (file: File): string | null => {
    // Check file type
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      return 'Only PDF files are allowed';
    }

    // Check file size (10MB max)
    const maxSize = 10 * 1024 * 1024; // 10MB in bytes
    if (file.size > maxSize) {
      return 'File size must be less than 10MB';
    }

    return null;
  };

  const handleUpload = async (file: File) => {
    // Validate file
    const validationError = validateFile(file);
    if (validationError) {
      onUploadError(validationError);
      return;
    }

    setSelectedFile(file);
    setIsUploading(true);

    try {
      // Create form data
      const formData = new FormData();
      formData.append('file', file);

      // Upload to backend
      const response = await fetch(apiConfig.endpoints.upload, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      const data = await response.json();
      onUploadSuccess(data.file_id, data.filename);
    } catch (error) {
      onUploadError(error instanceof Error ? error.message : 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleUpload(files[0]);
    }
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleUpload(files[0]);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto px-4">
      {/* Logo */}
      <div className="flex justify-center mb-8 md:mb-12">
        <img
          src={logoImage}
          alt="Totality Insurance Agency"
          className="h-20 w-auto md:h-28 lg:h-32 object-contain"
        />
      </div>

      {/* Upload Zone */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`
          relative border-2 border-dashed rounded-lg p-8 md:p-12
          transition-all duration-200 ease-in-out
          ${isDragging 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 bg-white hover:border-gray-400'
          }
          ${isUploading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        `}
      >
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileSelect}
          disabled={isUploading}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          id="file-upload"
        />

        <div className="flex flex-col items-center text-center space-y-4">
          {isUploading ? (
            <>
              {/* Loading State */}
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              <div className="space-y-2">
                <p className="text-lg font-medium text-gray-700">Uploading...</p>
                {selectedFile && (
                  <p className="text-sm text-gray-500">{selectedFile.name}</p>
                )}
              </div>
            </>
          ) : (
            <>
              {/* Upload Icon */}
              <div className="p-4 bg-blue-50 rounded-full">
                <Upload className="h-8 w-8 md:h-10 md:w-10 text-blue-600" />
              </div>

              {/* Instructions */}
              <div className="space-y-2">
                <p className="text-lg md:text-xl font-semibold text-gray-700">
                  Upload Insurance Policy
                </p>
                <p className="text-sm md:text-base text-gray-500">
                  Drag and drop your PDF here, or click to browse
                </p>
              </div>

              {/* File Requirements */}
              <div className="flex items-center space-x-2 text-xs md:text-sm text-gray-400">
                <FileText className="h-4 w-4" />
                <span>PDF only • Max 10MB</span>
              </div>

              {/* Upload Button for Mobile */}
              <button
                type="button"
                className="mt-4 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium
                         hover:bg-blue-700 transition-colors duration-200
                         focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
                         md:hidden"
                onClick={() => document.getElementById('file-upload')?.click()}
              >
                Choose File
              </button>
            </>
          )}
        </div>
      </div>

      {/* Info Message */}
      <div className="mt-6 flex items-start space-x-2 text-sm text-gray-600 bg-blue-50 p-4 rounded-lg">
        <AlertCircle className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
        <div>
          <p className="font-medium">AI will extract:</p>
          <p className="text-gray-500 mt-1">
            Policy holder, policy number, insurer name, dates, premium, and more from your insurance certificate.
          </p>
        </div>
      </div>
    </div>
  );
};

export default UploadZone;
