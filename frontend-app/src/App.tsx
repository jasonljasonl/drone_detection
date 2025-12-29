import DroneDisplay from './components/DroneDisplay';
import RadarDisplay from './components/RadarDisplay';
import RadarApiCall from './components/ApiCalls/RadarApiCall';
import WebsocketData from './components/WebsocketData';

function App() {
  const data = WebsocketData();
  const radars = RadarApiCall();

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
    <>
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

      <DroneDisplay selectedDrone="drone" data={data} />
    </>
  );
}

export default App;
