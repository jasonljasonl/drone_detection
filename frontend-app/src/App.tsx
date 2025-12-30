import DroneDisplay from './components/DroneDisplay';
import RadarDisplay from './components/RadarDisplay';
import RadarApiCall from './components/ApiCalls/RadarApiCall';
import WebsocketData from './components/WebsocketData';
import LeafletMap from './components/LeafletMap';


function App() {
  const data = WebsocketData();
  const radars = RadarApiCall();
  const drone = data.drone ? { latitude: Number(data.drone.latitude), longitude: Number(data.drone.longitude) } : undefined;
  const radar1 = 'home-radar';
  const radar2 = 'downtown-radar';

  const getRadarPosition = (name: string) => {
    const radar = radars.find(r => r.name === name);
    return radar
      ? radar.radar_position
      : { latitude: 0, longitude: 0, altitude: 0 };
  };

  if (radars.length === 0) return <p>Loading radars…</p>;

  return (
    <div className='grid xl:grid-cols-3 h-screen'>
        <div className='lg:col-span-1 overflow-auto'>

           <h1 className='text-3xl text-center p-8'>DRONE DETECTION</h1>

            <div className="flex items-center gap-4 p-4">
              <hr className="flex-1 border-t border-black" />
              <h2 className="text-2xl font-semibold ">Drones</h2>
              <hr className="flex-1 border-t border-black" />
            </div>

           <DroneDisplay selectedDrone="drone" data={data} />


            <div className="flex items-center gap-4 p-4">
              <hr className="flex-1 border-t border-black" />
              <h2 className="text-2xl font-semibold ">Radars</h2>
              <hr className="flex-1 border-t border-black" />
            </div>

            <RadarDisplay
                selectedRadar={radar1}
                data={data}
                radarPosition={getRadarPosition(radar1)}
                radarInfo={radars.find(r => r.name === radar1)}
            />

            <RadarDisplay
                selectedRadar={radar2}
                data={data}
                radarPosition={getRadarPosition(radar2)}
                radarInfo={radars.find(r => r.name === radar1)}
            />

        </div>

          <div className='lg:col-span-2 h-full'>
            <LeafletMap
              drones={drone ? [drone] : []}
              radars={radars.map(r => r.radar_position)}
            />
          </div>
        </div>
  );
}

export default App;
