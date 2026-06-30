'use client';

import { useState } from 'react';
import { useAuth } from './lib/auth-context';
import { agentAPI } from './lib/api';
import { MessageSquare, Send, Bot, User, Shield } from 'lucide-react';

interface Message {
  id: number;
  type: 'user' | 'agent';
  content: string;
  timestamp: Date;
}

export default function Home() {
  const { isAuthenticated, user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      type: 'agent',
      content: 'Namaste! I am your JanSahayak AI assistant. I can help you discover government welfare schemes, verify your documents, and assist with applications. How can I help you today?',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: messages.length + 1,
      type: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages([...messages, userMessage]);
    setInput('');
    setLoading(true);

    try {
      if (!isAuthenticated) {
        // If not authenticated, prompt for login
        setTimeout(() => {
          const authMessage: Message = {
            id: messages.length + 2,
            type: 'agent',
            content: 'Please login with your Aadhaar and mobile number to access personalized assistance.',
            timestamp: new Date(),
          };
          setMessages((prev) => [...prev, authMessage]);
          setLoading(false);
        }, 500);
        return;
      }

      const response = await agentAPI.processQuery(input);
      
      const agentMessage: Message = {
        id: messages.length + 2,
        type: 'agent',
        content: `I've processed your request through our multi-agent system. ${response.data.message || 'Your query is being handled by the appropriate agents.'}`,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, agentMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: messages.length + 2,
        type: 'agent',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-primary-600 p-2 rounded-lg">
                <Bot className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">JanSahayak AI</h1>
                <p className="text-sm text-gray-600">Government Welfare Assistant</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              {isAuthenticated && user ? (
                <div className="flex items-center space-x-2">
                  <User className="h-5 w-5 text-gray-600" />
                  <span className="text-sm font-medium text-gray-700">{user.name}</span>
                </div>
              ) : (
                <a
                  href="/login"
                  className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition"
                >
                  Login
                </a>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Chat Interface */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-lg overflow-hidden">
              <div className="bg-primary-600 px-6 py-4">
                <div className="flex items-center space-x-3">
                  <MessageSquare className="h-6 w-6 text-white" />
                  <h2 className="text-xl font-semibold text-white">AI Assistant</h2>
                </div>
              </div>

              {/* Messages */}
              <div className="h-96 overflow-y-auto p-6 space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-md px-4 py-3 rounded-lg ${
                        message.type === 'user'
                          ? 'bg-primary-600 text-white'
                          : 'bg-gray-100 text-gray-900'
                      }`}
                    >
                      <p className="text-sm">{message.content}</p>
                      <p className="text-xs mt-1 opacity-70">
                        {message.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 px-4 py-3 rounded-lg">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Input */}
              <div className="border-t px-6 py-4">
                <div className="flex space-x-4">
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask about government schemes, document verification, or application status..."
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                    disabled={loading}
                  />
                  <button
                    onClick={handleSendMessage}
                    disabled={loading || !input.trim()}
                    className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition disabled:opacity-50"
                  >
                    <Send className="h-5 w-5" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Features Panel */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center space-x-3 mb-4">
                <Shield className="h-6 w-6 text-primary-600" />
                <h3 className="text-lg font-semibold text-gray-900">ArmorIQ Security</h3>
              </div>
              <p className="text-sm text-gray-600 mb-4">
                Your interactions are protected by our multi-agent security layer with real-time audit logging.
              </p>
              <div className="space-y-2">
                <div className="flex items-center space-x-2 text-sm">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-gray-700">Action verification</span>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-gray-700">Agent permission control</span>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-gray-700">Real-time audit logs</span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <a
                  href="/schemes"
                  className="block w-full text-left px-4 py-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
                >
                  <div className="font-medium text-gray-900">View Schemes</div>
                  <div className="text-sm text-gray-600">Browse eligible welfare schemes</div>
                </a>
                <a
                  href="/documents"
                  className="block w-full text-left px-4 py-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
                >
                  <div className="font-medium text-gray-900">Upload Documents</div>
                  <div className="text-sm text-gray-600">Verify your documents</div>
                </a>
                <a
                  href="/applications"
                  className="block w-full text-left px-4 py-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
                >
                  <div className="font-medium text-gray-900">My Applications</div>
                  <div className="text-sm text-gray-600">Track application status</div>
                </a>
                <a
                  href="/audit"
                  className="block w-full text-left px-4 py-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
                >
                  <div className="font-medium text-gray-900">Audit Dashboard</div>
                  <div className="text-sm text-gray-600">View security logs</div>
                </a>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
