import React, { useState } from 'react';
import UploadZone from './components/UploadZone';
import ExtractionLoader from './components/ExtractionLoader';
import VerificationForm from './components/VerificationForm';
import ResultsDisplay from './components/ResultsDisplay';
import type { ExtractionResponse, VerificationResponse } from './types/policy';

import logo from './assets/images/totality-insurance-agency-logo.png';

type MainPageState = 'main' | 'upload' | 'extracting' | 'verify' | 'complete';

function App() {
  const [page, setPage] = useState<MainPageState>('main');
  const [fileId, setFileId] = useState<string>('');
  const [filename, setFilename] = useState<string>('');
  const [extractedData, setExtractedData] = useState<ExtractionResponse | null>(null);
  const [verificationResult, setVerificationResult] = useState<VerificationResponse | null>(null);
  const [error, setError] = useState<string>('');

  // Handlers for workflow
  const handleUploadSuccess = (uploadedFileId: string, uploadedFilename: string) => {
    setFileId(uploadedFileId);
    setFilename(uploadedFilename);
    setPage('extracting');
    setError('');
  };
  const handleUploadError = (errorMessage: string) => setError(errorMessage);
  const handleExtractionComplete = (data: ExtractionResponse) => {
    setExtractedData(data);
    setPage('verify');
    setError('');
  };
  const handleExtractionError = (errorMessage: string) => {
    setError(errorMessage);
    setPage('upload');
  };
  const handleVerificationComplete = (result: VerificationResponse) => {
    setVerificationResult(result);
    setPage('complete');
    setError('');
  };
  const handleVerificationError = (errorMessage: string) => setError(errorMessage);
  const handleStartOver = () => {
    setPage('main');
    setFileId('');
    setFilename('');
    setExtractedData(null);
    setVerificationResult(null);
    setError('');
  };

  // Main landing page
  if (page === 'main') {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 to-white px-4">
        <img
          src={logo}
          alt="Totality Insurance Agency Logo"
          className="h-24 md:h-32 lg:h-36 mb-8 drop-shadow-xl"
        />
        <h1 className="text-3xl md:text-4xl font-bold text-blue-900 mb-2 text-center">Policy AI Lens</h1>
        <p className="text-gray-600 mb-8 text-center max-w-xl">Welcome! Please choose an option below to get started.</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-xl">
          <button
            className="py-5 px-6 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-lg shadow-lg transition-all border-2 border-blue-700"
            onClick={() => setPage('upload')}
          >
            Save new record
          </button>
          <button
            className="py-5 px-6 rounded-xl bg-white hover:bg-gray-100 text-blue-700 font-semibold text-lg shadow-lg transition-all border-2 border-blue-700"
            onClick={() => alert('Search record coming soon!')}
          >
            Search record
          </button>
          <button
            className="py-5 px-6 rounded-xl bg-green-600 hover:bg-green-700 text-white font-semibold text-lg shadow-lg transition-all border-2 border-green-700"
            onClick={() => alert('Generate Quotation coming soon!')}
          >
            Generate Quotation
          </button>
          <button
            className="py-5 px-6 rounded-xl bg-black hover:bg-gray-900 text-white font-semibold text-lg shadow-lg transition-all border-2 border-gray-900"
            onClick={() => alert('Generate Receipt coming soon!')}
          >
            Generate Receipt
          </button>
        </div>
      </div>
    );
  }

  // Back button for all workflow pages except main
  const showBackButton = page !== 'main';

  // Existing workflow (Save new record)
  return (
    <div className="min-h-screen bg-gray-50 py-8 md:py-12 relative">
      {showBackButton && (
        <button
          className="absolute top-6 left-6 flex items-center px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 shadow transition-colors duration-200 z-10"
          onClick={handleStartOver}
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7"></path></svg>
          Back
        </button>
      )}
      <div className="container mx-auto px-4">

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
        {page === 'upload' && (
          <UploadZone 
            onUploadSuccess={handleUploadSuccess}
            onUploadError={handleUploadError}
          />
        )}

        {page === 'extracting' && (
          <ExtractionLoader
            filename={filename}
            fileId={fileId}
            onExtractionComplete={handleExtractionComplete}
            onExtractionError={handleExtractionError}
          />
        )}

        {page === 'verify' && extractedData && (
          <VerificationForm
            extractedData={extractedData}
            fileId={fileId}
            onVerificationComplete={handleVerificationComplete}
            onVerificationError={handleVerificationError}
          />
        )}

        {page === 'complete' && verificationResult && (
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
