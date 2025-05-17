import { PartListCombobox } from "@/components/part-identification/PartListCombobox";
import { Loader2 } from "lucide-react";

export default function PartIdentification({ partData }) {
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
  if (!partData || partData.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center gap-8 w-full">
        <div className="text-[72px] w-1/2 leading-[115%] tracking-[-3px] font-semibold text-center text-stone-800">Indetifying Parts</div>
        <div className="flex items-center justify-center h-full space-x-2">
          <div className="text-gray-500 text-2xl">extracting partnumbers from file...</div>{" "}
          <Loader2
            className="h-5 w-5
         animate-spin text-neutral-500"
          />
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center gap-8 w-full">
      <div className="text-[72px] w-1/2 leading-[115%] tracking-[-3px] font-semibold text-center text-stone-800">Indetifying Parts</div>

      <div className="p-6 space-y-6">
        <PartListCombobox parts={partData} onSelect={(part) => console.log("Selected", part)} />
      </div>
    </div>
  );
}
