import { useEffect } from 'react';

export function useSSE(
  url: string | null,
  handler: (event: string, data: any) => void
) {
  useEffect(() => {
    if (!url) return;

    const fullUrl = url.startsWith('http') 
      ? url 
      : `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}${url}`;

    const eventSource = new EventSource(fullUrl);

    const eventTypes = [
      'agent_started',
      'agent_progress',
      'agent_finding',
      'agent_complete',
      'agent_failed',
      'investigation_complete'
    ];

    eventTypes.forEach((eventType) => {
      eventSource.addEventListener(eventType, (e: MessageEvent) => {
        try {
          const data = JSON.parse(e.data);
          handler(eventType, data);

          if (eventType === 'investigation_complete') {
            eventSource.close();
          }
        } catch (error) {
          console.error(`Error parsing SSE event ${eventType}:`, error);
        }
      });
    });

    eventSource.onerror = (error) => {
      console.error('SSE connection error:', error);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, [url, handler]);
}
