import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useUser, useSidebar, useToast } from './lib/store';
import Sidebar from './components/Sidebar';
import TopBar from './components/TopBar';
import ToastContainer from './components/ToastContainer';
import LoginPrompt from './pages/LoginPrompt';
import HomePage from './pages/HomePage';
import ChatPage from './pages/ChatPage';
import PracticePage from './pages/PracticePage';
import MistakePage from './pages/MistakePage';
import StreaksPage from './pages/StreaksPage';
import TeacherPage from './pages/TeacherPage';

export default function App() {
  const { user, setUser } = useUser();
  const { open, toggle, setOpen } = useSidebar();
  const { toasts, show } = useToast();

  if (!user) {
    return (
      <LoginPrompt
        onLogin={name => {
          setUser({ username: name, role: 'student' });
          show(`Welcome, ${name}! Use the sidebar to navigate.`, 'success');
        }}
      />
    );
  }

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-surface">
        <Sidebar open={open} onClose={() => setOpen(false)} username={user.username} />
        <TopBar
          onMenuClick={toggle}
          username={user.username}
          onLogout={() => setUser(null)}
        />

        <main>
          <Routes>
            <Route path="/" element={<HomePage username={user.username} onStartChat={() => {}} />} />
            <Route path="/chat" element={<ChatPage username={user.username} showToast={show} />} />
            <Route path="/practice" element={<PracticePage showToast={show} />} />
            <Route path="/mistakes" element={<MistakePage showToast={show} />} />
            <Route path="/streaks" element={<StreaksPage username={user.username} showToast={show} />} />
            <Route path="/teacher" element={<TeacherPage showToast={show} />} />
          </Routes>
        </main>

        <ToastContainer toasts={toasts} />
      </div>
    </BrowserRouter>
  );
}
