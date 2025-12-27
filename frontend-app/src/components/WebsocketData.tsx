import { useEffect, useState } from 'react';

export type RadarData = Record<string, string>;
export type LabelData = Record<string, Record<string, string>>;

export default function WebsocketData() {
  const [data, setData] = useState<LabelData>({});
  const websocketURL = '127.0.0.1:8000';

  useEffect(() => {
    const socket = new WebSocket(`ws://${websocketURL}/ws/mavlink/`);

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      const source = message.data?.radar ?? 'drone';
      const values: Record<string, string> = {};
      if (message.data) {
        Object.entries(message.data).forEach(([key, value]) => {
          values[key] = Array.isArray(value) ? value.join(', ') : value?.toString() ?? '---';
        });
      }
      setData((prev) => ({
        ...prev,
        [source]: {
          ...prev[source],
          ...values,
        },
      }));
    };

    return () => socket.close();
  }, []);

  return data;
}
