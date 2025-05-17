import { Input } from "@/components/ui/input";
import { useEffect, useState } from "react";

import FileDropArea from "@/components/partnumber-input/FileDropArea";
import GlobalFileDropOverlay from "@/components/partnumber-input/GlobalFileDropOverlay";

function Home({ onStart, onInitialParts, onUpdateParts }) {
  const [showOverlay, setShowOverlay] = useState(false);
  const [parts, setParts] = useState([]);

  const handleFileSelected = async (file) => {
    onStart(); // direkt zur PartIdentification-Komponente wechseln

    const formData = new FormData();
    formData.append("file", file);

    try {
      // 1. Upload Excel und bekomme die Partnummern
      const parseRes = await fetch("http://localhost:8000/parse-excel", {
        method: "POST",
        body: formData,
      });

      const json = await parseRes.json();
      const partNumbers = json.partnumbers || [];

      // 2. Baue initiale Pending-Liste
      let partList = partNumbers.map((pn) => ({
        id: pn,
        partNumber: pn,
        status: "pending",
      }));

      onInitialParts(partList); // Zeige pending list

      // 3. Iteriere über jede Partnummer und identifiziere sie einzeln
      for (const part of partList) {
        try {
          // zuerst "searching" markieren
          partList = partList.map((p) => (p.id === part.id ? { ...p, status: "searching" } : p));
          onUpdateParts([...partList]);

          const res = await fetch(`http://localhost:8000/identify-part?partnumber=${encodeURIComponent(part.partNumber)}`);
          const data = await res.json();

          console.log("Identified part:", data);

          partList = partList.map((p) =>
            p.id === part.id
              ? {
                  ...p,
                  productType: data.productType,
                  manufacturer: data.manufacturer,
                  status: data.status,
                }
              : p
          );

          onUpdateParts([...partList]);
        } catch (err) {
          console.error("Fehler bei Identifikation:", err);
          partList = partList.map((p) => (p.id === part.id ? { ...p, status: "failed" } : p));
          onUpdateParts([...partList]);
        }
      }
    } catch (err) {
      console.error("Fehler beim Parsen der Datei:", err);
    }
  };

  useEffect(() => {
    let dragCounter = 0;

    const handleDragEnter = (e) => {
      e.preventDefault();
      dragCounter++;
      setShowOverlay(true);
    };

    const handleDragLeave = (e) => {
      e.preventDefault();
      dragCounter--;
      if (dragCounter === 0) setShowOverlay(false);
    };

    const handleDrop = (e) => {
      e.preventDefault();
      dragCounter = 0;
      setShowOverlay(false);

      const file = e.dataTransfer.files?.[0];
      if (file) {
        handleFileSelected(file);
      }
    };

    const preventDefault = (e) => {
      e.preventDefault();
      e.stopPropagation();
    };

    window.addEventListener("dragenter", handleDragEnter);
    window.addEventListener("dragleave", handleDragLeave);
    window.addEventListener("drop", handleDrop);
    window.addEventListener("dragover", preventDefault);

    return () => {
      window.removeEventListener("dragenter", handleDragEnter);
      window.removeEventListener("dragleave", handleDragLeave);
      window.removeEventListener("drop", handleDrop);
      window.removeEventListener("dragover", preventDefault);
    };
  }, []);

  return (
    <div className="min-h-screen flex flex-col w-full h-full gap-16 items-center justify-center bg-white p-6">
      <GlobalFileDropOverlay visible={showOverlay} />
      <div className="text-[72px] w-1/2 leading-[115%] tracking-[-3px] font-semibold text-center text-stone-800">
        Upload BOM <br />
        to find matching <br />
        <span className="text-[#D00C17]">Würth Elektronik </span>parts
      </div>
      <div className="w-1/2 flex flex-col gap-2">
        <div className="font-semibold text-neutral-600">xlsx file upload</div>
        <FileDropArea onSelectFile={handleFileSelected} />
      </div>
      <div className="w-1/2 flex flex-col gap-2">
        <div className="font-semibold text-neutral-600">single partnumber</div>
        <Input placeholder="XXXXXXXXXXXXXX" />
      </div>
    </div>
  );
}

export default Home;
