class Component:
    """Base class for electronic components."""
    
    def __init__(self, name, manufacturer, partnumber):
        self.name = name
        self.manufacturer = manufacturer
        self.partnumber = partnumber
        self.category = None  # Will be set by child classes
        self.technology = None 


class Capacitor(Component):
    """
    Capacitor component class.
    
    Core Constraints:
    - Capacitance: Equal (=)
    - Rated Voltage: Greater than or equal (>=)
    - Case Code or Dimensions: Equal (=)
    
    Optional Constraints:
    - Tolerance: Less than or equal (<=)
    - Dielectric Material / Temperature Coefficient: Equal (=)
    - Operating Temperature (Minimum): Less than or equal (<=)
    - Operating Temperature (Maximum): Greater than or equal (>=)
    """
    
    def __init__(self, name, manufacturer, capacitance, rated_voltage, partnumber, case_code=None, dimensions=None, 
                 tolerance=None, dielectric_material=None, temp_coefficient=None, 
                 min_operating_temp=None, max_operating_temp=None, technology=None):
        super().__init__(name, manufacturer, partnumber )
        self.category = "Capacitor"
        self.technology = technology
        
        # Core constraints
        self.capacitance = capacitance
        self.rated_voltage = rated_voltage
        self.case_code = case_code
        self.dimensions = dimensions  # (Height, Length, Width)
        self.partnumber = partnumber
        
        # Optional constraints
        self.tolerance = tolerance
        self.dielectric_material = dielectric_material
        self.temp_coefficient = temp_coefficient
        self.min_operating_temp = min_operating_temp
        self.max_operating_temp = max_operating_temp


class Inductor(Component):
    """
    Inductor component class.
    
    Core Constraints:
    - Inductance: Equal (=)
    - Rated Current: Greater than or equal (>=)
    - Case Code or Dimensions: Equal (=)
    
    Optional Constraints:
    - Shielding: Equal (=)
    - DC Resistance: Less than or equal (<=)
    - Tolerance: Less than or equal (<=)
    - Operating Temperature (Minimum): Less than or equal (<=)
    - Operating Temperature (Maximum): Greater than or equal (>=)
    - Self-Resonant Frequency: Greater than or equal (>=)
    """
    
    def __init__(self, name, manufacturer, partnumber, inductance, rated_current, case_code=None, dimensions=None,
                 shielding=None, dc_resistance=None, tolerance=None,
                 min_operating_temp=None, max_operating_temp=None, self_resonant_freq=None, technology=None):
        super().__init__(name, manufacturer, partnumber)
        self.category = "Inductor"
        self.technology = technology
        
        # Core constraints
        self.inductance = inductance
        self.rated_current = rated_current
        self.case_code = case_code
        self.dimensions = dimensions  # (Height, Length, Width)
        self.partnumber = partnumber
        
        # Optional constraints
        self.shielding = shielding
        self.dc_resistance = dc_resistance
        self.tolerance = tolerance
        self.min_operating_temp = min_operating_temp
        self.max_operating_temp = max_operating_temp
        self.self_resonant_freq = self_resonant_freq


class Resistor(Component):
    """
    Resistor component class.
    
    Core Constraints:
    - Resistance: Equal (=)
    - Power Rating: Greater than or equal (>=)
    - Case Code or Dimensions: Equal (=)
    
    Optional Constraints:
    - Tolerance: Less than or equal (<=)
    - Temperature Coefficient: Equal (=)
    - Operating Temperature (Minimum): Less than or equal (<=)
    - Operating Temperature (Maximum): Greater than or equal (>=)
    """
    
    def __init__(self, name, manufacturer, partnumber, resistance, power_rating, case_code=None, dimensions=None,
                 tolerance=None, temp_coefficient=None, min_operating_temp=None, max_operating_temp=None, technology=None):
        super().__init__(name, manufacturer, partnumber)
        self.category = "Resistor"
        self.technology = technology
        
        # Core constraints
        self.resistance = resistance
        self.power_rating = power_rating
        self.case_code = case_code
        self.dimensions = dimensions  # (Height, Length, Width)
        self.partnumber = partnumber
        
        # Optional constraints
        self.tolerance = tolerance
        self.temp_coefficient = temp_coefficient
        self.min_operating_temp = min_operating_temp
        self.max_operating_temp = max_operating_temp

