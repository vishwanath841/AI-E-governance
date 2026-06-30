'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '../lib/auth-context';
import { userAPI } from '../lib/api';
import { User, Mail, Phone, Shield, Edit2, Save, X } from 'lucide-react';

export default function ProfilePage() {
  const { user, logout } = useAuth();
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [profileData, setProfileData] = useState({
    name: '',
    email: '',
  });

  useEffect(() => {
    if (user) {
      setProfileData({
        name: user.name,
        email: user.email || '',
      });
    }
  }, [user]);

  const handleSave = async () => {
    setLoading(true);
    try {
      await userAPI.updateProfile(profileData);
      setEditing(false);
      alert('Profile updated successfully!');
    } catch (error) {
      console.error('Failed to update profile:', error);
      alert('Failed to update profile. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setProfileData({
      name: user?.name || '',
      email: user?.email || '',
    });
    setEditing(false);
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Please login to view your profile</p>
          <a href="/login" className="text-primary-600 hover:underline">
            Go to Login
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">User Profile</h1>
          <p className="text-gray-600 mt-2">Manage your account information</p>
        </div>

        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          {/* Profile Header */}
          <div className="bg-primary-600 px-6 py-8">
            <div className="flex items-center space-x-4">
              <div className="bg-white p-3 rounded-full">
                <User className="h-8 w-8 text-primary-600" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">{user.name}</h2>
                <p className="text-primary-100">Citizen ID: {user.aadhaar}</p>
              </div>
            </div>
          </div>

          {/* Profile Details */}
          <div className="p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg font-semibold text-gray-900">Personal Information</h3>
              {!editing ? (
                <button
                  onClick={() => setEditing(true)}
                  className="flex items-center space-x-2 text-primary-600 hover:text-primary-700"
                >
                  <Edit2 className="h-4 w-4" />
                  <span>Edit</span>
                </button>
              ) : (
                <div className="flex space-x-2">
                  <button
                    onClick={handleSave}
                    disabled={loading}
                    className="flex items-center space-x-2 bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 disabled:opacity-50"
                  >
                    <Save className="h-4 w-4" />
                    <span>{loading ? 'Saving...' : 'Save'}</span>
                  </button>
                  <button
                    onClick={handleCancel}
                    className="flex items-center space-x-2 bg-gray-600 text-white px-3 py-1 rounded hover:bg-gray-700"
                  >
                    <X className="h-4 w-4" />
                    <span>Cancel</span>
                  </button>
                </div>
              )}
            </div>

            <div className="space-y-4">
              <div className="flex items-start space-x-4">
                <User className="h-5 w-5 text-gray-400 mt-1" />
                <div className="flex-1">
                  <p className="text-sm text-gray-600">Full Name</p>
                  {editing ? (
                    <input
                      type="text"
                      value={profileData.name}
                      onChange={(e) => setProfileData({ ...profileData, name: e.target.value })}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                    />
                  ) : (
                    <p className="font-medium text-gray-900">{user.name}</p>
                  )}
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <Shield className="h-5 w-5 text-gray-400 mt-1" />
                <div className="flex-1">
                  <p className="text-sm text-gray-600">Aadhaar Number</p>
                  <p className="font-medium text-gray-900">{user.aadhaar}</p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <Phone className="h-5 w-5 text-gray-400 mt-1" />
                <div className="flex-1">
                  <p className="text-sm text-gray-600">Mobile Number</p>
                  <p className="font-medium text-gray-900">{user.mobile}</p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <Mail className="h-5 w-5 text-gray-400 mt-1" />
                <div className="flex-1">
                  <p className="text-sm text-gray-600">Email</p>
                  {editing ? (
                    <input
                      type="email"
                      value={profileData.email}
                      onChange={(e) => setProfileData({ ...profileData, email: e.target.value })}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                      placeholder="your@email.com"
                    />
                  ) : (
                    <p className="font-medium text-gray-900">{user.email || 'Not provided'}</p>
                  )}
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <Shield className="h-5 w-5 text-gray-400 mt-1" />
                <div className="flex-1">
                  <p className="text-sm text-gray-600">Verification Status</p>
                  <span
                    className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
                      user.is_verified
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}
                  >
                    {user.is_verified ? 'Verified' : 'Pending'}
                  </span>
                </div>
              </div>
            </div>

            <div className="mt-8 pt-6 border-t">
              <button
                onClick={logout}
                className="w-full bg-red-600 text-white py-3 rounded-lg hover:bg-red-700 transition font-medium"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
