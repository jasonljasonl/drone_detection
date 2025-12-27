import { LabelComponent } from './LabelComponent';
import type { RadarData } from './LabelDisplay';

interface Props {
  selectedRadar: string;
  data: Record<string, RadarData>;
}

export default function RadarDisplay({ selectedRadar, data }: Props) {
  const radarValues = data[selectedRadar];
  if (!radarValues) return <p>Loading {selectedRadar}…</p>;
  return (
    <div className="radar-container">
      <h3>{selectedRadar}</h3>
      <LabelComponent label={{ subtitle: 'distance', subtitleData: radarValues.distance ?? '---', subtitleSize: 'medium' }} />
      <LabelComponent label={{ subtitle: 'radar_position', subtitleData: radarValues.radar_position ?? '---', subtitleSize: 'medium' }} />
    </div>
  );
}
