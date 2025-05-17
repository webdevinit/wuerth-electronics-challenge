import { SelectedPartListCombobox } from "@/components/part-matching/SelectedPartListCombobox";
import matchingData from "@/data/matchingData";

export default function PartMatching() {
  /*if (!matchingData || matchingData.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center gap-8 w-full">
        <div className="text-[72px] w-1/2 leading-[115%] tracking-[-3px] font-semibold text-center text-stone-800">Product Matches</div>

        <div className="flex items-center justify-center h-full space-x-2">
          <div className="text-gray-500 text-2xl">finding similar products from product catalog...</div>
          <Loader2
            className="h-5 w-5
         animate-spin text-neutral-500"
          />
        </div>
      </div>
    );
  }*/

  return (
    <div className="flex flex-col items-center justify-center gap-8 w-full">
      <div className="text-[72px] w-1/2 leading-[115%] tracking-[-3px] font-semibold text-center text-stone-800">Product Matches</div>

      <div className="p-6 space-y-6">
        <SelectedPartListCombobox parts={matchingData} />
      </div>
    </div>
  );
}
