import { Bot } from 'lucide-react';

/**
 * Animated typing indicator shown while the assistant is generating a response.
 * Renders three bouncing dots inside a chat-bubble frame.
 */
export default function TypingIndicator() {
  return (
    <div className="flex items-start gap-3 message-enter">
      <div className="w-8 h-8 rounded-full bg-navy-700 flex items-center justify-center shrink-0">
        <Bot size={16} className="text-accent" />
      </div>
      <div className="bg-navy-800 border border-navy-700 rounded-2xl rounded-tl-sm px-5 py-3">
        <div className="flex items-center gap-1.5">
          <span className="typing-dot w-2 h-2 rounded-full bg-accent/70" />
          <span className="typing-dot w-2 h-2 rounded-full bg-accent/70" />
          <span className="typing-dot w-2 h-2 rounded-full bg-accent/70" />
        </div>
      </div>
    </div>
  );
}
