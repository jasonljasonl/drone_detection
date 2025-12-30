import { LabelComponent } from './LabelComponent';
import type { RadarData } from './LabelDisplay';

interface Props {
  selectedDrone: string;
  data: Record<string, RadarData>;
}

export default function DroneDisplay({ selectedDrone, data }: Props) {
  const droneValues = data[selectedDrone];
  const droneId = droneValues.system_id ?? '---';

  if (!droneValues) return <p>Loading drone…</p>;
  return (
    <div className="bg-gray-200 rounded-4xl p-4 m-4">
      <h4 className="text-sm text-gray-400 font-semibold">Drone ID</h4>
      <h3 className="text-lg font-bold tracking-tight text-black sm:text-2xl">
        {droneId}
      </h3>
      <LabelComponent
        label={{
          subtitle: '',
          subtitleData: (
            <div className="flex flex-wrap gap-x-2 gap-y-1">
              <div className="grid mr-8">
                <span className="text-xs text-gray-400 font-semibold">LATITUDE:</span>
                <span className="font-bold text-lg">{droneValues.latitude}</span>
              </div>
              <div className="grid mr-8">
                <span className="text-xs text-gray-400 font-semibold">LONGITUDE:</span>
                <span className="font-bold text-lg">{droneValues.longitude}</span>
              </div>
              <div className="grid mr-8">
                <span className="text-xs text-gray-400 font-semibold">ALTITUDE:</span>
                <span className="font-bold text-lg">{droneValues.altitude}</span>
              </div>
            </div>
          ),
        }}
      />
    </div>
  );
}
