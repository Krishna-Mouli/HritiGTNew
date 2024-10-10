import './App.css';
import { AppDrawer } from './Component/AppDrawer';
import Store from './Core/Store/Store';
import { Layout } from './Layout/Layout';
import { Provider } from 'react-redux';

function App() {
  return (
    <Provider store={Store}>
      <div className="App">
        <Layout/>
        {/* <AppDrawer/> */}
      </div>
    </Provider>
    
  );
}

export default App;
