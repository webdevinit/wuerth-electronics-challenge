import { PartListCombobox } from "@/components/part-identification/PartListCombobox";
import { useState } from "react";

export default function PartIdentification({ partData }) {
  const [parts, setParts] = useState(partData || []);

  /*const handleFileUpload = async (file) => {
    const res = await fetch("/api/identify", {
      method: "POST",
      body: file,
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let partial = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      partial += decoder.decode(value, { stream: true });

      const lines = partial.split("\n").filter(Boolean);
      for (const line of lines) {
        try {
          const item = JSON.parse(line);
          setParts((prev) => [...prev, item]);
        } catch (e) {
          console.error("Invalid JSON line:", line);
        }
      }

      partial = "";
    }
  };*/

  return (
    <div className="p-6 space-y-6">
      <PartListCombobox parts={parts} onSelect={(part) => console.log("Selected", part)} />
    </div>
  );
}
