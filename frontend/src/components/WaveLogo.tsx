import React from 'react';

interface WaveLogoProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  useImage?: boolean;
  imageSrc?: string;
}

export function WaveLogo({ 
  size = 'md', 
  className = '', 
  useImage = false, 
  imageSrc = '/assets/wave-logo.png' 
}: WaveLogoProps): React.JSX.Element {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-12 h-12',
    lg: 'w-16 h-16'
  };

  if (useImage && imageSrc) {
    return (
      <div className={`${sizeClasses[size]} ${className}`}>
        <img
          src={imageSrc}
          alt="Flow Roll Wave Logo"
          className="w-full h-full object-contain"
        />
      </div>
    );
  }

  return (
    <div className={`${sizeClasses[size]} ${className}`}>
      <svg
        viewBox="0 0 64 64"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full"
      >
        {/* Wave 1 - Left */}
        <path
          d="M8 32C8 32 12 24 20 24C28 24 32 32 32 32"
          stroke="currentColor"
          strokeWidth="3"
          strokeLinecap="round"
          fill="none"
        />
        
        {/* Wave 2 - Center (Main) */}
        <path
          d="M24 40C24 40 28 16 40 16C52 16 56 40 56 40"
          stroke="currentColor"
          strokeWidth="4"
          strokeLinecap="round"
          fill="none"
        />
        
        {/* Wave 3 - Right */}
        <path
          d="M40 32C40 32 44 24 52 24C60 24 64 32 64 32"
          stroke="currentColor"
          strokeWidth="3"
          strokeLinecap="round"
          fill="none"
        />
        
        {/* Wave foam/curl details */}
        <circle cx="40" cy="16" r="2" fill="currentColor" />
        <circle cx="44" cy="20" r="1.5" fill="currentColor" />
        <circle cx="20" cy="24" r="1.5" fill="currentColor" />
        <circle cx="52" cy="24" r="1.5" fill="currentColor" />
      </svg>
    </div>
  );
}
