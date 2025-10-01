import React, { useState, useRef, useEffect } from 'react';
import { Header } from './Header';
import { Hero } from './Hero';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { InjurySelector } from './InjurySelector';
import { Results } from './Results';
import { WaveLogo } from './WaveLogo';
import { Footer } from './Footer';


export function AppLayout(): React.JSX.Element {
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant' | 'system'; text: string; timestamp?: Date }>>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [busy, setBusy] = useState<boolean>(false);
  const [data, setData] = useState<any>(null);
  const chatRef = useRef<HTMLDivElement>(null);
  const sessionIdRef = useRef<string>(Math.random().toString(36).slice(2));

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  async function sendMessage(message: string): Promise<void> {
    const userMessage = { role: 'user' as const, text: message, timestamp: new Date() };
    setMessages(m => [...m, userMessage]);
    setBusy(true);
    
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionIdRef.current, message })
      });
      
      if (!res.ok) throw new Error('Request failed');
      const response = await res.json();
      
      setMessages(m => [...m, { 
        role: 'assistant', 
        text: response.reply || '(no reply)', 
        timestamp: new Date() 
      }]);
    } catch (e: any) {
      setMessages(m => [...m, { 
        role: 'system', 
        text: 'Error: ' + e.message, 
        timestamp: new Date() 
      }]);
    } finally {
      setBusy(false);
    }
  }

  async function fetchRecs(): Promise<void> {
    setBusy(true);
    try {
      const res = await fetch('/api/recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ injuries: selected })
      });
      const json = await res.json();
      setData(json);
    } catch (e: any) {
      setData({ 
        injuries: selected, 
        safe_moves: [], 
        unsafe_moves: [], 
        ai_recommendations: { recommendations: '' }, 
        recovery_advice: 'Error: ' + e.message 
      });
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <div className="space-y-0">
          {/* Hero Section */}
          <Hero />

          {/* Injury Selector */}
          <div data-section="injuries" className="py-8">
            <InjurySelector 
              selected={selected} 
              setSelected={setSelected} 
              onFetch={fetchRecs} 
              busy={busy} 
            />
          </div>


          {/* Chat Area */}
          <div data-section="chat" className="bg-card/50 backdrop-blur-sm rounded-2xl border border-border/50 shadow-xl">
            <div className="p-6 border-b border-border/50">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 rounded-full bg-primary"></div>
                  <div>
                    <h2 className="text-xl font-semibold text-foreground">Chat with AI Coach</h2>
                    <p className="text-sm text-muted-foreground">powered by NVIDIA Nemotron</p>
                  </div>
                </div>
              </div>
            </div>
            <div 
              ref={chatRef}
              className="h-[500px] overflow-y-auto p-6 space-y-6 scrollbar-hide"
            >
              {messages.length === 0 && (
                <div className="flex flex-col items-center justify-center h-full text-center space-y-6">
                  <div className="w-24 h-24 rounded-2xl bg-primary/20 flex items-center justify-center border border-primary/20">
                    <WaveLogo size="lg" className="text-primary" useImage={true} imageSrc="/static/frontend/assets/wave-logo.png" />
                  </div>
                  <div className="space-y-3">
                    <h3 className="text-2xl font-semibold text-foreground">Ready to help!</h3>
                    <p className="text-muted-foreground max-w-md leading-relaxed">
                      Ask me about BJJ techniques, injury modifications, training strategies, or recovery advice. I'm here to help you train safely and effectively.
                    </p>
                  </div>
                  <div className="flex flex-wrap gap-2 justify-center">
                    <button 
                      onClick={() => sendMessage("I need technique advice for my BJJ training. Can you help me with some fundamental techniques?")}
                      className="px-3 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary border border-primary/20 hover:bg-primary/20 hover:border-primary/30 transition-colors cursor-pointer"
                    >
                      Technique advice
                    </button>
                    <button 
                      onClick={() => sendMessage("I have some injuries and need modifications for BJJ techniques. What should I avoid?")}
                      className="px-3 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary border border-primary/20 hover:bg-primary/20 hover:border-primary/30 transition-colors cursor-pointer"
                    >
                      Injury modifications
                    </button>
                    <button 
                      onClick={() => sendMessage("Can you give me some training strategies for improving my BJJ game?")}
                      className="px-3 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary border border-primary/20 hover:bg-primary/20 hover:border-primary/30 transition-colors cursor-pointer"
                    >
                      Training strategies
                    </button>
                  </div>
                </div>
              )}
              
              {messages.map((message, index) => (
                <ChatMessage
                  key={index}
                  role={message.role}
                  content={message.text}
                  timestamp={message.timestamp}
                />
              ))}
              
              {busy && (
                <div className="flex justify-start mb-4 animate-in fade-in-0 slide-in-from-left-2 duration-300">
                  <div className="flex max-w-[85%] flex-row items-start gap-3">
                    {/* Avatar */}
                    <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold shadow-sm bg-gradient-to-br from-blue-500 to-blue-600 text-white">
                      AI
                    </div>
                    
                    {/* Typing indicator */}
                    <div className="relative rounded-2xl px-4 py-3 shadow-sm bg-muted/80 backdrop-blur-sm text-foreground rounded-bl-md border border-border/50">
                      <div className="flex items-center space-x-1">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-muted-foreground/60 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                          <div className="w-2 h-2 bg-muted-foreground/60 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                          <div className="w-2 h-2 bg-muted-foreground/60 rounded-full animate-bounce"></div>
                        </div>
                        <span className="text-xs text-muted-foreground ml-2">AI Coach is typing...</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
            <div className="p-6 border-t border-border/50 bg-muted/30">
              <ChatInput 
                onSend={sendMessage}
                disabled={busy}
                placeholder="Ask about BJJ techniques, injury modifications, or training advice..."
              />
            </div>
          </div>

          {/* Results */}
          {data && (
            <div className="py-8">
              <Results data={data} />
            </div>
          )}
        </div>
      </main>
      
      <Footer />
    </div>
  );
}
