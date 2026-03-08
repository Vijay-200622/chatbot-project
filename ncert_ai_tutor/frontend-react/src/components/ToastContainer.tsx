import type { Toast } from '../lib/store';
import { CheckCircle, AlertCircle, Info } from 'lucide-react';

interface ToastContainerProps {
  toasts: Toast[];
}

const ICONS = {
  success: CheckCircle,
  error: AlertCircle,
  info: Info,
};

const COLORS = {
  success: 'bg-teal text-white',
  error: 'bg-coral text-white',
  info: 'bg-primary text-white',
};

export default function ToastContainer({ toasts }: ToastContainerProps) {
  if (!toasts.length) return null;
  return (
    <div className="fixed bottom-4 right-4 z-[100] flex flex-col gap-2">
      {toasts.map(t => {
        const Icon = ICONS[t.type];
        return (
          <div
            key={t.id}
            className={`flex items-center gap-2 px-4 py-3 rounded-lg shadow-lg animate-fade-in-up ${COLORS[t.type]}`}
          >
            <Icon size={18} />
            <span className="text-sm font-medium">{t.message}</span>
          </div>
        );
      })}
    </div>
  );
}
