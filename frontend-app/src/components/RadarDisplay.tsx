import { LabelComponent } from './LabelComponent';
import type { RadarData } from './LabelDisplay';

interface RadarInfo {
  radar_range: number;
  status: string;
  installationDate: string;
}

interface Props {
  selectedRadar: string;
  data: Record<string, RadarData>;
  radarPosition: { latitude: number; longitude: number; altitude: number };
  radarInfo?: RadarInfo;
}

export default function RadarDisplay({ selectedRadar, data, radarPosition, radarInfo }: Props) {
  const radarValues = data[selectedRadar] ?? {};
  const droneData = data['drone'] ?? {};

  const distance =
    radarValues.distance ??
    radarValues.distance_to_drone ??
    '---';

  const droneId = droneData.system_id ?? '---';

  return (
    <div className="bg-gray-200 rounded-4xl p-4 m-4">
      <div className="mb-4 grid grid-cols-6">
        <div className="col-start-1 col-end-4">
          <h4 className="text-sm text-gray-400 font-semibold">Radar name</h4>
          <h3 className="text-lg font-bold tracking-tight text-black sm:text-2xl">
            {selectedRadar}
          </h3>
        </div>
        <div className="col-end-7">
          <LabelComponent
            label={{
              subtitle: 'STATUS',
              subtitleData: radarInfo?.status ?? '---',
            }}
          />

        </div>
      </div>


      <LabelComponent
        label={{
          subtitle: '',
          subtitleData: (
            <div className="flex flex-wrap gap-x-2 gap-y-1">
              <div className="grid mr-8">
                <span className="text-xs text-gray-400 font-semibold">LATITUDE:</span>
                <span className="font-bold text-lg">{radarPosition.latitude}</span>
              </div>
              <div className="grid mr-8">
                <span className="text-xs text-gray-400 font-semibold">LONGITUDE:</span>
                <span className="font-bold text-lg">{radarPosition.longitude}</span>
              </div>
              <div className="grid mr-8">
                <span className="text-xs text-gray-400 font-semibold">ALTITUDE:</span>
                <span className="font-bold text-lg">{radarPosition.altitude}</span>
              </div>
            </div>
          ),
        }}
      />


        <div className="flex flex-wrap gap-x-2 gap-y-1">
            <div className='p-2'>
                <span className='text-xs text-gray-400 font-semibold p-1 '>DRONE ID</span>
                <p className='text-lg text-black font-bold p-1'>{droneId}</p>
            </div>
            <div>
              <LabelComponent
                label={{
                  subtitle: `DISTANCE BETWEEN`,
                  subtitleData: `${distance} meters`,
                }}
              />
            </div>
        </div>


          <LabelComponent
            label={{
              subtitle: 'RADAR RANGE (in meter)',
              subtitleData: radarInfo?.radar_range ?? '---',
            }}
          />
    </div>
  );
}
