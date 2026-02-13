import React from 'react';
import { CheckCircle, TrendingUp, RefreshCw, FileCheck } from 'lucide-react';
import type { VerificationResponse } from '../types/policy';

interface ResultsDisplayProps {
  verificationResult: VerificationResponse;
  onStartOver: () => void;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({
  verificationResult,
  onStartOver,
}) => {
  const { accuracy_score, total_fields, edited_fields_count } = verificationResult;
  const extractedFieldsCount = total_fields - edited_fields_count;

  // Determine accuracy color
  const getAccuracyColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-orange-600';
  };

  const getAccuracyBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-50 border-green-200';
    if (score >= 60) return 'bg-yellow-50 border-yellow-200';
    return 'bg-orange-50 border-orange-200';
  };

  return (
    <div className="w-full max-w-2xl mx-auto px-4">
      {/* Logo */}
      <div className="flex justify-center mb-8 md:mb-12">
        <img
          src="/src/assets/images/totality-insurance-agency-logo.png"
          alt="Totality Insurance Agency"
          className="h-20 w-auto md:h-28 lg:h-32 object-contain"
        />
      </div>

      {/* Results Card */}
      <div className="bg-white rounded-lg shadow-lg p-8 md:p-12">
        {/* Success Icon */}
        <div className="flex justify-center mb-6">
          <div className="relative">
            <div className="absolute inset-0 bg-green-500 rounded-full opacity-20 animate-pulse"></div>
            <div className="relative p-4 bg-green-50 rounded-full">
              <CheckCircle className="h-16 w-16 md:h-20 md:w-20 text-green-600" />
            </div>
          </div>
        </div>

        {/* Success Message */}
        <div className="text-center mb-8">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-800 mb-2">
            Verification Complete!
          </h2>
          <p className="text-base md:text-lg text-gray-600">
            Your policy data has been successfully verified and saved
          </p>
        </div>

        {/* Accuracy Score */}
        <div className={`p-6 rounded-lg border-2 mb-6 ${getAccuracyBgColor(accuracy_score)}`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <TrendingUp className={`h-8 w-8 ${getAccuracyColor(accuracy_score)}`} />
              <div>
                <p className="text-sm text-gray-600 font-medium">AI Extraction Accuracy</p>
                <p className="text-xs text-gray-500">Based on {total_fields} total fields</p>
              </div>
            </div>
            <div className={`text-4xl md:text-5xl font-bold ${getAccuracyColor(accuracy_score)}`}>
              {accuracy_score.toFixed(0)}%
            </div>
          </div>
        </div>

        {/* Statistics Grid */}
        <div className="grid grid-cols-2 gap-4 mb-8">
          {/* Total Fields */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <FileCheck className="h-5 w-5 text-blue-600" />
              <span className="text-sm font-medium text-gray-700">Total Fields</span>
            </div>
            <p className="text-3xl font-bold text-blue-600">{total_fields}</p>
          </div>

          {/* AI Extracted */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <span className="text-sm font-medium text-gray-700">AI Extracted</span>
            </div>
            <p className="text-3xl font-bold text-green-600">{extractedFieldsCount}</p>
          </div>

          {/* Manual Edits */}
          <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <svg className="h-5 w-5 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
              <span className="text-sm font-medium text-gray-700">Corrections Made</span>
            </div>
            <p className="text-3xl font-bold text-orange-600">{edited_fields_count}</p>
          </div>

          {/* Completion Rate */}
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <svg className="h-5 w-5 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-sm font-medium text-gray-700">Completion</span>
            </div>
            <p className="text-3xl font-bold text-purple-600">100%</p>
          </div>
        </div>

        {/* Performance Message */}
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-6">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 mt-0.5">
              <svg
                className="h-5 w-5 text-blue-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <div className="text-sm text-gray-700">
              {accuracy_score >= 80 ? (
                <p>
                  <span className="font-semibold text-green-600">Excellent performance!</span> The AI
                  successfully extracted most fields automatically.
                </p>
              ) : accuracy_score >= 60 ? (
                <p>
                  <span className="font-semibold text-yellow-600">Good performance.</span> The AI
                  extracted a majority of fields with some manual corrections needed.
                </p>
              ) : (
                <p>
                  <span className="font-semibold text-orange-600">Partial extraction.</span> This
                  document may have complex formatting or missing information.
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="space-y-3">
          <button
            onClick={onStartOver}
            className="w-full py-4 px-6 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-lg transition-all duration-200 flex items-center justify-center space-x-2"
          >
            <RefreshCw className="h-5 w-5" />
            <span>Process Another Policy</span>
          </button>

          {/* TODO: Add Google Sheets export button in Phase 3 */}
        </div>

        {/* Next Steps Info */}
        <div className="mt-6 text-center text-sm text-gray-500">
          <p>✓ Data verified and saved</p>
          <p className="mt-1 text-xs">
            Future updates will include Google Sheets export and calendar reminders
          </p>
        </div>
      </div>
    </div>
  );
};

export default ResultsDisplay;
