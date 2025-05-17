const matchingData = [
  {
    part_competitor: {
      id: "123456789",
      manufacturer: "Siemens",
      partnumber: "123456789",
      specs: [
        { attribute: "Order_Code", value: "890324025031CS" },
        { attribute: "Product_Group", value: "Capacitors" },
        { attribute: "Product_Series", value: "WCAP-FTX2 Film Capacitors" },
        { attribute: "Product_Family", value: "Film Capacitors" },
        { attribute: "Capacitance (µF)", value: 0.27 },
        { attribute: "Rated_Voltage (V)", value: 275 },
        { attribute: "Rated_Voltage_2 (V)", value: 560 },
        { attribute: "Rate_Of_Voltage_Rise (V/µs)", value: 250 },
        { attribute: "Dissipation_Factor (%)", value: 3 },
        { attribute: "Operating_Temperature (°C) Minimum", value: -40 },
        { attribute: "Operating_Temperature (°C) Maximum", value: 105 },
        { attribute: "Safety_Class", value: "X2" },
        { attribute: "Pitch (mm)", value: 15 },
        { attribute: "Length (mm)", value: 18 },
        { attribute: "Width (mm)", value: 7.5 },
        { attribute: "Height (mm)", value: 14.5 },
        { attribute: "Size_Code", value: "Pitch 15 mm" }
      ]
    },
    wuerth_suggestions: [
      {
        Order_Code: "890334025031CS",
        specs: [
          { attribute: "Capacitance (µF)", values: [0.27, 0.27], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Rated_Voltage (V)", values: [310, 275], rule_outcome: "good", operator: ">=" },
          { attribute: "Length (mm)", values: [18, 18], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Height (mm)", values: [14.5, 14.5], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Width (mm)", values: [7.5, 7.5], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Pitch (mm)", values: [15, 15], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Operating_Temperature (°C) Minimum", values: [-40, -40], rule_outcome: "good", operator: "<=" },
          { attribute: "Operating_Temperature (°C) Maximum", values: [105, 105], rule_outcome: "good", operator: ">=" }
        ]
      },
      {
        Order_Code: "890324025031",
        specs: [
          { attribute: "Capacitance (µF)", values: [0.27, 0.27], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Rated_Voltage (V)", values: [275, 275], rule_outcome: "good", operator: ">=" },
          { attribute: "Length (mm)", values: [18, 18], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Height (mm)", values: [14.5, 14.5], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Width (mm)", values: [7.5, 7.5], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Pitch (mm)", values: [15, 15], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Operating_Temperature (°C) Minimum", values: [-40, -40], rule_outcome: "good", operator: "<=" },
          { attribute: "Operating_Temperature (°C) Maximum", values: [105, 105], rule_outcome: "good", operator: ">=" }
        ]
      },
      {
        Order_Code: "890334025031",
        specs: [
          { attribute: "Capacitance (µF)", values: [0.27, 0.27], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Rated_Voltage (V)", values: [310, 275], rule_outcome: "good", operator: ">=" },
          { attribute: "Length (mm)", values: [18, 18], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Height (mm)", values: [14.5, 14.5], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Width (mm)", values: [7.5, 7.5], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Pitch (mm)", values: [15, 15], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Operating_Temperature (°C) Minimum", values: [-40, -40], rule_outcome: "good", operator: "<=" },
          { attribute: "Operating_Temperature (°C) Maximum", values: [105, 105], rule_outcome: "good", operator: ">=" }
        ]
      },
      {
        Order_Code: "890324025031CS",
        specs: [
          { attribute: "Capacitance (µF)", values: [0.27, 0.27], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Rated_Voltage (V)", values: [275, 275], rule_outcome: "good", operator: ">=" },
          { attribute: "Length (mm)", values: [18, 18], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Height (mm)", values: [14.5, 14.5], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Width (mm)", values: [7.5, 7.5], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Pitch (mm)", values: [15, 15], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Operating_Temperature (°C) Minimum", values: [-40, -40], rule_outcome: "good", operator: "<=" },
          { attribute: "Operating_Temperature (°C) Maximum", values: [105, 105], rule_outcome: "good", operator: ">=" }
        ]
      },
      {
        Order_Code: "890303325010CS",
        specs: [
          { attribute: "Capacitance (µF)", values: [0.22, 0.27], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Rated_Voltage (V)", values: [630, 275], rule_outcome: "good", operator: ">=" },
          { attribute: "Length (mm)", values: [18, 18], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Height (mm)", values: [14, 14.5], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Width (mm)", values: [8, 7.5], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Pitch (mm)", values: [15, 15], rule_outcome: "tolerated", operator: "=" },
          { attribute: "Operating_Temperature (°C) Minimum", values: [-40, -40], rule_outcome: "good", operator: "<=" },
          { attribute: "Operating_Temperature (°C) Maximum", values: [105, 105], rule_outcome: "good", operator: ">=" }
        ]
      }
    ]
  }
];

export default matchingData;