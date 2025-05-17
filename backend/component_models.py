from typing import Optional, List, Union, ClassVar
from pydantic import BaseModel, Field, ConfigDict

class CapacitorModel(BaseModel):
    """Pydantic model for a Capacitor."""
    name: str = Field(description="Name of the component, e.g., 'C1', 'Ceramic Capacitor 10uF'")
    manufacturer: str = Field(description="Manufacturer of the capacitor")
    partnumber: str = Field(None, description="Part number of the capacitor")
    capacitance: str = Field(description="Capacitance value (e.g., '10uF', '100pF')")
    rated_voltage: str = Field(description="Rated voltage (e.g., '25V', '50V')")
    case_code: Optional[str] = Field(None, description="Case code, if available")
    dimensions: Optional[List[float]] = Field(None, description="Dimensions (Height, Length, Width) in mm as a list of 3 floats", min_length=3, max_length=3)
    tolerance: Optional[str] = Field(None, description="Tolerance (e.g., '±10%', '0.1pF')")
    dielectric_material: Optional[str] = Field(None, description="Dielectric material")
    temp_coefficient: Optional[str] = Field(None, description="Temperature coefficient")
    min_operating_temp: Optional[str] = Field(None, description="Minimum operating temperature (e.g., '-55°C')")
    max_operating_temp: Optional[str] = Field(None, description="Maximum operating temperature (e.g., '125°C')")
    component_type: str = Field("Capacitor", description="Type of component, fixed to 'Capacitor'")
    technology: Optional[str] = Field(None, description="Technology, material, build of the capacitor (e.g., 'Ceramic Capacitors', 'THT')")
    category: ClassVar[str] = "Capacitor"

class InductorModel(BaseModel):
    """Pydantic model for an Inductor."""
    name: str = Field(description="Name of the component, e.g., 'L1', 'Power Inductor 100uH'")
    manufacturer: str = Field(description="Manufacturer of the inductor")
    partnumber: str = Field(None, description="Part number of the inductor")
    inductance: str = Field(description="Inductance value (e.g., '100uH', '10mH')")
    rated_current: str = Field(description="Rated current (e.g., '1A', '500mA')")
    case_code: Optional[str] = Field(None, description="Case code, if available")
    dimensions: Optional[List[float]] = Field(None, description="Dimensions (Height, Length, Width) in mm as a list of 3 floats", min_length=3, max_length=3)
    shielding: Optional[str] = Field(None, description="Shielding type, if any")
    dc_resistance: Optional[str] = Field(None, description="DC resistance (e.g., '0.1ohm', '10mohm')")
    tolerance: Optional[str] = Field(None, description="Tolerance (e.g., '±20%')")
    min_operating_temp: Optional[str] = Field(None, description="Minimum operating temperature")
    max_operating_temp: Optional[str] = Field(None, description="Maximum operating temperature")
    self_resonant_freq: Optional[str] = Field(None, description="Self-resonant frequency (e.g., '100MHz')")
    component_type: str = Field("Inductor", description="Type of component, fixed to 'Inductor'")
    technology: Optional[str] = Field(None, description="Technology, material, build of the inductor (e.g., 'Inductors For Digital Audio')")
    category: ClassVar[str] = "Inductor"

class ResistorModel(BaseModel):
    """Pydantic model for a Resistor."""
    name: str = Field(description="Name of the component, e.g., 'R1', 'SMD Resistor 1kOhm'")
    manufacturer: str = Field(description="Manufacturer of the resistor")
    partnumber: str = Field(None, description="Part number of the resistor")
    resistance: str = Field(description="Resistance value (e.g., '1kOhm', '100R')")
    power_rating: str = Field(description="Power rating (e.g., '0.25W', '1/8W')")
    case_code: Optional[str] = Field(None, description="Case code, if available")
    dimensions: Optional[List[float]] = Field(None, description="Dimensions (Height, Length, Width) in mm as a list of 3 floats", min_length=3, max_length=3)
    tolerance: Optional[str] = Field(None, description="Tolerance (e.g., '±1%', '±5%')")
    temp_coefficient: Optional[str] = Field(None, description="Temperature coefficient (e.g., '100ppm/°C')")
    min_operating_temp: Optional[str] = Field(None, description="Minimum operating temperature")
    max_operating_temp: Optional[str] = Field(None, description="Maximum operating temperature")
    component_type: str = Field("Resistor", description="Type of component, fixed to 'Resistor'")
    technology: Optional[str] = Field(None, description="Technology, material, build of the resistor (e.g., 'Resis Precision Resistor')")
    category: ClassVar[str] = "Resistor"

class ComponentBaseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    """Base model for all components. The LLM will populate one of these models."""
    final_ouput: Union[CapacitorModel, InductorModel, ResistorModel]