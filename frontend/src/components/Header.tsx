import React from 'react';
import { WaveLogo } from './WaveLogo';

export function Header(): React.JSX.Element {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo and Brand */}
          <div className="flex items-center space-x-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl shadow-lg">
              <WaveLogo size="sm" className="text-primary-foreground" useImage={true} imageSrc="/static/frontend/assets/wave-logo.png" />
            </div>
            <div className="flex flex-col">
              <span className="text-xl font-bold text-foreground">
                FlowRoll
              </span>
            </div>
          </div>
          
        </div>
      </div>
    </header>
  );
}
