import Navbar from '../components/Navbar';
import RankingsPage from '../pages/RankingsPage';

//React Imports
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import VotePage from '../pages/VotePage';

const App = () => {

  return (
    <Router>
      <Navbar />
      <main>
        <Routes>
            <Route path="/" exact element={<Navigate to="/vote" />}></Route>
            <Route path="/vote" element={ <VotePage /> }></Route>
            <Route path="/rankings" element={<RankingsPage />}></Route>
            <Route path="/calculator"></Route>
        </Routes>
      </main>
    </Router>
  )
}
export default App;