import { ReactNode } from 'react';

export type TimelineColor = 'primary' | 'secondary' | 'muted' | 'accent' | 'destructive';

export interface TimelineElement {
  date: string;
  title: string;
  description?: string;
  icon?: ReactNode | (() => ReactNode);
  color?: 'primary' | 'secondary' | 'muted' | 'accent';
}