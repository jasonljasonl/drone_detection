import DroneDisplay from './components/DroneDisplay';
import RadarDisplay from './components/RadarDisplay';
import WebsocketData from './components/WebsocketData';

function App() {
    const data = WebsocketData();
  return (
    <>
      <RadarDisplay selectedRadar="home-radar" data={data} />
      <RadarDisplay selectedRadar="downtown-radar" data={data} />
      <DroneDisplay selectedDrone="drone" data={data} />
    </>
  );
}

export default App;
