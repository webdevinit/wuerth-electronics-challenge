import Home from "@/components/pages/Home";
import PartIdentification from "@/components/pages/PartIdentification";
import PartMatching from "@/components/pages/PartMatching";
import logo from "@/images/logo.png";
import { useState } from "react";

function App() {
  const [parts, setParts] = useState([]);
  const [showIdentification, setShowIdentification] = useState(false);
  const [showMatching, setShowMatching] = useState(false);

  return (
    <div className="min-h-screen flex flex-col w-full h-full gap-16 items-center justify-center bg-white p-6">
      <img src={logo} alt="Logo" className="absolute top-[5%] left-[5%] h-16" />
      {showIdentification ? (
        <PartIdentification partData={parts} />
      ) : showMatching ? (
        <PartMatching matchingData={parts} selectedPartData={parts} onSelect={(part) => console.log("Selected", part)} />
      ) : (
        <Home
          onStart={() => setShowIdentification(true)} // ← direkt anzeigen
          onInitialParts={(initialParts) => setParts(initialParts)}
          onUpdateParts={(updatedParts) => setParts(updatedParts)}
        />
      )}
    </div>
  );
}

export default App;
