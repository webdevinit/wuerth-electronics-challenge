import Home from "@/components/pages/Home";
import PartIdentification from "@/components/pages/PartIdentification";
import { useState } from "react";

function App() {
  const [parts, setParts] = useState([]);
  const [showIdentification, setShowIdentification] = useState(false);

  const handleStartIdentification = (initialPartsPromise) => {
    // initialPartsPromise ist z. B. der fetch-Request vom File-Upload
    initialPartsPromise.then((partsStream) => {
      setParts(partsStream);
      setShowIdentification(true);
    });
  };

  return (
    <div className="min-h-screen flex flex-col w-full h-full gap-16 items-center justify-center bg-white p-6">
      {!showIdentification ? <Home onStartIdentification={handleStartIdentification} /> : <PartIdentification partData={parts} />}
    </div>
  );
}

export default App;
