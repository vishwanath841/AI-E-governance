'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '../lib/auth-context';
import { auditAPI, agentAPI } from '../lib/api';
import { Shield, AlertTriangle, CheckCircle, Activity, Filter, RefreshCw } from 'lucide-react';

interface AuditLog {
  id: number;
  timestamp: string;
  agent: string;
  action: string;
  result: string;
  details: string | null;
}

interface AgentActionLog {
  agent_name: string;
  action: string;
  allowed: boolean;
  reason: string | null;
  timestamp: string;
}

interface AuditSummary {
  database_stats: {
    total_logs: number;
    authorized: number;
    unauthorized: number;
    blocked: number;
  };
  armoriq_stats: {
    total_actions: number;
    authorized: number;
    blocked: number;
  };
  combined_total: number;
}

export default function AuditPage() {
  const { user } = useAuth();
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);
  const [agentActions, setAgentActions] = useState<AgentActionLog[]>([]);
  const [summary, setSummary] = useState<AuditSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'authorized' | 'blocked'>('all');
  const [agentFilter, setAgentFilter] = useState<string>('all');

  useEffect(() => {
    fetchAuditData();
  }, []);

  const fetchAuditData = async () => {
    try {
      const [logsRes, actionsRes, summaryRes] = await Promise.all([
        auditAPI.getAuditLogs(),
        auditAPI.getAgentActions(),
        auditAPI.getSummary(),
      ]);

      setAuditLogs(logsRes.data);
      setAgentActions(actionsRes.data);
      setSummary(summaryRes.data);
    } catch (error) {
      console.error('Failed to fetch audit data:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredLogs = auditLogs.filter((log) => {
    if (filter !== 'all' && log.result !== filter) return false;
    if (agentFilter !== 'all' && log.agent !== agentFilter) return false;
    return true;
  });

  const filteredActions = agentActions.filter((action) => {
    if (filter !== 'all') {
      if (filter === 'authorized' && !action.allowed) return false;
      if (filter === 'blocked' && action.allowed) return false;
    }
    if (agentFilter !== 'all' && action.agent_name !== agentFilter) return false;
    return true;
  });

  const getStatusColor = (result: string) => {
    switch (result) {
      case 'authorized':
        return 'bg-green-100 text-green-800';
      case 'unauthorized':
      case 'blocked':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (result: string) => {
    switch (result) {
      case 'authorized':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'unauthorized':
      case 'blocked':
        return <AlertTriangle className="h-5 w-5 text-red-600" />;
      default:
        return <Activity className="h-5 w-5 text-gray-600" />;
    }
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Please login to view audit logs</p>
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
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Audit Dashboard</h1>
              <p className="text-gray-600 mt-2">Monitor security events and agent actions</p>
            </div>
            <button
              onClick={fetchAuditData}
              disabled={loading}
              className="flex items-center space-x-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition disabled:opacity-50"
            >
              <RefreshCw className={`h-5 w-5 ${loading ? 'animate-spin' : ''}`} />
              <span>Refresh</span>
            </button>
          </div>
        </div>

        {/* Summary Cards */}
        {summary && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center space-x-3">
                <div className="bg-primary-100 p-3 rounded-lg">
                  <Activity className="h-6 w-6 text-primary-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total Actions</p>
                  <p className="text-2xl font-bold text-gray-900">{summary.combined_total}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center space-x-3">
                <div className="bg-green-100 p-3 rounded-lg">
                  <CheckCircle className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Authorized</p>
                  <p className="text-2xl font-bold text-green-600">
                    {summary.database_stats.authorized + summary.armoriq_stats.authorized}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center space-x-3">
                <div className="bg-red-100 p-3 rounded-lg">
                  <AlertTriangle className="h-6 w-6 text-red-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Blocked</p>
                  <p className="text-2xl font-bold text-red-600">
                    {summary.database_stats.blocked + summary.armoriq_stats.blocked}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center space-x-3">
                <div className="bg-blue-100 p-3 rounded-lg">
                  <Shield className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Security Rate</p>
                  <p className="text-2xl font-bold text-blue-600">
                    {summary.combined_total > 0
                      ? Math.round(
                          ((summary.database_stats.authorized + summary.armoriq_stats.authorized) /
                            summary.combined_total) *
                            100
                        )
                      : 0}
                    %
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex items-center space-x-2">
              <Filter className="h-5 w-5 text-gray-400" />
              <span className="font-medium text-gray-700">Filters:</span>
            </div>
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value as 'all' | 'authorized' | 'blocked')}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="all">All Actions</option>
              <option value="authorized">Authorized Only</option>
              <option value="blocked">Blocked Only</option>
            </select>
            <select
              value={agentFilter}
              onChange={(e) => setAgentFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="all">All Agents</option>
              <option value="coordinator_agent">Coordinator Agent</option>
              <option value="verification_agent">Verification Agent</option>
              <option value="document_agent">Document Agent</option>
              <option value="eligibility_agent">Eligibility Agent</option>
              <option value="submission_agent">Submission Agent</option>
              <option value="notification_agent">Notification Agent</option>
            </select>
          </div>
        </div>

        {/* Audit Logs */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Database Logs */}
          <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            <div className="px-6 py-4 border-b bg-gray-50">
              <h2 className="text-xl font-semibold text-gray-900">Database Audit Logs</h2>
            </div>
            <div className="max-h-96 overflow-y-auto">
              {loading ? (
                <div className="p-6 text-center text-gray-600">Loading...</div>
              ) : filteredLogs.length === 0 ? (
                <div className="p-6 text-center text-gray-600">No logs found</div>
              ) : (
                <div className="divide-y">
                  {filteredLogs.map((log) => (
                    <div key={log.id} className="p-4 hover:bg-gray-50 transition">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          {getStatusIcon(log.result)}
                          <span className="font-medium text-gray-900">{log.agent}</span>
                        </div>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(log.result)}`}>
                          {log.result}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mb-1">{log.action}</p>
                      {log.details && (
                        <p className="text-xs text-gray-500">{log.details}</p>
                      )}
                      <p className="text-xs text-gray-400 mt-2">
                        {new Date(log.timestamp).toLocaleString()}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* ArmorIQ Agent Actions */}
          <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            <div className="px-6 py-4 border-b bg-gray-50">
              <h2 className="text-xl font-semibold text-gray-900">ArmorIQ Agent Actions</h2>
            </div>
            <div className="max-h-96 overflow-y-auto">
              {loading ? (
                <div className="p-6 text-center text-gray-600">Loading...</div>
              ) : filteredActions.length === 0 ? (
                <div className="p-6 text-center text-gray-600">No actions found</div>
              ) : (
                <div className="divide-y">
                  {filteredActions.map((action, index) => (
                    <div key={index} className="p-4 hover:bg-gray-50 transition">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          {action.allowed ? (
                            <CheckCircle className="h-5 w-5 text-green-600" />
                          ) : (
                            <AlertTriangle className="h-5 w-5 text-red-600" />
                          )}
                          <span className="font-medium text-gray-900">{action.agent_name}</span>
                        </div>
                        <span
                          className={`px-2 py-1 rounded text-xs font-medium ${
                            action.allowed ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                          }`}
                        >
                          {action.allowed ? 'Allowed' : 'Blocked'}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mb-1">{action.action}</p>
                      {action.reason && (
                        <p className="text-xs text-gray-500">{action.reason}</p>
                      )}
                      <p className="text-xs text-gray-400 mt-2">
                        {new Date(action.timestamp).toLocaleString()}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
