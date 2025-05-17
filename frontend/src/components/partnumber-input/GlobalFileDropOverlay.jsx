const GlobalFileDropOverlay = ({ visible }) => {
  if (!visible) return null;

  return (
    <div className="fixed inset-0 bg-red-500/50 z-50 flex items-center justify-center pointer-events-none">
      <div className="relative w-full h-full">
        {/* Ecke oben links */}
        <div className="absolute top-8 left-8 w-10 h-10 border-t-8 border-l-8 border-white rounded-tl-xl" />

        {/* Ecke oben rechts */}
        <div className="absolute top-8 right-8 w-10 h-10 border-t-8 border-r-8 border-white rounded-tr-xl" />

        {/* Ecke unten links */}
        <div className="absolute bottom-8 left-8 w-10 h-10 border-b-8 border-l-8 border-white rounded-bl-xl" />

        {/* Ecke unten rechts */}
        <div className="absolute bottom-8 right-8 w-10 h-10 border-b-8 border-r-8 border-white rounded-br-xl" />

        {/* Zentraler Text */}
        <div className="absolute inset-0 flex items-center justify-center">
          <h1 className="text-white text-3xl md:text-5xl font-bold">Datei hier ablegen</h1>
        </div>
      </div>
    </div>
  );
};

export default GlobalFileDropOverlay;
