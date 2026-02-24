import React, { useState } from "react";
import axios from "axios";
import { apiConfig } from "../services/apiConfig";
import type { PolicyData } from "../types/policy";

interface Props {
  formData: PolicyData;
  onClose: () => void;
  onReceiptGenerated?: (url: string) => void;
}

const RECEIPT_FIELDS: (keyof PolicyData)[] = [
  "policy_number",
  "policy_holder",
  "policy_type",
  "commencing_date",
  "expiring_date",
  "premium_amount",
  "paid_amount",
  "balance_amount",
  "registration_no",
  "vehicle_type",
];

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

const GenerateReceiptModal: React.FC<Props> = ({ formData, onClose }) => {
  const [fields, setFields] = useState(() => {
    const obj: Record<string, string> = {};
    RECEIPT_FIELDS.forEach((key) => {
      obj[key] = formData[key] || "";
    });
    return obj;
  });
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFields({ ...fields, [e.target.name]: e.target.value });
  };

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPdfUrl(null);
    try {
      const response = await axios.post(
        `${apiConfig.baseUrl}/api/v1/receipt/generate`,
        fields,
        { responseType: "blob" }
      );
      const url = window.URL.createObjectURL(new Blob([response.data], { type: "application/pdf" }));
      setPdfUrl(url);
      if (onReceiptGenerated) onReceiptGenerated(url);
      onClose(); // Close modal immediately after successful generation
    } catch (err: any) {
      setError("Failed to generate receipt.");
    }
    setLoading(false);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-lg relative max-h-screen overflow-y-auto p-4 sm:p-6">
        <button onClick={onClose} className="absolute top-2 right-2 text-gray-500 hover:text-black">&times;</button>
        <h2 className="text-xl font-bold mb-4 text-blue-800 text-center">Edit & Generate Receipt</h2>
        <form onSubmit={handleGenerate} className="space-y-2">
          {RECEIPT_FIELDS.map((key) => (
            <div key={key}>
              <label className="block font-semibold capitalize mb-1">{fieldLabels[key]}</label>
              <input
                type="text"
                name={key}
                value={fields[key]}
                onChange={handleChange}
                className="w-full border rounded px-2 py-1"
                required
              />
            </div>
          ))}
          <button
            type="submit"
            className="bg-blue-700 text-white px-4 py-2 rounded hover:bg-blue-800 w-full"
            disabled={loading}
          >
            {loading ? "Generating..." : "Generate Receipt"}
          </button>
        </form>
        {error && <div className="text-red-600 mt-2 text-center">{error}</div>}
        {pdfUrl && (
          <div className="mt-4 flex flex-col sm:flex-row gap-2 justify-center">
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
        )}
      </div>
    </div>
  );
};

export default GenerateReceiptModal;
