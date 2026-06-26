/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import PedestalCalculator from './pages/PedestalCalculator';
import WorkstationCalculator from './pages/WorkstationCalculator';
import LShapeTableCalculator from './pages/LShapeTableCalculator';
import CustomStorageCalculator from './pages/CustomStorageCalculator';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="calculator/pedestal" element={<PedestalCalculator />} />
          <Route path="calculator/workstation" element={<WorkstationCalculator />} />
          <Route path="calculator/l-shape-table" element={<LShapeTableCalculator />} />
          <Route path="calculator/custom-storage" element={<CustomStorageCalculator />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
