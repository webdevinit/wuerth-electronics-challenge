import Home from "@/components/pages/Home";
import PartIdentification from "@/components/pages/PartIdentification";
import { useState } from "react";

function App() {
  const [parts, setParts] = useState([]);
  const [showIdentification, setShowIdentification] = useState(false);

  return (
    <div className="min-h-screen flex flex-col w-full h-full gap-16 items-center justify-center bg-white p-6">
      {!showIdentification ? (
        <Home
          onStart={() => setShowIdentification(true)} // ← direkt anzeigen
          onInitialParts={(initialParts) => setParts(initialParts)}
          onUpdateParts={(updatedParts) => setParts(updatedParts)}
        />
      ) : (
        <PartIdentification partData={parts} />
      )}
    </div>
  );
}

export default App;
