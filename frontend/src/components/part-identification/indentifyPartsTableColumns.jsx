import { Check, Loader2, X } from "lucide-react";

export const columns = [
  {
    accessorKey: "productType",
    header: "Part Type",
    cell: ({ row }) => row.getValue("productType"),
  },
  {
    accessorKey: "manufacturer",
    header: "Manufacturer",
    cell: ({ row }) => row.getValue("manufacturer"),
  },
  {
    accessorKey: "partNumber",
    header: "Part Number",
    cell: ({ row }) => row.getValue("partNumber"),
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const status = row.getValue("status");
      if (status === "searching") return <Loader2 className="animate-spin text-yellow-500" />;
      if (status === "identified") return <Check className="text-green-500" />;
      return <X className="text-red-500" />;
    },
  },
];
