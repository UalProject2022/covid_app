import { Route, Routes } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import { ConsultPage } from './pages/ConsultPage';
import { HomePage } from './pages/HomePage';
import { MapPage } from './pages/MapPage';
export const API_URL = '';

function App() {
  return (
    <div>
      <Layout>
        <Routes>
          <Route path='/' element={<HomePage />} />
          <Route path='/map' element={<MapPage />} />
          <Route path='/consult' element={<ConsultPage />} />
        </Routes>
      </Layout>
    </div>
  );
}

export default App
