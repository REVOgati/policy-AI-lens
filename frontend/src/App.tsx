import React, { useState } from 'react';
import UploadZone from './components/UploadZone';
import ExtractionLoader from './components/ExtractionLoader';
import VerificationForm from './components/VerificationForm';
import ResultsDisplay from './components/ResultsDisplay';
import type { ExtractionResponse, VerificationResponse } from './types/policy';

function App() {
  const [currentStep, setCurrentStep] = useState<'upload' | 'extracting' | 'verify' | 'complete'>('upload');
  const [fileId, setFileId] = useState<string>('');
  const [filename, setFilename] = useState<string>('');
  const [extractedData, setExtractedData] = useState<ExtractionResponse | null>(null);
  const [verificationResult, setVerificationResult] = useState<VerificationResponse | null>(null);
  const [error, setError] = useState<string>('');

  const handleUploadSuccess = (uploadedFileId: string, uploadedFilename: string) => {
    setFileId(uploadedFileId);
    setFilename(uploadedFilename);
    setCurrentStep('extracting');
    setError('');
  };

  const handleUploadError = (errorMessage: string) => {
    setError(errorMessage);
  };

  const handleExtractionComplete = (data: ExtractionResponse) => {
    console.log('Extraction completed:', data); // Debug log
    setExtractedData(data);
    setCurrentStep('verify');
    setError('');
  };

  const handleExtractionError = (errorMessage: string) => {
    setError(errorMessage);
    setCurrentStep('upload');
  };

  const handleVerificationComplete = (result: VerificationResponse) => {
    setVerificationResult(result);
    setCurrentStep('complete');
    setError('');
  };

  const handleVerificationError = (errorMessage: string) => {
    setError(errorMessage);
  };

  const handleStartOver = () => {
    setCurrentStep('upload');
    setFileId('');
    setFilename('');
    setExtractedData(null);
    setVerificationResult(null);
    setError('');
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 md:py-12">
      <div className="container mx-auto px-4">
        {/* Debug Info - Remove in production */}
        <div className="max-w-2xl mx-auto mb-4 p-2 bg-gray-800 text-white text-xs rounded">
          <p>Current Step: {currentStep}</p>
          <p>Has Extracted Data: {extractedData ? 'Yes' : 'No'}</p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="max-w-2xl mx-auto mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-start space-x-2">
              <svg className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <p className="font-medium text-red-800">Error</p>
                <p className="text-sm text-red-600">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Main Content */}
        {currentStep === 'upload' && (
          <UploadZone 
            onUploadSuccess={handleUploadSuccess}
            onUploadError={handleUploadError}
          />
        )}

        {currentStep === 'extracting' && (
          <ExtractionLoader
            filename={filename}
            fileId={fileId}
            onExtractionComplete={handleExtractionComplete}
            onExtractionError={handleExtractionError}
          />
        )}

        {currentStep === 'verify' && extractedData && (
          <VerificationForm
            extractedData={extractedData}
            fileId={fileId}
            onVerificationComplete={handleVerificationComplete}
            onVerificationError={handleVerificationError}
          />
        )}

        {currentStep === 'complete' && verificationResult && (
          <ResultsDisplay
            verificationResult={verificationResult}
            onStartOver={handleStartOver}
          />
        )}
      </div>
    </div>
  );
}

export default App;
