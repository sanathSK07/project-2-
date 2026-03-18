import { useRef, useEffect, useState } from 'react';
import { Send, Sparkles } from 'lucide-react';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';

/**
 * Suggested quick questions shown when the chat is empty.
 * @type {string[]}
 */
const QUICK_QUESTIONS = [
  'How do I reset my password?',
  'VPN is not connecting',
  'Set up email on my phone',
  'Request new software',
];

/**
 * Main chat area: message list, quick-start suggestions, text input, and send button.
 *
 * @param {Object} props
 * @param {Array} props.messages - Chat messages
 * @param {boolean} props.loading - Whether the assistant is typing
 * @param {(text: string) => void} props.onSend - Send handler
 * @param {Function} props.onFeedback - Feedback handler
 */
export default function ChatWindow({ messages, loading, onSend, onFeedback }) {
  const [input, setInput] = useState('');
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  /** Auto-scroll to bottom on new messages. */
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  /** Focus input on mount. */
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  /** Submit handler. */
  const handleSubmit = (e) => {
    e?.preventDefault();
    if (!input.trim() || loading) return;
    onSend(input.trim());
    setInput('');
  };

  /** Quick question click. */
  const handleQuick = (text) => {
    onSend(text);
  };

  return (
    <div className="flex flex-col flex-1 min-h-0">
      {/* ── Messages area ─────────────────────────────── */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6">
        {messages.length === 0 ? (
          /* ── Empty state with quick suggestions ────── */
          <div className="flex flex-col items-center justify-center h-full animate-fade-in">
            <div className="w-16 h-16 rounded-2xl bg-accent/10 flex items-center justify-center mb-6">
              <Sparkles size={28} className="text-accent" />
            </div>
            <h2 className="text-xl font-semibold text-white mb-2">
              How can I help you?
            </h2>
            <p className="text-sm text-navy-400 mb-8 text-center max-w-md">
              I can assist with password resets, VPN issues, software requests, and
              other IT support topics.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-lg">
              {QUICK_QUESTIONS.map((q) => (
                <button
                  key={q}
                  onClick={() => handleQuick(q)}
                  className="text-left px-4 py-3 rounded-xl bg-navy-800 border border-navy-700 text-sm text-navy-300 hover:border-accent/40 hover:text-white transition-default"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg, i) => (
              <MessageBubble
                key={i}
                message={msg}
                index={i}
                onFeedback={onFeedback}
              />
            ))}
            {loading && <TypingIndicator />}
          </>
        )}
        <div ref={bottomRef} />
      </div>

      {/* ── Input bar ─────────────────────────────────── */}
      <form
        onSubmit={handleSubmit}
        className="shrink-0 border-t border-navy-700 bg-navy-800/50 px-4 py-3"
      >
        <div className="flex items-center gap-3 max-w-3xl mx-auto">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe your IT issue..."
            className="flex-1 bg-navy-900 border border-navy-600 rounded-xl px-4 py-3 text-sm text-white placeholder-navy-500 focus:outline-none focus:border-accent transition-default"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="p-3 rounded-xl bg-accent text-white hover:bg-accent-hover disabled:opacity-40 disabled:cursor-not-allowed transition-default"
            aria-label="Send message"
          >
            <Send size={18} />
          </button>
        </div>
      </form>
    </div>
  );
}
