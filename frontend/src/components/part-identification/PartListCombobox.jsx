import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command";
import { Check, CircleArrowRight, Info, Loader2, X } from "lucide-react";
import * as React from "react";

export function PartListCombobox({ parts, onSelect }) {
  const [filter, setFilter] = React.useState("");
  const [selected, setSelected] = React.useState([]);
  const [allSelected, setAllSelected] = React.useState(false);
  const [selectionMode, setSelectionMode] = React.useState(false);

  const toggleSelection = (id) => {
    setSelected((prev) => (prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]));
  };

  const handleSelectAll = () => {
    const filteredParts = parts.filter((part) => `${part.productType} ${part.manufacturer} ${part.partNumber}`.toLowerCase().includes(filter.toLowerCase()));

    const filteredIds = filteredParts.filter((p) => p.status === "identified").map((p) => p.id);

    if (allSelected) {
      // deselect all
      setSelected((prev) => prev.filter((id) => !filteredIds.includes(id)));
      setAllSelected(false);
    } else {
      setSelected((prev) => Array.from(new Set([...prev, ...filteredIds])));
      setAllSelected(true);
    }
  };

  return (
    <div className="w-[800px] max-w-md border rounded-md space-y-2 p-4 border-none">
      <Command className="flex flex-col gap-2">
        <div className="flex gap-2 justify-between items-center">
          <Button variant="outline" size="sm" onClick={() => setSelectionMode(!selectionMode)}>
            {selectionMode ? "CANCEL" : "SELECT"}
          </Button>
          <CommandInput placeholder="filter parts..." className="h-10 w-[250px]" onValueChange={setFilter} />
        </div>
        <div className="flex justify-between items-center w-full">
          {selectionMode && (
            <Button variant="link" className="text-xs p-2" onClick={handleSelectAll}>
              {allSelected ? "UNSELECT ALL" : "SELECT ALL"}
            </Button>
          )}
          <div className="flex items-center w-full justify-end">
            <div className="flex items-center">
              <Info className="h-4 text-neutral-400" />
              <p className="text-sm text-neutral-400">
                identified: {parts.filter((p) => p.status === "identified").length} / {parts.length}
              </p>
            </div>
          </div>
        </div>
        <CommandList>
          <CommandEmpty>No parts found.</CommandEmpty>
          <CommandGroup>
            {parts
              .filter((part) => `${part.productType} ${part.manufacturer} ${part.partNumber}`.toLowerCase().includes(filter.toLowerCase()))
              .map((part) => (
                <CommandItem
                  key={part.id}
                  onSelect={() => {
                    if (part.status !== "identified") return; // ⛔️ nicht klickbar außer identified

                    if (selectionMode) {
                      toggleSelection(part.id);
                    } else {
                      setSelected([part.id]);
                      onSelect?.(part);
                    }
                  }}
                  className="flex items-center justify-between gap-2"
                >
                  {part.status === "identified" ? (
                    <>
                      <div className="flex items-center gap-4 px-3 py-1 bg-neutral-50 shadow-sm rounded-md">
                        {selectionMode && <Checkbox checked={selected.includes(part.id)} onCheckedChange={() => toggleSelection(part.id)} onClick={(e) => e.stopPropagation()} />}
                        <div>
                          <div className="font-medium">
                            {part.productType} ・ {part.manufacturer}
                          </div>
                          <div className="text-sm text-muted-foreground">{part.partNumber}</div>
                        </div>
                        <div className="flex-shrink-0">
                          <Check className="h-4 w-4 text-green-500" />
                        </div>
                      </div>
                    </>
                  ) : (
                    <>
                      <div className={`flex items-center gap-4 ${selectionMode ? "px-11" : "px-3"}`}>
                        <div>
                          {part.status === "searching" ? (
                            <div className="font-medium text-neutral-500">{part.partNumber}</div>
                          ) : part.status === "failed" ? (
                            <div className="font-light text-neutral-300">{part.partNumber}</div>
                          ) : (
                            <div className="text-neutral-500">{part.partNumber}</div>
                          )}
                        </div>
                        <div className="flex-shrink-0">
                          {part.status !== "failed" && <Loader2 className="h-4 w-4 animate-spin text-neutral-500" />}
                          {part.status === "failed" && (
                            <div className="flex items-center gap-1">
                              <X className="h-4 w-4 text-red-300" /> <p className="text-red-300">failed</p>
                            </div>
                          )}
                        </div>
                      </div>
                    </>
                  )}
                </CommandItem>
              ))}
          </CommandGroup>
        </CommandList>
      </Command>
      <div className="flex justify-end">
        <Button className="bg-[#D00C17]">
          {selectionMode && selected.length > 0 ? `MATCH ${selected.length} PART${selected.length === 1 ? "" : "S"}` : "MATCH ALL PARTS"} <CircleArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
