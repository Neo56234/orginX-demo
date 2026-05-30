export const DEMO_MODE = process.env.NEXT_PUBLIC_DEMO_MODE === 'true';

export const DEMO_IDS = ['demo-pakistan-protest', 'demo-india-flood', 'demo-authentic-bd'];

export function isDemoId(id: string): boolean {
  return id.startsWith('demo-');
}
