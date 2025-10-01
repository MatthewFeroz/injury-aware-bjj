import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Checkbox } from './ui/checkbox';
import { Label } from './ui/label';
import { Button } from './ui/button';

const ALL_INJURIES = [
  'ACL reconstruction',
  'Meniscus tear',
  'Shoulder instability',
  'Labrum tear',
  'Wrist ligament injury',
  'Neck injury',
  'Lower back pain',
  "I'm feeling sluggish or tired",
];

interface InjurySelectorProps {
  selected: string[];
  setSelected: (injuries: string[]) => void;
  onFetch: () => void;
  busy: boolean;
}

export function InjurySelector({ selected, setSelected, onFetch, busy }: InjurySelectorProps): React.JSX.Element {
  function toggle(injury: string): void {
    if (selected.includes(injury)) {
      setSelected(selected.filter((i) => i !== injury));
    } else {
      setSelected([...selected, injury]);
    }
  }

  return (
    <Card className="bg-card/50 backdrop-blur-sm border-border/50 shadow-xl">
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center gap-3 text-xl">
          <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
            <span className="text-sm font-bold text-primary">+</span>
          </div>
          Select Your Injuries
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          Choose any injuries or conditions you have to get personalized training recommendations.
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {ALL_INJURIES.map((inj) => (
            <button
              key={inj}
              type="button"
              className={`w-full flex items-center gap-3 p-4 rounded-lg border transition-all text-left ${
                selected.includes(inj) 
                  ? 'bg-primary/10 border-primary/30 text-primary shadow-md' 
                  : 'bg-muted/30 border-border/50 hover:bg-muted/50 hover:border-primary/20 hover:shadow-sm'
              }`}
              onClick={() => toggle(inj)}
            >
              <Checkbox 
                id={inj} 
                checked={selected.includes(inj)} 
                onCheckedChange={() => toggle(inj)} 
                className="data-[state=checked]:bg-primary data-[state=checked]:border-primary pointer-events-none"
              />
              <Label htmlFor={inj} className="text-sm font-medium cursor-pointer flex-1 pointer-events-none">
                {inj}
              </Label>
            </button>
          ))}
        </div>
        
        <div className="flex items-center justify-between pt-4 border-t border-border/50">
          <div className="flex items-center gap-2">
            {selected.length > 0 && (
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <div className="w-2 h-2 rounded-full bg-primary"></div>
                <span>{selected.length} injury{selected.length !== 1 ? 'ies' : ''} selected</span>
              </div>
            )}
          </div>
          <Button 
            onClick={onFetch} 
            disabled={busy || selected.length === 0}
            className="px-8 py-2 bg-primary hover:bg-primary/90 shadow-lg"
            size="lg"
          >
            {busy ? (
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin"></div>
                Loading…
              </div>
            ) : (
              'Get Recommendations'
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
