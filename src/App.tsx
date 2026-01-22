import { Routes,Route } from "react-router";
import VaultList from "./pages/VaultList";
import VaultPage from "./pages/VaultPage";


function App() {
  return (
    <Routes>
      <Route path="/" element={<VaultList />} />
      <Route path="/vault/:vaultId" element={<VaultPage />} />
    </Routes>

  );
}

export default App;
