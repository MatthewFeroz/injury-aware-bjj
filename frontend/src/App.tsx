import React, { useEffect, useRef, useState } from 'react';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Checkbox } from './components/ui/checkbox';
import { Label } from './components/ui/label';

const ALL_INJURIES = [
  'ACL reconstruction',
  'Meniscus tear',
  'Shoulder instability',
  'Labrum tear',
  'Wrist ligament injury',
  'Neck injury',
  'Lower back pain',
];

function ChatPanel(): React.JSX.Element {
  const [messages, setMessages] = useState<Array<{ role: string; text: string }>>([]);
  const [input, setInput] = useState<string>('');
  const [busy, setBusy] = useState<boolean>(false);
  const chatRef = useRef<HTMLDivElement | null>(null);
  const sessionIdRef = useRef<string>(Math.random().toString(36).slice(2));

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  async function send(): Promise<void> {
    const text = input.trim();
    if (!text || busy) return;
    setMessages((m) => [...m, { role: 'You', text }]);
    setInput('');
    setBusy(true);
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionIdRef.current, message: text }),
      });
      if (!res.ok) throw new Error('Request failed');
      const data = await res.json();
      setMessages((m) => [...m, { role: 'Coach', text: data.reply || '(no reply)' }]);
    } catch (e: any) {
      setMessages((m) => [...m, { role: 'System', text: 'Error: ' + e.message }]);
    } finally {
      setBusy(false);
    }
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLInputElement>): void {
    if (e.key === 'Enter') void send();
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>💬 Chat with AI Coach</CardTitle>
      </CardHeader>
      <CardContent>
        <div ref={chatRef} className="h-60 overflow-auto rounded-md border p-3">
          {messages.length === 0 && <div className="text-sm text-muted-foreground">Ask about modifications, strategy, or rehab safety.</div>}
          {messages.map((m, i) => (
            <div key={i} className="my-2 leading-relaxed">
              <span className="opacity-70 mr-1 font-semibold">{m.role}:</span>
              <span>{m.text}</span>
            </div>
          ))}
        </div>
        <div className="mt-3 flex gap-2">
          <Input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={onKeyDown} placeholder="Type your message..." />
          <Button onClick={send} disabled={busy}>{busy ? 'Sending…' : 'Send'}</Button>
        </div>
      </CardContent>
    </Card>
  );
}

function InjurySelector(props: {
  selected: string[];
  setSelected: (injuries: string[]) => void;
  onFetch: () => void;
  busy: boolean;
}): React.JSX.Element {
  const { selected, setSelected, onFetch, busy } = props;

  function toggle(injury: string): void {
    if (selected.includes(injury)) {
      setSelected(selected.filter((i) => i !== injury));
    } else {
      setSelected([...selected, injury]);
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>🩹 Select Injuries</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {ALL_INJURIES.map((inj) => (
            <div className="flex items-center gap-2" key={inj}>
              <Checkbox id={inj} checked={selected.includes(inj)} onCheckedChange={() => toggle(inj)} />
              <Label htmlFor={inj}>{inj}</Label>
            </div>
          ))}
        </div>
        <div className="mt-3 flex items-center gap-3">
          <Button onClick={onFetch} disabled={busy || selected.length === 0}>{busy ? 'Loading…' : 'Get Recommendations'}</Button>
          {selected.length > 0 && (
            <div className="text-sm text-muted-foreground">{selected.length} selected</div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

type ApiData = {
  injuries?: string[];
  safe_moves?: string[];
  unsafe_moves?: string[];
  ai_recommendations?: { recommendations?: string };
  recovery_advice?: string;
} | null;

function Results({ data }: { data: ApiData }): React.JSX.Element | null {
  if (!data) return null;
  const { injuries = [], safe_moves = [], unsafe_moves = [], ai_recommendations = {}, recovery_advice = '' } = data;
  return (
    <Card>
      <CardHeader>
        <CardTitle>📊 Results</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="mb-2 space-x-2">
          {injuries.map((i) => (
            <span key={i} className="inline-block rounded-full border px-2 py-1 text-xs text-muted-foreground">
              {i}
            </span>
          ))}
        </div>
        <div className="grid md:grid-cols-2 gap-3">
          <div className="rounded-md border-l-4 border-destructive p-3 border">
            <h4 className="font-semibold mb-2 text-destructive">❌ Unsafe Moves</h4>
            {unsafe_moves.length ? (
              <ul className="ml-4 list-disc">
                {unsafe_moves.map((m) => (
                  <li key={m}>{m}</li>
                ))}
              </ul>
            ) : (
              <div className="text-sm text-muted-foreground">No unsafe moves found.</div>
            )}
          </div>
          <div className="rounded-md border-l-4 border-green-500 p-3 border">
            <h4 className="font-semibold mb-2 text-green-500">✅ Safe Moves</h4>
            {safe_moves.length ? (
              <ul className="ml-4 list-disc">
                {safe_moves.map((m) => (
                  <li key={m}>{m}</li>
                ))}
              </ul>
            ) : (
              <div className="text-sm text-muted-foreground">No safe moves found.</div>
            )}
          </div>
        </div>
        {ai_recommendations && ai_recommendations.recommendations && (
          <div className="mt-3 rounded-md border-l-4 border-primary p-3 border">
            <h4 className="font-semibold mb-2 text-primary">🤖 AI Coach Recommendations</h4>
            <div className="whitespace-pre-line">{ai_recommendations.recommendations}</div>
          </div>
        )}
        {recovery_advice && (
          <div className="mt-3 rounded-md border-l-4 border-yellow-400 p-3 border">
            <h4 className="font-semibold mb-2 text-yellow-400">🏥 Recovery & Rehabilitation Advice</h4>
            <div className="whitespace-pre-line">{recovery_advice}</div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default function App(): React.JSX.Element {
  const [selected, setSelected] = useState<string[]>([]);
  const [busy, setBusy] = useState<boolean>(false);
  const [data, setData] = useState<ApiData>(null);

  async function fetchRecs(): Promise<void> {
    setBusy(true);
    try {
      const res = await fetch('/api/recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ injuries: selected }),
      });
      const json = await res.json();
      setData(json);
    } catch (e: any) {
      setData({ injuries: selected, safe_moves: [], unsafe_moves: [], ai_recommendations: { recommendations: '' }, recovery_advice: 'Error: ' + e.message });
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-4 p-4">
      <div className="text-center">
        <h1 className="text-3xl md:text-4xl font-bold tracking-tight">Injury Aware BJJ Coach</h1>
      </div>
      <ChatPanel />
      <InjurySelector selected={selected} setSelected={setSelected} onFetch={fetchRecs} busy={busy} />
      <Results data={data} />
    </div>
  );
}


