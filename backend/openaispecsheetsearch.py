from dotenv import load_dotenv
import os
from openai import AzureOpenAI, OpenAI
from openai.types.shared import response_format_json_schema
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'env')
load_dotenv(dotenv_path=env_path, override=True)


from component_models import CapacitorModel, InductorModel, ResistorModel, ComponentBaseModel

def get_component_model_from_partnumber(partnumber: str):
    """
    Given a part number, use OpenAI to find the latest datasheet and return a populated component model.
    """
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini-search-preview-2025-03-11",
        messages=[
            {"role": "system", "content": (
                "You are an expert in electronic components and data extraction. "
                "You will be provided with a partnumber for an electronic component and your task is to find the latest datasheet for that component and fill out the following form for it. "
                "Output your answer as a JSON object matching exactly one of these Pydantic models: CapacitorModel, InductorModel, or ResistorModel. "
                "Dimensions should be in mm and in the format [length, width, height]. "
                "The technology field should specificly describe the type of the component its construction type, mounting type, and construction material and any other relevant specifications."
                "The JSON must use the exact field names and types as in the models below. "
                "Do not include any extra text, markdown, or code blocks—output only valid JSON. "
                "If a field is not available, use null for optional fields. "
                "Here are examples for each model:\n\n"
                "CapacitorModel example:\n"
                "{\n"
                "  \"name\": \"C1\",\n"
                "  \"manufacturer\": \"Murata\",\n"
                "  \"partnumber\": \"C1608X7R1H101K\",\n"
                "  \"capacitance\": \"100pF\",\n"
                "  \"rated_voltage\": \"50V\",\n"
                "  \"case_code\": \"0603\",\n"
                "  \"dimensions\": [0.8, 1.6, 0.8],\n"
                "  \"tolerance\": \"±10%\",\n"
                "  \"dielectric_material\": \"X7R\",\n"
                "  \"temp_coefficient\": null,\n"
                "  \"min_operating_temp\": \"-55°C\",\n"
                "  \"max_operating_temp\": \"125°C\",\n"
                "  \"component_type\": \"Capacitor\"\n"
                "  \"technology\": \"Capacitors Ceramic Capacitors\",\n"
                "}\n\n"
                "InductorModel example:\n"
                "{\n"
                "  \"name\": \"L1\",\n"
                "  \"manufacturer\": \"Würth Elektronik\",\n"
                "  \"partnumber\": \"7447779100\",\n"
                "  \"inductance\": \"10uH\",\n"
                "  \"rated_current\": \"1A\",\n"
                "  \"case_code\": \"1210\",\n"
                "  \"dimensions\": [2.5, 3.2, 2.5],\n"
                "  \"shielding\": \"Shielded\",\n"
                "  \"dc_resistance\": \"0.1ohm\",\n"
                "  \"tolerance\": \"±20%\",\n"
                "  \"min_operating_temp\": \"-40°C\",\n"
                "  \"max_operating_temp\": \"125°C\",\n"
                "  \"self_resonant_freq\": \"100MHz\",\n"
                "  \"component_type\": \"Inductor\"\n"
                "  \"technology\": \"Inductors For Digital Audio\",\n"
                "}\n\n"
                "ResistorModel example:\n"
                "{\n"
                "  \"name\": \"R1\",\n"
                "  \"manufacturer\": \"Vishay\",\n"
                "  \"partnumber\": \"CRCW0603100RFKEA\",\n"
                "  \"resistance\": \"100Ω\",\n"
                "  \"power_rating\": \"0.1W\",\n"
                "  \"case_code\": \"0603\",\n"
                "  \"dimensions\": [0.8, 1.6, 0.8],\n"
                "  \"tolerance\": \"±1%\",\n"
                "  \"temp_coefficient\": \"100ppm/°C\",\n"
                "  \"min_operating_temp\": \"-55°C\",\n"
                "  \"max_operating_temp\": \"155°C\",\n"
                "  \"component_type\": \"Resistor\"\n"
                "  \"technology\": \"Resis Precision Resistor\",\n"
                "}\n\n"
                "If you are unsure, make your best guess based on the partnumber and datasheet information."
            )},
            {"role": "user", "content": partnumber}
        ]
    )
    import json
    content = response.choices[0].message.content
    try:
        data = json.loads(content)
    except Exception:
        # If the model returns a code block or text, extract JSON
        import re
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
        else:
            raise ValueError("Could not parse model output as JSON.")

    # Try to instantiate the correct model
    for Model in (CapacitorModel, InductorModel, ResistorModel):
        try:
            return Model(**data)
        except Exception:
            continue
    raise ValueError("Could not match data to any known component model.")
