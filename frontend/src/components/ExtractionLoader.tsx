import React, { useEffect, useState } from 'react';
import { Loader2, FileCheck, Brain, Sparkles } from 'lucide-react';
import { apiConfig } from '../services/apiConfig';

interface ExtractionLoaderProps {
  filename: string;
  fileId: string;
  onExtractionComplete: (data: any) => void;
  onExtractionError: (error: string) => void;
}

const ExtractionLoader: React.FC<ExtractionLoaderProps> = ({
  filename,
  fileId,
  onExtractionComplete,
  onExtractionError,
}) => {
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState('Processing document...');

  const steps = [
    { text: 'Reading PDF document...', icon: FileCheck },
    { text: 'Analyzing with AI...', icon: Brain },
    { text: 'Extracting policy data...', icon: Sparkles },
  ];

  useEffect(() => {
    // Animate progress
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) return prev;
        return prev + 10;
      });
    }, 300);

    // Cycle through steps
    let stepIndex = 0;
    const stepInterval = setInterval(() => {
      stepIndex = (stepIndex + 1) % steps.length;
      setCurrentStep(steps[stepIndex].text);
    }, 2000);

    // Call extraction API
    const extractData = async () => {
      try {
        const response = await fetch(apiConfig.endpoints.extract(fileId), {
          method: 'POST',
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Extraction failed');
        }

        const data = await response.json();
        
        console.log('Extraction response:', data); // Debug log
        
        // Complete the progress
        setProgress(100);
        
        // Wait a moment before completing
        setTimeout(() => {
          onExtractionComplete(data);
        }, 500);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Extraction failed';
        
        // Provide user-friendly error messages
        if (errorMessage.includes('timeout') || errorMessage.includes('Deadline')) {
          onExtractionError('AI service timed out. Please try again - the service may be busy.');
        } else if (errorMessage.includes('quota') || errorMessage.includes('429')) {
          onExtractionError('AI service quota exceeded. Please wait a few minutes and try again.');
        } else {
          onExtractionError(errorMessage);
        }
      } finally {
        clearInterval(progressInterval);
        clearInterval(stepInterval);
      }
    };

    extractData();

    return () => {
      clearInterval(progressInterval);
      clearInterval(stepInterval);
    };
  }, [fileId]);

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

      {/* Extraction Card */}
      <div className="bg-white rounded-lg shadow-lg p-8 md:p-12">
        {/* Animated Icon */}
        <div className="flex justify-center mb-6">
          <div className="relative">
            <div className="absolute inset-0 bg-blue-500 rounded-full opacity-20 animate-ping"></div>
            <div className="relative p-4 bg-blue-50 rounded-full">
              <Loader2 className="h-12 w-12 md:h-16 md:w-16 text-blue-600 animate-spin" />
            </div>
          </div>
        </div>

        {/* Status Text */}
        <div className="text-center space-y-2 mb-6">
          <h2 className="text-xl md:text-2xl font-bold text-gray-800">
            Analyzing Your Policy
          </h2>
          <p className="text-sm md:text-base text-gray-600">{filename}</p>
        </div>

        {/* Progress Bar */}
        <div className="mb-6">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>{currentStep}</span>
            <span>{progress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
            <div
              className="bg-blue-600 h-2.5 rounded-full transition-all duration-300 ease-out"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>

        {/* Processing Steps */}
        <div className="space-y-3">
          {steps.map((step, index) => {
            const Icon = step.icon;
            const isActive = step.text === currentStep;
            const isComplete = progress > (index + 1) * 30;

            return (
              <div
                key={index}
                className={`flex items-center space-x-3 p-3 rounded-lg transition-all duration-300 ${
                  isActive ? 'bg-blue-50 border border-blue-200' : 'bg-gray-50'
                }`}
              >
                <div
                  className={`flex-shrink-0 p-2 rounded-full ${
                    isComplete
                      ? 'bg-green-100'
                      : isActive
                      ? 'bg-blue-100'
                      : 'bg-gray-200'
                  }`}
                >
                  <Icon
                    className={`h-5 w-5 ${
                      isComplete
                        ? 'text-green-600'
                        : isActive
                        ? 'text-blue-600'
                        : 'text-gray-400'
                    }`}
                  />
                </div>
                <span
                  className={`text-sm md:text-base ${
                    isActive ? 'font-medium text-gray-800' : 'text-gray-600'
                  }`}
                >
                  {step.text}
                </span>
                {isActive && (
                  <Loader2 className="h-4 w-4 text-blue-600 animate-spin ml-auto" />
                )}
                {isComplete && (
                  <svg
                    className="h-5 w-5 text-green-600 ml-auto"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                )}
              </div>
            );
          })}
        </div>

        {/* Info Text */}
        <div className="mt-6 text-center text-sm text-gray-500">
          <p>Using AI to extract policy details...</p>
          <p className="mt-1">This usually takes 5-15 seconds</p>
          <p className="mt-2 text-xs text-gray-400">
            If it takes longer, the document may be complex or the service may be busy
          </p>
        </div>
      </div>
    </div>
  );
};

export default ExtractionLoader;
