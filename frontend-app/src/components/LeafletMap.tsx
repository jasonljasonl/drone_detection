import { useEffect } from 'react';
import { MapContainer, TileLayer, Circle, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

type Drone = { latitude: number; longitude: number };
type Radar = { latitude: number; longitude: number };

type Props = {
  drones: Drone[];
  radars: Radar[];
};

function FitBounds({ points }: { points: [number, number][] }) {
  const map = useMap();

  useEffect(() => {
    if (!map || points.length === 0) return;
    map.fitBounds(points, { padding: [50, 50] });
  }, [points, map]);

  return null;
}

export default function LeafletMap({ drones, radars }: Props) {
  const points: [number, number][] = [
    ...drones.map(drone => [drone.latitude, drone.longitude]),
    ...radars.map(radar => [radar.latitude, radar.longitude]),
  ];

  return (
    <div className="h-full w-full">
      <MapContainer
        center={[0, 0]}
        zoom={2}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer url="https://tile.openstreetmap.org/{z}/{x}/{y}.png" />

        <FitBounds points={points} />

        {drones.map((drone, i) => (
          <Circle key={`drone-${i}`} center={[drone.latitude, drone.longitude]} radius={100} color="blue" />
        ))}

        {radars.map((radar, i) => (
          <Circle key={`radar-${i}`} center={[radar.latitude, radar.longitude]} radius={100} color="red" />
        ))}
      </MapContainer>
    </div>
  );
}
