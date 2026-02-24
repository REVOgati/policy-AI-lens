import React, { useState } from "react";
import axios from "axios";
import { apiConfig } from "../services/apiConfig";

const initialState = {
  policy_number: "",
  policy_holder: "",
  policy_type: "",
  commencing_date: "",
  expiring_date: "",
  premium_amount: "",
  paid_amount: "",
  balance_amount: "",
  registration_no: "",
  vehicle_type: "",
};

const fieldLabels: Record<string, string> = {
  policy_number: "Policy Number",
  policy_holder: "Policy Holder",
  policy_type: "Policy Type",
  commencing_date: "Commencing Date",
  expiring_date: "Expiring Date",
  premium_amount: "Premium Amount",
  paid_amount: "Paid Amount",
  balance_amount: "Balance Amount",
  registration_no: "Registration No",
  vehicle_type: "Vehicle Type",
};

const GenerateReceipt: React.FC = () => {
  const [form, setForm] = useState(initialState);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState(false);
  const receiptSectionRef = React.useRef<HTMLDivElement>(null);

  // Back navigation
  const handleBack = () => {
    if (window.history.length > 1) {
      window.history.back();
    } else {
      window.location.href = '/';
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPdfUrl(null);
    try {
      const response = await axios.post(
        `${apiConfig.baseUrl}/api/v1/receipt/generate`,
        form,
        { responseType: "blob" }
      );
      const url = window.URL.createObjectURL(new Blob([response.data], { type: "application/pdf" }));
      setPdfUrl(url);
      setSubmitted(true);
      // Automatically open in new tab
      window.open(url, '_blank', 'noopener,noreferrer');
      // Scroll to receipt section
      setTimeout(() => {
        receiptSectionRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 300);
    } catch (err: any) {
      setError("Failed to generate receipt.");
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto p-4 bg-white rounded shadow mt-8 relative">
      {/* Responsive Back Button */}
      <button
        onClick={handleBack}
        className="absolute top-4 left-4 flex items-center px-3 py-2 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 shadow transition-colors duration-200 z-10"
        aria-label="Back"
      >
        <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7"></path></svg>
        <span className="hidden sm:inline">Back</span>
      </button>
      <h2 className="text-2xl font-bold mb-4 text-blue-800 text-center">Generate Receipt</h2>
      <form onSubmit={handleSubmit} className="space-y-2 mt-4">
        {Object.keys(initialState).map((key) => (
          <div key={key}>
            <label className="block font-semibold capitalize mb-1">{fieldLabels[key]}</label>
            <input
              type="text"
              name={key}
              value={(form as any)[key]}
              onChange={handleChange}
              className="w-full border rounded px-2 py-1"
              required
              disabled={submitted}
            />
          </div>
        ))}
        <button
          type="submit"
          className="bg-blue-700 text-white px-4 py-2 rounded hover:bg-blue-800 w-full"
          disabled={loading || submitted}
        >
          {loading ? "Generating..." : "Generate Receipt"}
        </button>
      </form>
      {error && <div className="text-red-600 mt-2">{error}</div>}
      {pdfUrl && (
        <div ref={receiptSectionRef} className="mt-4 flex flex-col items-center">
          <div className="text-green-700 font-semibold mb-2">Receipt generated successfully!</div>
          <div className="flex flex-col sm:flex-row gap-2 justify-center">
            <a
              href={pdfUrl}
              download="receipt.pdf"
              className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
            >
              Download Receipt
            </a>
            <a
              href={pdfUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-gray-700 text-white px-4 py-2 rounded hover:bg-gray-800"
            >
              View Receipt
            </a>
          </div>
        </div>
      )}
    </div>
  );
};

export default GenerateReceipt;
