import { Routes, Route } from 'react-router-dom';
import Chat from './pages/Chat';
import Admin from './pages/Admin';
import Analytics from './pages/Analytics';

/**
 * Root application component.
 * Defines the top-level route structure for the IT HelpDesk AI frontend.
 */
function App() {
  return (
    <Routes>
      <Route path="/" element={<Chat />} />
      <Route path="/admin" element={<Admin />} />
      <Route path="/analytics" element={<Analytics />} />
    </Routes>
  );
}

export default App;
