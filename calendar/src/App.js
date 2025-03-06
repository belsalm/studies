import './App.css';
import Calendar from 'reactjs-availability-calendar'
import bookings from './bookings'

function App() {

  return (
    <div className="App">
      <Calendar
        bookings={bookings}
        showControls={true}
        showKey={false}
      />
    </div>
  );
}

export default App;
