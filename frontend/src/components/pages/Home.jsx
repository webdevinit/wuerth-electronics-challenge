import { Input } from "@/components/ui/input";
import { useEffect, useState } from "react";

import FileDropArea from "@/components/partnumber-input/FileDropArea";
import GlobalFileDropOverlay from "@/components/partnumber-input/GlobalFileDropOverlay";

function Home() {
  const [showOverlay, setShowOverlay] = useState(false);

  useEffect(() => {
    let dragCounter = 0;

    const handleDragEnter = (e) => {
      dragCounter++;
      setShowOverlay(true);
    };

    const handleDragLeave = (e) => {
      dragCounter--;
      if (dragCounter === 0) setShowOverlay(false);
    };

    const handleDrop = (e) => {
      dragCounter = 0;
      setShowOverlay(false);
    };

    const preventDefault = (e) => {
      e.preventDefault();
      e.stopPropagation();
    };

    window.addEventListener("dragenter", handleDragEnter);
    window.addEventListener("dragleave", handleDragLeave);
    window.addEventListener("dragover", preventDefault);
    window.addEventListener("drop", handleDrop);

    return () => {
      window.removeEventListener("dragenter", handleDragEnter);
      window.removeEventListener("dragleave", handleDragLeave);
      window.removeEventListener("dragover", preventDefault);
      window.removeEventListener("drop", handleDrop);
    };
  }, []);

  const handleFileSelected = (file) => {
    console.log("Ausgewählte Datei:", file);
    // Weiterverarbeitung hier
  };

  return (
    <div className="min-h-screen flex flex-col w-full h-full gap-16 items-center justify-center bg-white p-6">
      <GlobalFileDropOverlay visible={showOverlay} />
      <div className="text-[72px] w-1/2 leading-[115%] tracking-[-3px] font-semibold text-center text-stone-800">
        Upload BOM <br />
        to find matching <br />
        <span className="text-red-600">Würth Elektronik </span>parts
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
