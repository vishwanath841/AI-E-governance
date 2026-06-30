'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '../lib/auth-context';
import { documentAPI } from '../lib/api';
import { Upload, FileText, CheckCircle, XCircle, Trash2, Eye } from 'lucide-react';

interface Document {
  id: number;
  file_name: string;
  document_type: string;
  verification_status: string;
  created_at: string;
}

export default function DocumentsPage() {
  const { user } = useAuth();
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [documentType, setDocumentType] = useState('');

  const documentTypes = [
    'aadhaar_card',
    'pan_card',
    'income_certificate',
    'residence_proof',
    'bank_statement',
    'other',
  ];

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await documentAPI.getDocuments();
      setDocuments(response.data);
    } catch (error) {
      console.error('Failed to fetch documents:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile || !documentType) {
      alert('Please select a file and document type');
      return;
    }

    setUploading(true);
    try {
      await documentAPI.upload(selectedFile, documentType);
      alert('Document uploaded successfully!');
      setSelectedFile(null);
      setDocumentType('');
      fetchDocuments();
    } catch (error) {
      console.error('Failed to upload document:', error);
      alert('Failed to upload document. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleVerify = async (id: number) => {
    try {
      await documentAPI.verifyDocument(id);
      alert('Document verification initiated!');
      fetchDocuments();
    } catch (error) {
      console.error('Failed to verify document:', error);
      alert('Failed to verify document. Please try again.');
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this document?')) return;

    try {
      await documentAPI.deleteDocument(id);
      alert('Document deleted successfully!');
      fetchDocuments();
    } catch (error) {
      console.error('Failed to delete document:', error);
      alert('Failed to delete document. Please try again.');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'verified':
        return 'bg-green-100 text-green-800';
      case 'rejected':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-yellow-100 text-yellow-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'verified':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'rejected':
        return <XCircle className="h-5 w-5 text-red-600" />;
      default:
        return <Eye className="h-5 w-5 text-yellow-600" />;
    }
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Please login to view your documents</p>
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
          <h1 className="text-3xl font-bold text-gray-900">Documents</h1>
          <p className="text-gray-600 mt-2">Upload and verify your documents</p>
        </div>

        {/* Upload Section */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Upload New Document</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Document Type
              </label>
              <select
                value={documentType}
                onChange={(e) => setDocumentType(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Select document type</option>
                {documentTypes.map((type) => (
                  <option key={type} value={type}>
                    {type.replace(/_/g, ' ').toUpperCase()}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                File
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                <input
                  type="file"
                  onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                  accept=".pdf,.jpg,.jpeg,.png"
                  className="hidden"
                  id="file-upload"
                />
                <label
                  htmlFor="file-upload"
                  className="cursor-pointer flex flex-col items-center"
                >
                  <Upload className="h-8 w-8 text-gray-400 mb-2" />
                  <p className="text-sm text-gray-600">
                    {selectedFile ? selectedFile.name : 'Click to upload or drag and drop'}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">PDF, JPG, PNG up to 10MB</p>
                </label>
              </div>
            </div>

            <button
              onClick={handleUpload}
              disabled={uploading || !selectedFile || !documentType}
              className="w-full bg-primary-600 text-white py-3 rounded-lg hover:bg-primary-700 transition disabled:opacity-50 font-medium"
            >
              {uploading ? 'Uploading...' : 'Upload Document'}
            </button>
          </div>
        </div>

        {/* Documents List */}
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <div className="px-6 py-4 border-b">
            <h2 className="text-xl font-semibold text-gray-900">Your Documents</h2>
          </div>

          {loading ? (
            <div className="p-6 text-center text-gray-600">Loading documents...</div>
          ) : documents.length === 0 ? (
            <div className="p-6 text-center text-gray-600">
              No documents uploaded yet
            </div>
          ) : (
            <div className="divide-y">
              {documents.map((doc) => (
                <div key={doc.id} className="p-6 hover:bg-gray-50 transition">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="bg-primary-100 p-3 rounded-lg">
                        <FileText className="h-6 w-6 text-primary-600" />
                      </div>
                      <div>
                        <h3 className="font-medium text-gray-900">{doc.file_name}</h3>
                        <p className="text-sm text-gray-600">
                          {doc.document_type.replace(/_/g, ' ').toUpperCase()}
                        </p>
                        <p className="text-xs text-gray-500 mt-1">
                          Uploaded: {new Date(doc.created_at).toLocaleDateString()}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(doc.verification_status)}
                        <span
                          className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(
                            doc.verification_status
                          )}`}
                        >
                          {doc.verification_status.toUpperCase()}
                        </span>
                      </div>

                      {doc.verification_status === 'pending' && (
                        <button
                          onClick={() => handleVerify(doc.id)}
                          className="text-primary-600 hover:text-primary-700"
                        >
                          Verify
                        </button>
                      )}

                      <button
                        onClick={() => handleDelete(doc.id)}
                        className="text-red-600 hover:text-red-700"
                      >
                        <Trash2 className="h-5 w-5" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
