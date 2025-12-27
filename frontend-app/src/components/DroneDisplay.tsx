import { LabelComponent } from './LabelComponent';
import type { RadarData } from './LabelDisplay';

interface Props {
  selectedDrone: string;
  data: Record<string, RadarData>;
}

export default function DroneDisplay({ selectedDrone, data }: Props) {
  const droneValues = data[selectedDrone];
  if (!droneValues) return <p>Loading drone…</p>;
  return (
    <div className="drone-container">
      <h3>{selectedDrone}</h3>
      <LabelComponent label={{ subtitle: 'latitude', subtitleData: droneValues.latitude ?? '---', subtitleSize: 'medium' }} />
      <LabelComponent label={{ subtitle: 'longitude', subtitleData: droneValues.longitude ?? '---', subtitleSize: 'medium' }} />
      <LabelComponent label={{ subtitle: 'altitude', subtitleData: droneValues.altitude ?? '---', subtitleSize: 'large' }} />
    </div>
  );
}
