import logo from './logo.svg';
import './App.css';
import { Route, Router, Switch } from 'react-router-dom';
import AllEvents from './views/AllEvents';
import { createBrowserHistory } from 'history';
import "bootstrap/dist/css/bootstrap.min.css";
import { EventsProvider } from './context/EventsContext';
const history = createBrowserHistory();

function App() {
  return (
    <EventsProvider>
      <Router history={history}>
        <Switch>
        <Route path="/" component={AllEvents} />
        </Switch>
      </Router>
    </EventsProvider>
  );
}

export default App;
