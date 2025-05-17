import pandas as pd
import os
from openaispecsheetsearch import get_component_model_from_partnumber
from main_processor_input import save_components_to_csv
from classes import Capacitor as AppCapacitor, Inductor as AppInductor, Resistor as AppResistor

def filter_and_save_partnumbers(input_csv):
    # Read the CSV
    df = pd.read_csv(input_csv)
    # Filter partnumbers with length >= 5
    filtered = df[df['partnumber'].astype(str).str.len() >= 5]
    # Save to new CSV
    return filtered 

def test_partnumber_to_component_and_save(input_csv, output_dir):
    df = input_csv
    partnumbers = df['partnumber'].astype(str)
    components = []
    for pn in partnumbers:
        try:
            model = get_component_model_from_partnumber(pn)
            # Wrap in AppCapacitor/AppInductor/AppResistor for CSV saving
            if hasattr(model, "component_type"):
                if model.component_type == "Capacitor":
                    comp = AppCapacitor(
                        name=model.name,
                        manufacturer=model.manufacturer,
                        partnumber=model.partnumber,
                        capacitance=model.capacitance,
                        rated_voltage=model.rated_voltage,
                        case_code=model.case_code,
                        dimensions=tuple(model.dimensions) if model.dimensions else None,
                        tolerance=model.tolerance,
                        dielectric_material=model.dielectric_material,
                        temp_coefficient=model.temp_coefficient,
                        min_operating_temp=model.min_operating_temp,
                        max_operating_temp=model.max_operating_temp
                    )
                elif model.component_type == "Inductor":
                    comp = AppInductor(
                        name=model.name,
                        manufacturer=model.manufacturer,
                        partnumber=model.partnumber,
                        inductance=model.inductance,
                        rated_current=model.rated_current,
                        case_code=model.case_code,
                        dimensions=tuple(model.dimensions) if model.dimensions else None,
                        shielding=model.shielding,
                        dc_resistance=model.dc_resistance,
                        tolerance=model.tolerance,
                        min_operating_temp=model.min_operating_temp,
                        max_operating_temp=model.max_operating_temp,
                        self_resonant_freq=model.self_resonant_freq
                    )
                elif model.component_type == "Resistor":
                    comp = AppResistor(
                        name=model.name,
                        manufacturer=model.manufacturer,
                        partnumber=model.partnumber,
                        resistance=model.resistance,
                        power_rating=model.power_rating,
                        case_code=model.case_code,
                        dimensions=tuple(model.dimensions) if model.dimensions else None,
                        tolerance=model.tolerance,
                        temp_coefficient=model.temp_coefficient,
                        min_operating_temp=model.min_operating_temp,
                        max_operating_temp=model.max_operating_temp
                    )
                else:
                    continue
                components.append(comp)
        except Exception as e:
            print(f"Failed for {pn}: {e}")
    save_components_to_csv(components, output_dir)

if __name__ == "__main__":
    input_csv = "backend/Traffic Analysis/search_results.csv"
    output_csv = "backend/Traffic Analysis/new_cap.csv"
    numbers = filter_and_save_partnumbers(input_csv)
    # Now run the test
    test_partnumber_to_component_and_save(numbers, "backend/Traffic Analysis/component_csvs")