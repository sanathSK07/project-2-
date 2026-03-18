import { useState } from 'react';
import { ThumbsUp, ThumbsDown, Send } from 'lucide-react';

/**
 * Inline feedback widget for a single bot message.
 * Shows thumbs up / thumbs down buttons, and an optional comment field
 * when "not helpful" is selected.
 *
 * @param {Object} props
 * @param {number} props.messageIndex - Index of the message in the chat array
 * @param {'helpful'|'not_helpful'|undefined} props.currentFeedback - Already-submitted feedback
 * @param {(index: number, rating: string, comment?: string) => Promise<void>} props.onSubmit
 */
export default function FeedbackWidget({ messageIndex, currentFeedback, onSubmit }) {
  const [showComment, setShowComment] = useState(false);
  const [comment, setComment] = useState('');
  const [submitting, setSubmitting] = useState(false);

  /** Handle a rating click. */
  const handleRate = async (rating) => {
    if (currentFeedback) return; // already rated
    if (rating === 'not_helpful') {
      setShowComment(true);
      return;
    }
    setSubmitting(true);
    await onSubmit(messageIndex, rating);
    setSubmitting(false);
  };

  /** Submit the "not helpful" feedback with optional comment. */
  const handleSubmitComment = async () => {
    setSubmitting(true);
    await onSubmit(messageIndex, 'not_helpful', comment);
    setShowComment(false);
    setSubmitting(false);
  };

  if (currentFeedback) {
    return (
      <div className="flex items-center gap-1.5 mt-2 text-xs text-navy-500">
        {currentFeedback === 'helpful' ? (
          <>
            <ThumbsUp size={12} className="text-green-500" />
            <span>Helpful</span>
          </>
        ) : (
          <>
            <ThumbsDown size={12} className="text-red-400" />
            <span>Not helpful</span>
          </>
        )}
      </div>
    );
  }

  return (
    <div className="mt-2">
      {!showComment ? (
        <div className="flex items-center gap-2">
          <span className="text-xs text-navy-500">Was this helpful?</span>
          <button
            onClick={() => handleRate('helpful')}
            disabled={submitting}
            className="p-1 rounded hover:bg-green-500/10 text-navy-500 hover:text-green-500 transition-default disabled:opacity-50"
            aria-label="Helpful"
          >
            <ThumbsUp size={14} />
          </button>
          <button
            onClick={() => handleRate('not_helpful')}
            disabled={submitting}
            className="p-1 rounded hover:bg-red-500/10 text-navy-500 hover:text-red-400 transition-default disabled:opacity-50"
            aria-label="Not helpful"
          >
            <ThumbsDown size={14} />
          </button>
        </div>
      ) : (
        <div className="flex items-center gap-2 mt-1">
          <input
            type="text"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="What could be improved?"
            className="flex-1 bg-navy-900 border border-navy-600 rounded-lg px-3 py-1.5 text-xs text-white placeholder-navy-500 focus:outline-none focus:border-accent"
          />
          <button
            onClick={handleSubmitComment}
            disabled={submitting}
            className="p-1.5 rounded-lg bg-accent/20 text-accent hover:bg-accent/30 transition-default disabled:opacity-50"
            aria-label="Submit feedback"
          >
            <Send size={12} />
          </button>
        </div>
      )}
    </div>
  );
}
