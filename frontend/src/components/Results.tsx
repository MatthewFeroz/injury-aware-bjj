import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

type ApiData = {
  injuries?: string[];
  safe_moves?: string[];
  unsafe_moves?: string[];
  ai_recommendations?: { recommendations?: string };
  recovery_advice?: string;
} | null;

interface ResultsProps {
  data: ApiData;
}

export function Results({ data }: ResultsProps): React.JSX.Element | null {
  if (!data) return null;
  
  const { injuries = [], safe_moves = [], unsafe_moves = [], ai_recommendations = {}, recovery_advice = '' } = data;
  
  return (
    <div className="space-y-6">
      {/* Selected Injuries Tags */}
      {injuries.length > 0 && (
        <div className="bg-muted/30 rounded-xl p-4 border border-border/50">
          <h3 className="text-sm font-medium text-muted-foreground mb-3">Selected Injuries:</h3>
          <div className="flex flex-wrap gap-2">
            {injuries.map((i) => (
              <span 
                key={i} 
                className="inline-flex items-center px-3 py-1.5 rounded-full text-sm font-medium bg-primary/10 text-primary border border-primary/20"
              >
                {i}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Safe vs Unsafe Moves */}
      <div className="grid lg:grid-cols-2 gap-6">
        <Card className="bg-card/50 backdrop-blur-sm border-destructive/20 shadow-xl">
          <CardHeader className="pb-4">
            <CardTitle className="flex items-center gap-3 text-lg text-destructive">
              <div className="w-8 h-8 rounded-lg bg-destructive/20 flex items-center justify-center">
                <span className="text-sm font-bold text-destructive">!</span>
              </div>
              Unsafe Moves
            </CardTitle>
          </CardHeader>
          <CardContent>
            {unsafe_moves.length ? (
              <ul className="space-y-3">
                {unsafe_moves.map((m) => (
                  <li key={m} className="text-sm text-muted-foreground flex items-start gap-3">
                    <span className="w-2 h-2 bg-destructive rounded-full mt-2 flex-shrink-0" />
                    <span>{m}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-sm text-muted-foreground text-center py-4">
                No unsafe moves found for your selected injuries.
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="bg-card/50 backdrop-blur-sm border-green-500/20 shadow-xl">
          <CardHeader className="pb-4">
            <CardTitle className="flex items-center gap-3 text-lg text-green-500">
              <div className="w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center">
                <span className="text-sm font-bold text-green-500">✓</span>
              </div>
              Safe Moves
            </CardTitle>
          </CardHeader>
          <CardContent>
            {safe_moves.length ? (
              <ul className="space-y-3">
                {safe_moves.map((m) => (
                  <li key={m} className="text-sm text-muted-foreground flex items-start gap-3">
                    <span className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0" />
                    <span>{m}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-sm text-muted-foreground text-center py-4">
                No safe moves found for your selected injuries.
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* AI Recommendations */}
      {ai_recommendations && ai_recommendations.recommendations && (
        <Card className="bg-card/50 backdrop-blur-sm border-primary/20 shadow-xl">
          <CardHeader className="pb-4">
            <CardTitle className="flex items-center gap-3 text-lg text-primary">
              <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
                <span className="text-sm font-bold text-primary">AI</span>
              </div>
              AI Coach Recommendations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-sm leading-relaxed text-muted-foreground prose prose-sm max-w-none prose-headings:text-primary prose-headings:font-semibold prose-h1:text-lg prose-h2:text-base prose-h3:text-sm prose-p:text-muted-foreground prose-strong:text-foreground prose-strong:font-semibold prose-ul:text-muted-foreground prose-li:text-muted-foreground">
              <ReactMarkdown 
                remarkPlugins={[remarkGfm]}
                components={{
                  h1: ({children}) => <h1 className="text-lg font-semibold text-primary mt-4 mb-2">{children}</h1>,
                  h2: ({children}) => <h2 className="text-base font-semibold text-primary mt-3 mb-2">{children}</h2>,
                  h3: ({children}) => <h3 className="text-sm font-semibold text-primary mt-2 mb-1">{children}</h3>,
                  p: ({children}) => <p className="text-muted-foreground mb-2">{children}</p>,
                  ul: ({children}) => <ul className="list-disc list-inside text-muted-foreground mb-2 space-y-1">{children}</ul>,
                  ol: ({children}) => <ol className="list-decimal list-inside text-muted-foreground mb-2 space-y-1">{children}</ol>,
                  li: ({children}) => <li className="text-muted-foreground">{children}</li>,
                  strong: ({children}) => <strong className="text-foreground font-semibold">{children}</strong>,
                  em: ({children}) => <em className="text-muted-foreground italic">{children}</em>,
                }}
              >
                {ai_recommendations.recommendations}
              </ReactMarkdown>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Recovery Advice */}
      {recovery_advice && (
        <Card className="bg-card/50 backdrop-blur-sm border-green-500/20 shadow-xl">
          <CardHeader className="pb-4">
            <CardTitle className="flex items-center gap-3 text-lg text-green-500">
              <div className="w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center">
                <span className="text-sm font-bold text-green-500">R</span>
              </div>
              Recovery & Rehabilitation Advice
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-sm leading-relaxed text-muted-foreground prose prose-sm max-w-none prose-headings:text-green-500 prose-headings:font-semibold prose-h1:text-lg prose-h2:text-base prose-h3:text-sm prose-p:text-muted-foreground prose-strong:text-foreground prose-strong:font-semibold prose-ul:text-muted-foreground prose-li:text-muted-foreground">
              <ReactMarkdown 
                remarkPlugins={[remarkGfm]}
                components={{
                  h1: ({children}) => <h1 className="text-lg font-semibold text-green-500 mt-4 mb-2">{children}</h1>,
                  h2: ({children}) => <h2 className="text-base font-semibold text-green-500 mt-3 mb-2">{children}</h2>,
                  h3: ({children}) => <h3 className="text-sm font-semibold text-green-500 mt-2 mb-1">{children}</h3>,
                  p: ({children}) => <p className="text-muted-foreground mb-2">{children}</p>,
                  ul: ({children}) => <ul className="list-disc list-inside text-muted-foreground mb-2 space-y-1">{children}</ul>,
                  ol: ({children}) => <ol className="list-decimal list-inside text-muted-foreground mb-2 space-y-1">{children}</ol>,
                  li: ({children}) => <li className="text-muted-foreground">{children}</li>,
                  strong: ({children}) => <strong className="text-foreground font-semibold">{children}</strong>,
                  em: ({children}) => <em className="text-muted-foreground italic">{children}</em>,
                }}
              >
                {recovery_advice}
              </ReactMarkdown>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
