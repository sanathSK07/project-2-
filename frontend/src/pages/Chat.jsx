import { useState } from 'react';
import Header from '../components/Header';
import SideBar from '../components/SideBar';
import ChatWindow from '../components/ChatWindow';
import useChat from '../hooks/useChat';
import { PanelLeftClose, PanelLeft } from 'lucide-react';

/**
 * Full chat page layout: Header + Sidebar + ChatWindow.
 * Responsive -- sidebar collapses on mobile via a toggle button.
 */
export default function Chat() {
  const {
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
  } = useChat();

  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="h-screen flex flex-col overflow-hidden">
      <Header />

      <div className="flex flex-1 min-h-0 relative">
        {/* ── Mobile sidebar toggle ───────────────────── */}
        <button
          onClick={() => setSidebarOpen((o) => !o)}
          className="absolute top-3 left-3 z-20 p-2 rounded-lg bg-navy-800 border border-navy-700 text-navy-400 hover:text-white lg:hidden transition-default"
          aria-label="Toggle sidebar"
        >
          {sidebarOpen ? <PanelLeftClose size={18} /> : <PanelLeft size={18} />}
        </button>

        {/* ── Sidebar ─────────────────────────────────── */}
        <div
          className={`absolute inset-y-0 left-0 z-10 lg:relative lg:z-auto transition-transform duration-200 ${
            sidebarOpen
              ? 'translate-x-0'
              : '-translate-x-full lg:translate-x-0 lg:hidden'
          }`}
        >
          <SideBar
            onNewChat={newChat}
            conversations={conversations}
            activeId={conversationId}
            onSelect={switchConversation}
            categoryFilter={categoryFilter}
            onCategoryChange={setCategoryFilter}
          />
        </div>

        {/* ── Main chat area ──────────────────────────── */}
        <ChatWindow
          messages={messages}
          loading={loading}
          onSend={sendMessage}
          onFeedback={submitFeedback}
        />
      </div>
    </div>
  );
}
