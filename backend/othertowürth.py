import os
from dotenv import load_dotenv
from typing import List, Dict, Any

from openai import OpenAI
from urllib3 import response

# Import your component models
from component_models import ComponentBaseModel

# --- Environment Variable Loading ---
env_path = os.path.join(os.path.dirname(__file__), 'env')
load_dotenv(dotenv_path=env_path, override=True)


# --- Dummy Function Placeholder ---
def process_parsed_component(component_model: ComponentBaseModel):
    client = OpenAI()
    model = "gpt-4o"
    component = f"Component:{component_model.model_dump_json()})"
    # Reusing the prompt structure from main_processor_input.py
    messages =  [
            {
                "role": "system",
                "content": """
                You are an expert in electronic components and data extraction. 
                Your task is to analyze the provided datasheet of the given component and assign it to a json model from a diffrent manufacturer. 
                Dont output anything else than the json model.
                Here is the map on how to create the json model of the component: 
                {
  "Capacitors": {
  "Aluminum Electrolytic Capacitors": {
    "core": {
      "Capacitance": "Capacitance (\u00b5F)",
      "Rated Voltage": "Rated_Voltage (V)",
      "Dimensions": ["Length (mm)", "Diameter (mm)", "Pitch (mm)"]
    },
    "optional": {
      "Tolerance": null,
      "Operating Temperature (Minimum)": "Operating_Temperature (\u00b0C) Minimum",
      "Operating Temperature (Maximum)": "Operating_Temperature (\u00b0C) Maximum"
    }
  },
  "Aluminum Polymer Capacitors": {
    "core": {
      "Capacitance": "Capacitance (\u00b5F)",
      "Rated Voltage": "Rated_Voltage (V)",
      "Dimensions": ["Length (mm)", "Diameter (mm)", "Pitch (mm)"]
    },
    "optional": {
      "Tolerance": null,
      "Operating Temperature (Minimum)": "Operating_Temperature (\u00b0C) Minimum",
      "Operating Temperature (Maximum)": "Operating_Temperature (\u00b0C) Maximum"
    }
  },
  "Aluminum Hybrid Polymer Capacitors": {
    "core": {
      "Capacitance": "Capacitance (\u00b5F)",
      "Rated Voltage": "Rated_Voltage (V)",
      "Dimensions": ["Length (mm)", "Diameter (mm)"]
    },
    "optional": {
      "Tolerance": null,
      "Operating Temperature (Minimum)": null,
      "Operating Temperature (Maximum)": null
    }
  },
  "MLCCs - Multilayer Ceramic Chip Capacitors": {
    "core": {
      "Capacitance": "Capacitance (\u00b5F)",
      "Rated Voltage": "Rated_Voltage (V)",
      "Dimensions": ["Length (mm)", "Height (mm)", "Width (mm)"]
    },
    "optional": {
      "Tolerance": null,
      "Operating Temperature (Minimum)": "Operating_Temperature (\u00b0C) Minimum",
      "Operating Temperature (Maximum)": "Operating_Temperature (\u00b0C) Maximum"
    }
  },
  "Film Capacitors": {
    "core": {
      "Capacitance": "Capacitance (\u00b5F)",
      "Rated Voltage": "Rated_Voltage (V)",
      "Dimensions": ["Length (mm)", "Diameter (mm)", "Height (mm)", "Width (mm)", "Pitch (mm)"]
    },
    "optional": {
      "Tolerance": null,
      "Operating Temperature (Minimum)": "Operating_Temperature (\u00b0C) Minimum",
      "Operating Temperature (Maximum)": "Operating_Temperature (\u00b0C) Maximum"
    }
  },
  "Supercapacitors (EDLCs)": {
    "core": {
      "Capacitance": "Capacitance (\u00b5F)",
      "Rated Voltage": "Rated_Voltage (V)",
      "Dimensions": ["Length (mm)", "Diameter (mm)", "Pitch (mm)"]
    },
    "optional": {
      "Tolerance": null,
      "Operating Temperature (Minimum)": "Operating_Temperature (\u00b0C) Minimum",
      "Operating Temperature (Maximum)": "Operating_Temperature (\u00b0C) Maximum"
    }
  }

    },
    "Power Magnetics": {
    "Shielded Power Inductors": {
    "core": {
      "Inductance": "Inductance (\u00b5H)",
      "Rated Current": "Rated_Current (A)",
      "Dimensions": ["Size_Code", "Length (mm)", "Height (mm)", "Width (mm)"]
    },
    "optional": {
      "Tolerance": null,
      "DC Resistance": "DC_Resistance (\u03a9)",
      "Self-Resonant Frequency": "Self_Resonant_Frequency (MHz)",
      "Operating Temperature (Minimum)": "Operating_Temperature (\u00b0C) Minimum",
      "Operating Temperature (Maximum)": "Operating_Temperature (\u00b0C) Maximum"
    }
  }, 

  "Unshielded Power Inductors": {
    "core": {
      "Inductance": "Inductance (\u00b5H)",
      "Rated Current": "Rated_Current (A)",
      "Dimensions": ["Size_Code", "Length (mm)", "Height (mm)", "Width (mm)"]
    },
    "optional": {
      "Tolerance": null,
      "DC Resistance": "DC_Resistance (\u03a9)",
      "Self-Resonant Frequency": "Self_Resonant_Frequency (MHz)",
      "Operating Temperature (Minimum)": null,
      "Operating Temperature (Maximum)": null
    }
  },
  "High Voltage Power Inductors": {
    "core": {
      "Inductance": "Inductance (\u00b5H)",
      "Rated Current": "Rated_Current (A)",
      "Dimensions": ["Size_Code", "Length (mm)", "Height (mm)", "Width (mm)"]
    },
    "optional": {
      "Tolerance": null,
      "DC Resistance": "DC_Resistance (\u03a9)",
      "Self-Resonant Frequency": "Self_Resonant_Frequency (MHz)",
      "Operating Temperature (Minimum)": null,
      "Operating Temperature (Maximum)": null
    }
  },
  "Coupled Power Inductors": {
    "core": {
      "Inductance": "Inductance (\u00b5H)",
      "Rated Current": "Rated_Current (A)",
      "Dimensions": ["Size_Code", "Length (mm)", "Height (mm)", "Width (mm)"]
    },
    "optional": {
      "Tolerance": null,
      "DC Resistance": "DC_Resistance (\u03a9)",
      "Self-Resonant Frequency": "Self_Resonant_Frequency (MHz)",
      "Operating Temperature (Minimum)": null,
      "Operating Temperature (Maximum)": null
    }
  },
  "Inductors For Digital Audio": {
    "core": {
      "Inductance": "Inductance (\u00b5H)",
      "Rated Current": "Rated_Current (A)",
      "Dimensions": ["Length (mm)", "Height (mm)", "Width (mm)"]
    },
    "optional": {
      "Tolerance": null,
      "DC Resistance": "DC_Resistance (\u03a9)",
      "Self-Resonant Frequency": "Self_Resonant_Frequency (MHz)",
      "Operating Temperature (Minimum)": null,
      "Operating Temperature (Maximum)": null
    }
  },
  "Air Core Power Inductor": {
    "core": {
      "Inductance": "Inductance (\u00b5H)",
      "Rated Current": "Rated_Current (A)",
      "Dimensions": ["Size_Code", "Length (mm)", "Height (mm)", "Width (mm)"]
    },
    "optional": {
      "Tolerance": null,
      "DC Resistance": "DC_Resistance (\u03a9)",
      "Self-Resonant Frequency": "Self_Resonant_Frequency (MHz)",
      "Operating Temperature (Minimum)": null,
      "Operating Temperature (Maximum)": null
    }
  }
},
    "Resistors": {
    "Thick Film Resistors": {
    "core": {
      "Resistance": "Resistance (Ohm)",
      "Power Rating": "Rated_Power (W)",
      "Dimensions": ["Size_Code", "Length (mm)", "Height (mm)", "Width (mm)"]
    },
    "optional": {
      "Tolerance": null,
      "Operating Temperature (Minimum)": null,
      "Operating Temperature (Maximum)": null
    }
  },

    "Metal Plate Resistors": {
  "core": {
    "Resistance": "Resistance (Ohm)",
    "Power Rating": "Rated_Power (W)",
    "Dimensions": ["Size_Code", "Length (mm)", "Height (mm)", "Width (mm)"]
  },
  "optional": {
    "Tolerance": null,
    "Operating Temperature (Minimum)": null,
    "Operating Temperature (Maximum)": null
  }
    }

    }
}
                This map marks which fields are most important for the following steps, upmost important are the product group
                This can be taken, Product family as well as other core attributes
                Dont take the map as example for the output format, for the format just rely on the examples 
                Then, extract all relevant specifications for that component type. 
                Format your output following the examples.
                Ensure all required fields in the chosen model are populated. If a value is not present or applicable, use null. 
                Pay close attention to units and formats as described in the model fields.
                Examples:
                R1,Vishay,CRCW06030000Z0EA,Resistor,0Ω,0.1W,0603,"(1.55, 0.85, 0.5)",Jumper,±100ppm/°C,-55°C,155°C,Resistors Thick Film Surface Mount
                    {
                    "Product_Group": "Resistors",
                    "Product_Family": "Thick Film Resistors",
                    "Resistance (Ohm)": "",
                    "Rated_Power (W)": 0.1,
                    "Size_Code": 0603,
                    "Length (mm)": 1.55,
                    "Height (mm)": 0.5,
                    "Width (mm)": 0.85,
                    "Operating_Temperature (\u00b0C) Minimum": -55,
                    "Operating_Temperature (\u00b0C) Maximum": 155

                        }
                    SER201-202MLD,Coilcraft,SER201-202MLD,Inductor,2µH,45A,2010,"(19.18, 9.27, 9.4)",Shielded,1mΩ,±20%,-40°C,85°C,48MHz,Inductors For Digital Audio
                    {
                        "Product_Group": "Power Magnetics",
                        "Product_Family": "Shielded Power Inductors",
                        "Inductance (\u00b5H)": 2,
                        "Rated_Current (A)": "45",
                        "Size_Code": "2010",
                        "Length (mm)": "19.18",
                        "Height (mm)": "9.4",
                        "Width (mm)": "9.27",
                        "DC_Resistance (\u03a9)": 0.001,
                        "Self_Resonant_Frequency (MHz)": 48,
                        "Operating_Temperature (\u00b0C) Minimum": -40,
                        "Operating_Temperature (\u00b0C) Maximum": 85
                    }
                    C1,TDK,CKG57NX7S2A226M500JH,Capacitor,15000000µF,2.7V,"13.0 x 25.0", (5.0, 25.0, 14),-40°C,85°C
                    {
                        "Product_Group": "Capacitors",
                        "Product_Family": "Supercapacitors (EDLCs)",
                        "Capacitance (\u00b5F)": 15000000,
                        "Rated_Voltage (V)": 2.7,
                        "Operating_Temperature (\u00b0C) Minimum": -40,
                        "Operating_Temperature (\u00b0C) Maximum": 85,
                        "Pitch (mm)": 5,
                        "Length (mm)": 25,
                        "Diameter (mm)": 13,
                        "Size_Code": "13.0 x 25.0"
                    }
"""},
            {"role": "user", "content": f"Please process the following component: {component}"}
        ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    import json 
    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except Exception:
        # If the model returns a code block or text, extract JSON
        import re
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            raise ValueError("Could not parse model output as JSON.")
    finally:
        print(content)

