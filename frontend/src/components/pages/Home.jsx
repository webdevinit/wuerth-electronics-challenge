import { Input } from "@/components/ui/input";
import { useEffect, useState } from "react";

import FileDropArea from "@/components/partnumber-input/FileDropArea";
import GlobalFileDropOverlay from "@/components/partnumber-input/GlobalFileDropOverlay";

function Home({ onStartIdentification }) {
  const [showOverlay, setShowOverlay] = useState(false);
  const [parts, setParts] = useState([]);

  const handleFileSelected = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/upload-excel", {
      method: "POST",
      body: formData,
    });

    if (!res.body) {
      console.error("Keine Streaming-Antwort erhalten");
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buffer = "";

    const partList = [];

    const streamParts = new Promise((resolve) => {
      (async () => {
        while (true) {
          const { value, done } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });

          const lines = buffer.split("\n\n");
          buffer = lines.pop() || "";

          for (const line of lines) {
            if (!line.startsWith("data: ")) continue;
            const jsonData = JSON.parse(line.replace("data: ", ""));

            if (jsonData.status === "initial") {
              const pendingParts = jsonData.partnumbers.map((pn, idx) => ({
                id: pn,
                partNumber: pn,
                status: "pending",
              }));
              partList.push(...pendingParts);
            } else if (jsonData.status === "processed") {
              const index = partList.findIndex((p) => p.id === jsonData.partnumber);
              if (index !== -1) {
                partList[index] = {
                  ...partList[index],
                  ...jsonData.data,
                  status: "identified",
                };
              }
            } else if (jsonData.status === "error") {
              const index = partList.findIndex((p) => p.id === jsonData.partnumber);
              if (index !== -1) {
                partList[index] = {
                  ...partList[index],
                  status: "failed",
                };
              }
            }
          }
        }

        resolve(partList);
      })();
    });

    // 🔁 Übergibt Promise an App
    onStartIdentification(streamParts);
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
