import React from 'react';
import { WaveLogo } from './WaveLogo';
import { Button } from './ui/button';

export function Hero(): React.JSX.Element {
  return (
    <section className="relative py-16 lg:py-24 overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-background"></div>

      {/* Content */}
      <div className="relative mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <div className="text-center space-y-8">
          {/* Logo and Title */}
          <div className="space-y-6">
            <div className="flex justify-center">
              <div className="w-20 h-20 rounded-2xl bg-primary/20 flex items-center justify-center border border-primary/20 shadow-xl">
                <WaveLogo
                  size="lg"
                  className="text-primary"
                  useImage={true}
                  imageSrc="/static/frontend/assets/wave-logo.png"
                />
              </div>
            </div>
            <div className="space-y-4">
              <h1 className="text-4xl lg:text-6xl font-bold tracking-tight text-foreground">
                FlowRoll
              </h1>
              <p className="text-xl lg:text-2xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                AI-Powered Recovery for Injured Athletes
              </p>
            </div>
          </div>

          {/* Mission Statement */}
          <div className="space-y-6 max-w-4xl mx-auto">
            <div className="bg-card/50 backdrop-blur-sm rounded-2xl border border-border/50 p-8 shadow-xl">
              <h2 className="text-2xl lg:text-3xl font-bold text-foreground mb-6">
                Our Mission
              </h2>
              <p className="text-lg text-muted-foreground leading-relaxed mb-6">
                Flow Roll revolutionizes injury recovery for athletes by harnessing the power of
                <span className="text-primary font-semibold">
                  {' '}
                  NVIDIA Nemotron AI models
                </span>{' '}
                to provide personalized, intelligent training recommendations that adapt to your specific injuries and recovery progress.
              </p>
              <p className="text-lg text-muted-foreground leading-relaxed">
                We believe every athlete deserves to train safely, recover faster, and return to peak performance
                with confidence, guided by cutting-edge AI technology.
              </p>
            </div>
          </div>

          {/* Call to Action */}
          <div className="space-y-6">
            <p className="text-lg text-muted-foreground">
              Ready to transform your recovery journey?
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                size="lg"
                className="px-8 py-3 bg-primary hover:bg-primary/90 shadow-lg text-lg"
                onClick={() => {
                  const injurySection = document.querySelector('[data-section="injuries"]');
                  injurySection?.scrollIntoView({ behavior: 'smooth' });
                }}
              >
                Start Your Recovery Journey
              </Button>
              <Button
                variant="outline"
                size="lg"
                className="px-8 py-3 border-primary text-primary hover:bg-primary hover:text-primary-foreground text-lg"
                onClick={() => {
                  const chatSection = document.querySelector('[data-section="chat"]');
                  chatSection?.scrollIntoView({ behavior: 'smooth' });
                }}
              >
                Chat with AI Coach
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
