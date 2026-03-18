import { useState, useCallback, useRef } from 'react';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';

/**
 * Custom hook that manages the full chat lifecycle.
 *
 * @returns {{
 *   messages: Array<{role: string, content: string, sources?: Array, confidence?: number, escalated?: boolean, ticket_id?: string, category?: string}>,
 *   loading: boolean,
 *   conversationId: string,
 *   categoryFilter: string|null,
 *   setCategoryFilter: Function,
 *   sendMessage: (text: string) => Promise<void>,
 *   submitFeedback: (messageIndex: number, rating: 'helpful'|'not_helpful', comment?: string) => Promise<void>,
 *   newChat: () => void,
 *   conversations: Array<{id: string, title: string, timestamp: Date}>,
 *   switchConversation: (id: string) => void,
 * }}
 */
export default function useChat() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(() => uuidv4());
  const [categoryFilter, setCategoryFilter] = useState(null);
  const [conversations, setConversations] = useState([]);

  /** Map of conversation id -> messages for local history */
  const historyRef = useRef({});

  /**
   * Send a user message and append the assistant response.
   * @param {string} text - The user's message text
   */
  const sendMessage = useCallback(
    async (text) => {
      if (!text.trim()) return;

      const userMessage = { role: 'user', content: text };
      setMessages((prev) => [...prev, userMessage]);
      setLoading(true);

      try {
        const { data } = await axios.post('/api/chat', {
          message: text,
          conversation_id: conversationId,
          category: categoryFilter,
        });

        const botMessage = {
          role: 'assistant',
          content: data.response,
          sources: data.sources ?? [],
          confidence: data.confidence ?? null,
          escalated: data.escalated ?? false,
          ticket_id: data.ticket_id ?? null,
          category: data.category ?? null,
        };

        setMessages((prev) => {
          const updated = [...prev, botMessage];
          // persist in local history
          historyRef.current[conversationId] = updated;
          return updated;
        });

        // update conversation list
        setConversations((prev) => {
          const exists = prev.find((c) => c.id === conversationId);
          if (exists) return prev;
          return [
            { id: conversationId, title: text.slice(0, 40), timestamp: new Date() },
            ...prev,
          ];
        });
      } catch (err) {
        const errorMessage = {
          role: 'assistant',
          content:
            'Sorry, I encountered an error processing your request. Please try again or contact support if the issue persists.',
          error: true,
        };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setLoading(false);
      }
    },
    [conversationId, categoryFilter]
  );

  /**
   * Submit feedback for a specific bot message.
   * @param {number} messageIndex - Index of the message in the messages array
   * @param {'helpful'|'not_helpful'} rating - The feedback rating
   * @param {string} [comment] - Optional feedback comment
   */
  const submitFeedback = useCallback(
    async (messageIndex, rating, comment = '') => {
      try {
        await axios.post('/api/feedback', {
          conversation_id: conversationId,
          message_id: String(messageIndex),
          rating,
          feedback_text: comment || undefined,
        });

        setMessages((prev) =>
          prev.map((msg, i) =>
            i === messageIndex ? { ...msg, feedback: rating } : msg
          )
        );
      } catch (err) {
        console.error('Failed to submit feedback:', err);
      }
    },
    [conversationId]
  );

  /**
   * Start a new chat session with a fresh conversation ID.
   */
  const newChat = useCallback(() => {
    // save current conversation
    if (messages.length > 0) {
      historyRef.current[conversationId] = messages;
    }
    setMessages([]);
    setConversationId(uuidv4());
    setCategoryFilter(null);
  }, [messages, conversationId]);

  /**
   * Switch to a previous conversation.
   * @param {string} id - Conversation ID to switch to
   */
  const switchConversation = useCallback(
    (id) => {
      // save current
      if (messages.length > 0) {
        historyRef.current[conversationId] = messages;
      }
      setConversationId(id);
      setMessages(historyRef.current[id] || []);
    },
    [messages, conversationId]
  );

  return {
    messages,
    loading,
    conversationId,
    categoryFilter,
    setCategoryFilter,
    sendMessage,
    submitFeedback,
    newChat,
    conversations,
    switchConversation,
  };
}
