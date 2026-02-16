import React, { useState, useEffect } from 'react';
import { CheckCircle, Edit3, Calendar, DollarSign, FileText, User, Building, Shield } from 'lucide-react';
import type { PolicyData, ExtractionResponse, VerificationResponse } from '../types/policy';
import { apiConfig } from '../services/apiConfig';

interface VerificationFormProps {
  extractedData: ExtractionResponse;
  fileId: string;
  onVerificationComplete: (response: VerificationResponse) => void;
  onVerificationError: (error: string) => void;
}

const VerificationForm: React.FC<VerificationFormProps> = ({
  extractedData,
  fileId,
  onVerificationComplete,
  onVerificationError,
}) => {
  const [formData, setFormData] = useState<PolicyData>(extractedData.data);
  const [editedFields, setEditedFields] = useState<Set<string>>(new Set());
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleFieldChange = (field: keyof PolicyData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    setEditedFields((prev) => new Set(prev).add(field));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await fetch(apiConfig.endpoints.verify, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          extraction_id: extractedData.extraction_id,
          verified_data: formData,
          edited_fields: Array.from(editedFields),
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Verification failed');
      }

      const data: VerificationResponse = await response.json();
      onVerificationComplete(data);
    } catch (error) {
      onVerificationError(error instanceof Error ? error.message : 'Verification failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  const fieldIcons = {
    policy_holder: User,
    policy_number: FileText,
    insurer_name: Building,
    sum_insured: DollarSign,
    commencing_date: Calendar,
    expiring_date: Calendar,
    premium_amount: DollarSign,
    paid_amount: DollarSign,
    balance_amount: DollarSign,
    policy_type: Shield,
  };

  const fieldLabels = {
    policy_holder: 'Policy Holder',
    policy_number: 'Policy Number',
    insurer_name: 'Insurer Name',
    sum_insured: 'Sum Insured',
    commencing_date: 'Commencing Date',
    expiring_date: 'Expiring Date',
    premium_amount: 'Premium Amount',
    paid_amount: 'Paid Amount',
    balance_amount: 'Balance Amount',
    policy_type: 'Policy Type',
  };

  const renderField = (field: keyof PolicyData) => {
    const Icon = fieldIcons[field];
    const isEdited = editedFields.has(field);
    const hasValue = formData[field] !== null && formData[field] !== '';
    const isDateField = field === 'commencing_date' || field === 'expiring_date';

    return (
      <div key={field} className="space-y-2">
        <label
          htmlFor={field}
          className="flex items-center space-x-2 text-sm font-medium text-gray-700"
        >
          <Icon className="h-4 w-4 text-gray-500" />
          <span>{fieldLabels[field]}</span>
          {isEdited && (
            <span className="ml-auto flex items-center text-xs text-orange-600">
              <Edit3 className="h-3 w-3 mr-1" />
              Edited
            </span>
          )}
          {hasValue && !isEdited && (
            <span className="ml-auto flex items-center text-xs text-green-600">
              <CheckCircle className="h-3 w-3 mr-1" />
              AI Extracted
            </span>
          )}
        </label>
        <input
          type="text"
          id={field}
          value={formData[field] || ''}
          onChange={(e) => handleFieldChange(field, e.target.value)}
          className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all ${
            !hasValue
              ? 'border-orange-300 bg-orange-50'
              : isEdited
              ? 'border-orange-300 bg-orange-50'
              : 'border-gray-300 bg-white'
          }`}
          placeholder={isDateField ? 'DD/MM/YYYY' : `Enter ${fieldLabels[field].toLowerCase()}`}
        />
        {!hasValue && (
          <p className="text-xs text-orange-600 flex items-center space-x-1">
            <span>⚠️</span>
            <span>Not extracted - please fill in manually</span>
          </p>
        )}
      </div>
    );
  };

  const totalFields = Object.keys(fieldLabels).length;
  const extractedFields = Object.values(formData).filter(
    (value) => value !== null && value !== ''
  ).length;

  return (
    <div className="w-full max-w-3xl mx-auto px-4">
      {/* Logo */}
      <div className="flex justify-center mb-8 md:mb-12">
        <img
          src="/src/assets/images/totality-insurance-agency-logo.png"
          alt="Totality Insurance Agency"
          className="h-20 w-auto md:h-28 lg:h-32 object-contain"
        />
      </div>

      {/* Verification Card */}
      <div className="bg-white rounded-lg shadow-lg p-6 md:p-8">
        {/* Header */}
        <div className="mb-6 pb-6 border-b">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-800 mb-2">
            Verification Stage
          </h2>
          <p className="text-sm md:text-base text-gray-600">
            Review and correct the extracted information
          </p>

          {/* Extraction Stats */}
          <div className="mt-4 flex items-center justify-between p-4 bg-blue-50 rounded-lg">
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-5 w-5 text-blue-600" />
              <span className="text-sm font-medium text-gray-700">
                AI Extracted: {extractedFields}/{totalFields} fields
              </span>
            </div>
            <div className="text-2xl font-bold text-blue-600">
              {Math.round((extractedFields / totalFields) * 100)}%
            </div>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Personal Information */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800 flex items-center space-x-2">
              <User className="h-5 w-5" />
              <span>Personal Information</span>
            </h3>
            {renderField('policy_holder')}
          </div>

          {/* Policy Details */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800 flex items-center space-x-2">
              <FileText className="h-5 w-5" />
              <span>Policy Details</span>
            </h3>
            {renderField('policy_number')}
            {renderField('policy_type')}
            {renderField('insurer_name')}
          </div>

          {/* Financial Information */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800 flex items-center space-x-2">
              <DollarSign className="h-5 w-5" />
              <span>Financial Information</span>
            </h3>
            {renderField('sum_insured')}
            {renderField('premium_amount')}
            {renderField('paid_amount')}
            {renderField('balance_amount')}
          </div>

          {/* Dates */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800 flex items-center space-x-2">
              <Calendar className="h-5 w-5" />
              <span>Coverage Period</span>
            </h3>
            {renderField('commencing_date')}
            {renderField('expiring_date')}
          </div>

          {/* Info Box */}
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
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
              <div className="text-sm text-gray-600">
                <p className="font-medium mb-1">Verification Tips:</p>
                <ul className="list-disc list-inside space-y-1">
                  <li>Green checkmark = AI extracted successfully</li>
                  <li>Orange warning = Field needs manual entry</li>
                  <li>Edited fields will be marked for accuracy tracking</li>
                  <li>Dates should be in DD/MM/YYYY format</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <div className="pt-6">
            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full py-4 px-6 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold rounded-lg shadow-lg transition-all duration-200 flex items-center justify-center space-x-2"
            >
              {isSubmitting ? (
                <>
                  <svg
                    className="animate-spin h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  <span>Submitting...</span>
                </>
              ) : (
                <>
                  <CheckCircle className="h-5 w-5" />
                  <span>Confirm & Submit</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default VerificationForm;
