import { Upload } from "lucide-react";
import { useRef } from "react";

const FileDropArea = ({ onSelectFile }) => {
  const inputRef = useRef();
  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file && onSelectFile) {
      onSelectFile(file); // ✅ Datei an Callback übergeben
    }
  };

  const openFileDialog = () => {
    inputRef.current?.click();
  };

  const handleFileChange = (e) => {
    const files = e.target.files;
    if (files && files[0]) {
      onSelectFile(files[0]); // ✅ Auch bei manueller Auswahl
    }
  };

  return (
    <div
      onClick={openFileDialog}
      onDrop={handleDrop}
      className="border border-dashed border-gray-300 rounded-xl p-12 text-center cursor-pointer hover:bg-gray-50 transition-colors shadow-xs duration-150 gap-2 flex flex-col"
    >
      <div className="flex items-center justify-center">
        <Upload />
      </div>
      <p className="text-gray-800 font-semibold text-lg">
        Datei hier her ziehen, oder <span className="text-[#D00C17] underline">auswählen</span>
      </p>
      <p className="text-sm text-gray-500 mt-2">Unterstützte Formate: xlsx</p>
      <input type="file" accept="application/pdf" ref={inputRef} onChange={handleFileChange} hidden />
    </div>
  );
};

export default FileDropArea;
