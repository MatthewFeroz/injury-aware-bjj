import React, { useState, useEffect } from 'react';

interface ChatMessageProps {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: Date;
}

export function ChatMessage({ role, content, timestamp }: ChatMessageProps): React.JSX.Element {
  const isUser = role === 'user';
  const isSystem = role === 'system';
  const [displayedContent, setDisplayedContent] = useState('');
  
  // Typing animation for assistant messages
  useEffect(() => {
    if (isUser || isSystem || !content) {
      setDisplayedContent(content);
      return;
    }

    setDisplayedContent('');
    
    let index = 0;
    const timer = setInterval(() => {
      if (index <= content.length) {
        setDisplayedContent(content.slice(0, index));
        index++;
      } else {
        clearInterval(timer);
      }
    }, 20); // Adjust speed here (lower = faster)

    return () => clearInterval(timer);
  }, [content, isUser, isSystem]);
  
  if (isSystem) {
    return (
      <div className="flex justify-center my-4 animate-in fade-in-0 slide-in-from-top-2 duration-300">
        <div className="bg-muted/50 text-muted-foreground text-sm px-3 py-1 rounded-full">
          {content}
        </div>
      </div>
    );
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-in fade-in-0 slide-in-from-${isUser ? 'right' : 'left'}-2 duration-300`}>
      <div className={`flex max-w-[85%] ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start gap-3`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium ${
          isUser 
            ? 'bg-primary text-primary-foreground' 
            : 'bg-secondary text-secondary-foreground'
        }`}>
          {isUser ? 'U' : 'FR'}
        </div>
        
        {/* Message bubble */}
        <div className={`rounded-2xl px-4 py-2 ${
          isUser 
            ? 'bg-primary text-primary-foreground rounded-br-md' 
            : 'bg-muted text-foreground rounded-bl-md'
        }`}>
          <div className="text-sm leading-relaxed whitespace-pre-wrap">
            {displayedContent}
          </div>
          {timestamp && (
            <div className={`text-xs mt-1 ${
              isUser ? 'text-primary-foreground/70' : 'text-muted-foreground'
            }`}>
              {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
