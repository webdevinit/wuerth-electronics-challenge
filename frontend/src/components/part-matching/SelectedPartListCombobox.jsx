import { Button } from "@/components/ui/button";
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command";
import { Check, CircleArrowRight, Info } from "lucide-react";
import * as React from "react";

export function SelectedPartListCombobox({ parts }) {
  const [filter, setFilter] = React.useState("");

  return (
    <div className="w-[800px] max-w-md border rounded-md space-y-2 p-4 border-none">
      <Command className="flex flex-col gap-2">
        <div className="flex gap-2 justify-between items-center">
          <CommandInput placeholder="filter parts..." className="h-10 w-[250px]" onValueChange={setFilter} />
        </div>
        <div className="flex justify-between items-center w-full">
          <div className="flex items-center w-full justify-end">
            <div className="flex items-center">
              <Info className="h-4 text-neutral-400" />
              <p className="text-sm text-neutral-400"></p>
            </div>
          </div>
        </div>
        <CommandList>
          <CommandEmpty>No parts found.</CommandEmpty>
          <CommandGroup>
            {parts
              .filter((part) => `${part.productType} ${part.manufacturer} ${part.partNumber}`.toLowerCase().includes(filter.toLowerCase()))
              .map((part) => (
                <CommandItem key={part.id} className="flex items-center justify-between gap-2">
                  <>
                    <div className="flex items-center gap-4 px-3 py-1 bg-neutral-50 shadow-sm rounded-md">
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
                </CommandItem>
              ))}
          </CommandGroup>
        </CommandList>
      </Command>
      <div className="flex justify-end">
        <Button className="bg-[#D00C17]">
          "MATCH ALL PARTS" <CircleArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
