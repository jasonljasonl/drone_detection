import { useEffect, useState } from 'react';

export type RadarInfo = {
  name: string;
  radar_position: { latitude: number; longitude: number; altitude: number };
  radar_range: number;
  status: string;
  installationDate: string;
};

export default function RadarApiCall() {
  const [radars, setRadars] = useState<RadarInfo[]>([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/radars-list')
      .then(res => res.json())
      .then((data) => {
        const formatted = data.map((r: any) => ({
          name: r.name,
          radar_position: {
            latitude: r.latitude,
            longitude: r.longitude,
            altitude: r.altitude,
          },
            radar_range: r.radar_range,
            status: r.status,
            installationDate: r.installation_date
              ? new Date(r.installation_date).toLocaleString('fr-FR', {
                  day: '2-digit',
                  month: '2-digit',
                  year: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit',
                  second: '2-digit',
                })
              : '---',
          }));
        setRadars(formatted);
      });
  }, []);

  return radars;
}