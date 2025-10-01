import React from 'react';

export function Footer(): React.JSX.Element {
  return (
    <footer className="bg-card/30 border-t border-border/50 mt-16">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center space-x-2">
            <div className="w-6 h-6 rounded-lg bg-primary/20 flex items-center justify-center">
              <svg
                className="h-4 w-4 text-primary"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-foreground">Important Disclaimer</h3>
          </div>
          
          <div className="max-w-2xl mx-auto">
            <p className="text-sm text-muted-foreground leading-relaxed">
              <strong className="text-foreground">This application does not provide professional medical advice.</strong>
              <br />
              Please consult with a healthcare professional before making any medical or training decisions.
            </p>
          </div>
          
          <div className="pt-4 border-t border-border/30">
            <p className="text-xs text-muted-foreground/70">
              © 2025 FlowRoll. Built with AI-powered assistance. Use responsibly.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
