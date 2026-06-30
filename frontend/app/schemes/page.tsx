'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '../lib/auth-context';
import { schemeAPI } from '../lib/api';
import { Search, CheckCircle, XCircle, Info, Zap } from 'lucide-react';

interface Scheme {
  id: number;
  scheme_name: string;
  description: string;
  benefits: string;
  required_documents: string;
}

interface EligibilityResult {
  scheme_id: number;
  scheme_name: string;
  is_eligible: boolean;
  eligibility_score: number;
  missing_documents: string[];
  reasons: string[];
}

export default function SchemesPage() {
  const { user } = useAuth();
  const [schemes, setSchemes] = useState<Scheme[]>([]);
  const [eligibilityResults, setEligibilityResults] = useState<EligibilityResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [checkingEligibility, setCheckingEligibility] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedScheme, setSelectedScheme] = useState<Scheme | null>(null);

  useEffect(() => {
    fetchSchemes();
  }, []);

  const fetchSchemes = async () => {
    try {
      const response = await schemeAPI.getSchemes();
      setSchemes(response.data);
    } catch (error) {
      console.error('Failed to fetch schemes:', error);
    } finally {
      setLoading(false);
    }
  };

  const checkEligibility = async () => {
    if (!user) {
      alert('Please login to check eligibility');
      return;
    }

    setCheckingEligibility(true);
    try {
      // Mock user profile - in production, this would come from user data
      const userProfile = {
        user_id: user.id,
        name: user.name,
        income: 200000,
        age: 30,
        residence_type: 'urban',
        employment_status: 'employed',
        family_size: 4,
        has_disability: false,
        is_bpl: false,
        documents: ['aadhaar_card', 'pan_card'],
      };

      const response = await schemeAPI.checkEligibility(userProfile);
      setEligibilityResults(response.data);
    } catch (error) {
      console.error('Failed to check eligibility:', error);
      alert('Failed to check eligibility. Please try again.');
    } finally {
      setCheckingEligibility(false);
    }
  };

  const filteredSchemes = schemes.filter((scheme) =>
    scheme.scheme_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    scheme.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getEligibilityForScheme = (schemeId: number) => {
    return eligibilityResults.find((result) => result.scheme_id === schemeId);
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Please login to view schemes</p>
          <a href="/login" className="text-primary-600 hover:underline">
            Go to Login
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Government Welfare Schemes</h1>
          <p className="text-gray-600 mt-2">Discover and apply for government welfare schemes</p>
        </div>

        {/* Search and Actions */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search schemes..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <button
              onClick={checkEligibility}
              disabled={checkingEligibility}
              className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition disabled:opacity-50 font-medium flex items-center space-x-2"
            >
              <Zap className="h-5 w-5" />
              <span>{checkingEligibility ? 'Checking...' : 'Check My Eligibility'}</span>
            </button>
          </div>
        </div>

        {/* Schemes Grid */}
        {loading ? (
          <div className="text-center text-gray-600">Loading schemes...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredSchemes.map((scheme) => {
              const eligibility = getEligibilityForScheme(scheme.id);
              
              return (
                <div
                  key={scheme.id}
                  className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition"
                >
                  <div className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <h3 className="text-lg font-semibold text-gray-900">{scheme.scheme_name}</h3>
                      {eligibility && (
                        <div className="flex items-center space-x-1">
                          {eligibility.is_eligible ? (
                            <CheckCircle className="h-5 w-5 text-green-600" />
                          ) : (
                            <XCircle className="h-5 w-5 text-red-600" />
                          )}
                        </div>
                      )}
                    </div>

                    <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                      {scheme.description || 'No description available'}
                    </p>

                    {eligibility && (
                      <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-medium text-gray-700">Eligibility Score</span>
                          <span className="text-sm font-bold text-primary-600">
                            {eligibility.eligibility_score}%
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-primary-600 h-2 rounded-full transition-all"
                            style={{ width: `${eligibility.eligibility_score}%` }}
                          />
                        </div>
                      </div>
                    )}

                    <button
                      onClick={() => setSelectedScheme(scheme)}
                      className="w-full bg-primary-600 text-white py-2 rounded-lg hover:bg-primary-700 transition font-medium"
                    >
                      View Details
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Scheme Details Modal */}
        {selectedScheme && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <h2 className="text-2xl font-bold text-gray-900">{selectedScheme.scheme_name}</h2>
                  <button
                    onClick={() => setSelectedScheme(null)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <XCircle className="h-6 w-6" />
                  </button>
                </div>

                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-2 flex items-center">
                      <Info className="h-5 w-5 mr-2" />
                      Description
                    </h3>
                    <p className="text-gray-600">{selectedScheme.description || 'No description available'}</p>
                  </div>

                  <div>
                    <h3 className="font-semibold text-gray-900 mb-2">Benefits</h3>
                    <p className="text-gray-600">{selectedScheme.benefits || 'No benefits information available'}</p>
                  </div>

                  <div>
                    <h3 className="font-semibold text-gray-900 mb-2">Required Documents</h3>
                    <div className="flex flex-wrap gap-2">
                      {JSON.parse(selectedScheme.required_documents || '[]').map((doc: string, index: number) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm"
                        >
                          {doc.replace(/_/g, ' ').toUpperCase()}
                        </span>
                      ))}
                    </div>
                  </div>

                  <a
                    href={`/applications?scheme_id=${selectedScheme.id}`}
                    className="block w-full bg-primary-600 text-white py-3 rounded-lg hover:bg-primary-700 transition font-medium text-center"
                  >
                    Apply Now
                  </a>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
