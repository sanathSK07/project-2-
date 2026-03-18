import { useState } from 'react';
import axios from 'axios';
import Header from '../components/Header';
import {
  Shield,
  RefreshCw,
  CheckCircle2,
  XCircle,
  KeyRound,
  Loader2,
} from 'lucide-react';

/**
 * Admin dashboard page.
 * Protected by a simple API key input. Provides a reindex trigger button
 * and displays basic system status.
 */
export default function Admin() {
  const [apiKey, setApiKey] = useState('');
  const [authenticated, setAuthenticated] = useState(false);
  const [reindexing, setReindexing] = useState(false);
  const [statusMessage, setStatusMessage] = useState(null);
  const [statusType, setStatusType] = useState('info'); // 'success' | 'error' | 'info'

  /** Authenticate with the API key. */
  const handleAuth = (e) => {
    e.preventDefault();
    if (apiKey.trim()) {
      setAuthenticated(true);
    }
  };

  /** Trigger knowledge-base reindex. */
  const handleReindex = async () => {
    setReindexing(true);
    setStatusMessage(null);
    try {
      await axios.post(
        '/api/admin/reindex',
        {},
        { headers: { 'X-API-Key': apiKey } }
      );
      setStatusMessage('Knowledge base reindexed successfully.');
      setStatusType('success');
    } catch (err) {
      const msg =
        err.response?.data?.detail || 'Reindex failed. Check your API key.';
      setStatusMessage(msg);
      setStatusType('error');
    } finally {
      setReindexing(false);
    }
  };

  return (
    <div className="h-screen flex flex-col overflow-hidden">
      <Header />

      <div className="flex-1 overflow-y-auto p-6">
        <div className="max-w-2xl mx-auto">
          {/* ── Title ──────────────────────────────────── */}
          <div className="flex items-center gap-3 mb-8">
            <div className="w-10 h-10 rounded-xl bg-accent/10 flex items-center justify-center">
              <Shield size={22} className="text-accent" />
            </div>
            <div>
              <h1 className="text-xl font-semibold text-white">
                Admin Dashboard
              </h1>
              <p className="text-sm text-navy-400">
                Manage the IT HelpDesk AI knowledge base
              </p>
            </div>
          </div>

          {!authenticated ? (
            /* ── API Key gate ────────────────────────── */
            <form
              onSubmit={handleAuth}
              className="bg-navy-800 border border-navy-700 rounded-2xl p-6"
            >
              <div className="flex items-center gap-2 mb-4">
                <KeyRound size={18} className="text-navy-400" />
                <h2 className="text-sm font-medium text-white">
                  Enter Admin API Key
                </h2>
              </div>
              <div className="flex items-center gap-3">
                <input
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="Your API key"
                  className="flex-1 bg-navy-900 border border-navy-600 rounded-xl px-4 py-3 text-sm text-white placeholder-navy-500 focus:outline-none focus:border-accent transition-default"
                />
                <button
                  type="submit"
                  className="px-6 py-3 rounded-xl bg-accent text-white text-sm font-medium hover:bg-accent-hover transition-default"
                >
                  Authenticate
                </button>
              </div>
            </form>
          ) : (
            /* ── Authenticated controls ──────────────── */
            <div className="space-y-6">
              {/* Reindex card */}
              <div className="bg-navy-800 border border-navy-700 rounded-2xl p-6">
                <h2 className="text-sm font-medium text-white mb-2">
                  Knowledge Base
                </h2>
                <p className="text-sm text-navy-400 mb-4">
                  Trigger a full reindex of the IT knowledge base documents.
                </p>
                <button
                  onClick={handleReindex}
                  disabled={reindexing}
                  className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-accent text-white text-sm font-medium hover:bg-accent-hover disabled:opacity-50 transition-default"
                >
                  {reindexing ? (
                    <Loader2 size={16} className="animate-spin" />
                  ) : (
                    <RefreshCw size={16} />
                  )}
                  {reindexing ? 'Reindexing...' : 'Reindex Now'}
                </button>
              </div>

              {/* Status message */}
              {statusMessage && (
                <div
                  className={`flex items-start gap-3 p-4 rounded-xl border ${
                    statusType === 'success'
                      ? 'bg-green-500/10 border-green-500/20 text-green-400'
                      : 'bg-red-500/10 border-red-500/20 text-red-400'
                  }`}
                >
                  {statusType === 'success' ? (
                    <CheckCircle2 size={18} className="mt-0.5 shrink-0" />
                  ) : (
                    <XCircle size={18} className="mt-0.5 shrink-0" />
                  )}
                  <p className="text-sm">{statusMessage}</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
