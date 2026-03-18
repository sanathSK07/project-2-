import { useState } from 'react';
import { User, Bot, ChevronDown, ChevronUp, ExternalLink } from 'lucide-react';
import FeedbackWidget from './FeedbackWidget';

/**
 * Renders a single chat message bubble.
 *
 * @param {Object} props
 * @param {Object} props.message - Message data
 * @param {string} props.message.role - "user" | "assistant"
 * @param {string} props.message.content - Message text
 * @param {Array}  [props.message.sources] - Source citations
 * @param {number} [props.message.confidence] - Confidence score 0-1
 * @param {boolean} [props.message.escalated] - Whether the issue was escalated
 * @param {string} [props.message.ticket_id] - Support ticket id if escalated
 * @param {string} [props.message.feedback] - Already-submitted feedback
 * @param {number} props.index - Message index in array
 * @param {Function} props.onFeedback - Feedback submission handler
 */
export default function MessageBubble({ message, index, onFeedback }) {
  const [sourcesOpen, setSourcesOpen] = useState(false);
  const isUser = message.role === 'user';

  /**
   * Map a confidence score to a colour and label.
   * @param {number} score
   */
  const confidenceBadge = (score) => {
    if (score >= 0.75) return { color: 'bg-green-500', label: 'High' };
    if (score >= 0.45) return { color: 'bg-amber-500', label: 'Medium' };
    return { color: 'bg-red-500', label: 'Low' };
  };

  return (
    <div
      className={`flex items-start gap-3 message-enter ${
        isUser ? 'flex-row-reverse' : ''
      }`}
    >
      {/* ── Avatar ─────────────────────────────────────── */}
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
          isUser ? 'bg-accent' : 'bg-navy-700'
        }`}
      >
        {isUser ? (
          <User size={16} className="text-white" />
        ) : (
          <Bot size={16} className="text-accent" />
        )}
      </div>

      {/* ── Bubble ─────────────────────────────────────── */}
      <div
        className={`max-w-[75%] rounded-2xl px-4 py-3 ${
          isUser
            ? 'bg-accent text-white rounded-tr-sm'
            : 'bg-navy-800 border border-navy-700 text-gray-200 rounded-tl-sm'
        }`}
      >
        {/* Message text */}
        <p className="text-sm leading-relaxed whitespace-pre-wrap">
          {message.content}
        </p>

        {/* ── Confidence indicator ────────────────────── */}
        {!isUser && message.confidence != null && (
          <div className="flex items-center gap-1.5 mt-2">
            <span
              className={`w-2 h-2 rounded-full ${
                confidenceBadge(message.confidence).color
              }`}
            />
            <span className="text-xs text-navy-400">
              {confidenceBadge(message.confidence).label} confidence (
              {Math.round(message.confidence * 100)}%)
            </span>
          </div>
        )}

        {/* ── Source citations ────────────────────────── */}
        {!isUser && message.sources?.length > 0 && (
          <div className="mt-2">
            <button
              onClick={() => setSourcesOpen((o) => !o)}
              className="flex items-center gap-1 text-xs text-accent hover:text-accent-light transition-default"
            >
              {sourcesOpen ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
              {message.sources.length} source
              {message.sources.length !== 1 && 's'}
            </button>

            {sourcesOpen && (
              <div className="mt-1.5 flex flex-wrap gap-1.5">
                {message.sources.map((src, i) => (
                  <span
                    key={i}
                    className="inline-flex items-center gap-1 px-2 py-0.5 bg-navy-700 rounded-full text-xs text-navy-300"
                  >
                    <ExternalLink size={10} />
                    {typeof src === 'string' ? src : (src.title ?? src.source ?? `Source ${i + 1}`)}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}

        {/* ── Escalation alert ───────────────────────── */}
        {!isUser && message.escalated && (
          <div className="mt-3 p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20">
            <p className="text-xs font-medium text-amber-400">
              Escalated to IT Support
            </p>
            {message.ticket_id && (
              <p className="text-xs text-amber-500/70 mt-0.5">
                Ticket #{message.ticket_id}
              </p>
            )}
          </div>
        )}

        {/* ── Feedback ───────────────────────────────── */}
        {!isUser && !message.error && (
          <FeedbackWidget
            messageIndex={index}
            currentFeedback={message.feedback}
            onSubmit={onFeedback}
          />
        )}
      </div>
    </div>
  );
}
