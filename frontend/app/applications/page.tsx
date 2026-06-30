'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '../lib/auth-context';
import { applicationAPI, schemeAPI } from '../lib/api';
import { FileText, Clock, CheckCircle, XCircle, AlertCircle, Eye } from 'lucide-react';
import { useRouter, useSearchParams } from 'next/navigation';

interface Application {
  id: number;
  scheme_id: number;
  status: string;
  eligibility_score: number | null;
  rejection_reason: string | null;
  submitted_at: string | null;
  created_at: string;
}

interface Scheme {
  id: number;
  scheme_name: string;
}

export default function ApplicationsPage() {
  const { user } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const schemeIdFromUrl = searchParams.get('scheme_id');
  
  const [applications, setApplications] = useState<Application[]>([]);
  const [schemes, setSchemes] = useState<{ [key: number]: Scheme }>({});
  const [loading, setLoading] = useState(true);
  const [selectedApplication, setSelectedApplication] = useState<Application | null>(null);

  useEffect(() => {
    fetchApplications();
    fetchSchemes();
    
    // If scheme_id is in URL, prompt to create application
    if (schemeIdFromUrl) {
      createApplication(parseInt(schemeIdFromUrl));
    }
  }, [schemeIdFromUrl]);

  const fetchApplications = async () => {
    try {
      const response = await applicationAPI.getApplications();
      setApplications(response.data);
    } catch (error) {
      console.error('Failed to fetch applications:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchSchemes = async () => {
    try {
      const response = await schemeAPI.getSchemes();
      const schemeMap: { [key: number]: Scheme } = {};
      response.data.forEach((scheme: Scheme) => {
        schemeMap[scheme.id] = scheme;
      });
      setSchemes(schemeMap);
    } catch (error) {
      console.error('Failed to fetch schemes:', error);
    }
  };

  const createApplication = async (schemeId: number) => {
    try {
      await applicationAPI.createApplication({ scheme_id: schemeId });
      alert('Application created successfully!');
      fetchApplications();
    } catch (error) {
      console.error('Failed to create application:', error);
      alert('Failed to create application. Please try again.');
    }
  };

  const submitApplication = async (applicationId: number) => {
    if (!confirm('Are you sure you want to submit this application?')) return;

    try {
      await applicationAPI.submitApplication(applicationId);
      alert('Application submitted successfully!');
      fetchApplications();
    } catch (error) {
      console.error('Failed to submit application:', error);
      alert('Failed to submit application. Please try again.');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'approved':
        return 'bg-green-100 text-green-800';
      case 'rejected':
        return 'bg-red-100 text-red-800';
      case 'submitted':
      case 'under_review':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-yellow-100 text-yellow-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'approved':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'rejected':
        return <XCircle className="h-5 w-5 text-red-600" />;
      case 'submitted':
      case 'under_review':
        return <Clock className="h-5 w-5 text-blue-600" />;
      default:
        return <AlertCircle className="h-5 w-5 text-yellow-600" />;
    }
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Please login to view your applications</p>
          <a href="/login" className="text-primary-600 hover:underline">
            Go to Login
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Applications</h1>
          <p className="text-gray-600 mt-2">Track and manage your scheme applications</p>
        </div>

        {/* Applications List */}
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <div className="px-6 py-4 border-b">
            <h2 className="text-xl font-semibold text-gray-900">Application Status</h2>
          </div>

          {loading ? (
            <div className="p-6 text-center text-gray-600">Loading applications...</div>
          ) : applications.length === 0 ? (
            <div className="p-6 text-center text-gray-600">
              <FileText className="h-12 w-12 mx-auto mb-4 text-gray-400" />
              <p className="mb-4">No applications yet</p>
              <a
                href="/schemes"
                className="inline-block bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition"
              >
                Browse Schemes
              </a>
            </div>
          ) : (
            <div className="divide-y">
              {applications.map((app) => {
                const scheme = schemes[app.scheme_id];
                
                return (
                  <div key={app.id} className="p-6 hover:bg-gray-50 transition">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <div className="bg-primary-100 p-3 rounded-lg">
                          <FileText className="h-6 w-6 text-primary-600" />
                        </div>
                        <div>
                          <h3 className="font-medium text-gray-900">
                            {scheme?.scheme_name || 'Unknown Scheme'}
                          </h3>
                          <p className="text-sm text-gray-600">
                            Application ID: {app.id}
                          </p>
                          <p className="text-xs text-gray-500 mt-1">
                            Created: {new Date(app.created_at).toLocaleDateString()}
                            {app.submitted_at && ` • Submitted: ${new Date(app.submitted_at).toLocaleDateString()}`}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center space-x-4">
                        <div className="flex items-center space-x-2">
                          {getStatusIcon(app.status)}
                          <span
                            className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(
                              app.status
                            )}`}
                          >
                            {app.status.replace(/_/g, ' ').toUpperCase()}
                          </span>
                        </div>

                        {app.eligibility_score !== null && (
                          <div className="text-right">
                            <p className="text-xs text-gray-600">Eligibility Score</p>
                            <p className="font-bold text-primary-600">{app.eligibility_score}%</p>
                          </div>
                        )}

                        <button
                          onClick={() => setSelectedApplication(app)}
                          className="text-primary-600 hover:text-primary-700"
                        >
                          <Eye className="h-5 w-5" />
                        </button>

                        {app.status === 'draft' && (
                          <button
                            onClick={() => submitApplication(app.id)}
                            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition text-sm font-medium"
                          >
                            Submit
                          </button>
                        )}
                      </div>
                    </div>

                    {app.rejection_reason && (
                      <div className="mt-4 p-3 bg-red-50 rounded-lg">
                        <p className="text-sm text-red-800">
                          <strong>Rejection Reason:</strong> {app.rejection_reason}
                        </p>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Application Details Modal */}
        {selectedApplication && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <h2 className="text-2xl font-bold text-gray-900">Application Details</h2>
                  <button
                    onClick={() => setSelectedApplication(null)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <XCircle className="h-6 w-6" />
                  </button>
                </div>

                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">Application ID</p>
                      <p className="font-medium text-gray-900">{selectedApplication.id}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Scheme</p>
                      <p className="font-medium text-gray-900">
                        {schemes[selectedApplication.scheme_id]?.scheme_name || 'Unknown'}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Status</p>
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(selectedApplication.status)}
                        <span className="font-medium text-gray-900">
                          {selectedApplication.status.replace(/_/g, ' ').toUpperCase()}
                        </span>
                      </div>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Eligibility Score</p>
                      <p className="font-medium text-gray-900">
                        {selectedApplication.eligibility_score ?? 'N/A'}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Created</p>
                      <p className="font-medium text-gray-900">
                        {new Date(selectedApplication.created_at).toLocaleString()}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Submitted</p>
                      <p className="font-medium text-gray-900">
                        {selectedApplication.submitted_at
                          ? new Date(selectedApplication.submitted_at).toLocaleString()
                          : 'Not submitted'}
                      </p>
                    </div>
                  </div>

                  {selectedApplication.rejection_reason && (
                    <div className="p-4 bg-red-50 rounded-lg">
                      <p className="font-medium text-red-900 mb-1">Rejection Reason</p>
                      <p className="text-red-800">{selectedApplication.rejection_reason}</p>
                    </div>
                  )}

                  {selectedApplication.status === 'draft' && (
                    <button
                      onClick={() => {
                        submitApplication(selectedApplication.id);
                        setSelectedApplication(null);
                      }}
                      className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition font-medium"
                    >
                      Submit Application
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
