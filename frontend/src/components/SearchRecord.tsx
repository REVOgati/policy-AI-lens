import React, { useState } from 'react';
import axios from 'axios';
import { apiConfig } from '../services/apiConfig';

interface SearchResult {
  [key: string]: string;
}

const SearchRecord: React.FC<{ onBack: () => void }> = ({ onBack }) => {
  const [policyHolder, setPolicyHolder] = useState('');
  const [registrationNo, setRegistrationNo] = useState('');
  const [expiryDate, setExpiryDate] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResults([]);
    try {
      const params: any = {};
      if (policyHolder) params.policy_holder = policyHolder;
      if (registrationNo) params.registration_no = registrationNo;
      if (expiryDate) params.expiry_date = expiryDate;
      const response = await axios.get(`${apiConfig.baseUrl}/api/v1/search`, { params });
      let data = response.data;
      // Ensure data is always an array
      if (!Array.isArray(data)) {
        data = [];
      }
      setResults(data);
      if (data.length === 0) setError('No records found.');
    } catch (err: any) {
      setError('Search failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-8 mt-8">
      <button onClick={onBack} className="mb-4 text-blue-600 hover:underline">&larr; Back</button>
      <h2 className="text-2xl font-bold mb-4 text-blue-900">Search Record</h2>
      <form onSubmit={handleSearch} className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Policy Holder</label>
          <input type="text" value={policyHolder} onChange={e => setPolicyHolder(e.target.value)} className="w-full border rounded px-3 py-2" placeholder="e.g. John Doe" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Registration No.</label>
          <input type="text" value={registrationNo} onChange={e => setRegistrationNo(e.target.value)} className="w-full border rounded px-3 py-2" placeholder="e.g. KDA123A" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Expiry Date</label>
          <input type="text" value={expiryDate} onChange={e => setExpiryDate(e.target.value)} className="w-full border rounded px-3 py-2" placeholder="DD/MM/YYYY" />
        </div>
        <div className="md:col-span-3 flex justify-end">
          <button type="submit" className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700" disabled={loading}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>
      {error && <div className="text-red-600 mb-4">{error}</div>}
      {Array.isArray(results) && results.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full border text-sm">
            <thead>
              <tr>
                {Object.keys(results[0]).map(key => (
                  <th key={key} className="border px-2 py-1 bg-blue-50 text-blue-900 font-semibold">{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {results.map((row, i) => (
                <tr key={i} className="hover:bg-blue-50">
                  {Object.values(row).map((val, j) => (
                    <td key={j} className="border px-2 py-1">{val}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default SearchRecord;
