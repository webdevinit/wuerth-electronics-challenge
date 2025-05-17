import PartIdentification from "@/components/pages/PartIdentifiaction";
import partData from "@/data/partData.js"; // Assuming you have a parts.json file with your data

function App() {
  return (
    <div className="min-h-screen flex flex-col w-full h-full gap-16 items-center justify-center bg-white p-6">
      {/*<Home />*/}
      <PartIdentification partData={partData} />
    </div>
  );
}

export default App;
