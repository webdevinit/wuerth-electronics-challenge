from typing import List, Dict, Any, Union
import json

class Component:
    def __init__(self, attributes: Dict[str, Any]):
        self.attributes = attributes

    def get(self, key):
        if isinstance(key, list):
            return [self.attributes.get(k) for k in key]
        return self.attributes.get(key)
    
    def __repr__(self):
        return f"<Component {self.attributes.get('Order_Code')}>"

    def print_attributes(self):
        print("Component attributes:", self.attributes)


class MatchingRule:
    def __init__(self, rule_key: str, attribute_key: Union[str, List[str]], operator_str: str, optional: bool = False):
        self.rule_key = rule_key
        self.attribute_key = attribute_key
        self.operator_str = operator_str
        self.optional = optional

    def score(self, candidate: Component, reference: Component) -> float:
        def extract(attr):
            return candidate.get(attr), reference.get(attr)

        # Composite dimensions: average individual dimension scores
        if isinstance(self.attribute_key, list):
            scores = []
            for attr in self.attribute_key:
                c_val, r_val = extract(attr)
                if c_val is None or r_val is None:
                    scores.append(0.0)
                    continue
                if isinstance(c_val, (int, float)) and isinstance(r_val, (int, float)):
                    score = 1 - abs(c_val - r_val) / max(abs(r_val), 1)
                    scores.append(max(0.0, min(score, 1.0)))
                else:
                    scores.append(0.0)
            return sum(scores) / len(scores)

        # Scalar or special cases
        c_val, r_val = extract(self.attribute_key)
        if c_val is None or r_val is None:
            return 0.0 if not self.optional else 0.5  # boost for missing optional

        # --- Special handling for Operating Temperature min/max ---
        if isinstance(c_val, list) and isinstance(r_val, list):
            if "Minimum" in self.rule_key:
                c_val, r_val = c_val[0], r_val[0]
            elif "Maximum" in self.rule_key:
                c_val, r_val = c_val[1], r_val[1]
            else:
                # Compare entire range (fallback)
                c_min, c_max = c_val
                r_min, r_max = r_val
                if self.operator_str == ">=":
                    return 1.0 if c_max >= r_max else max(0.0, (c_max - r_max) / max(r_max, 1))
                elif self.operator_str == "<=":
                    return 1.0 if c_min <= r_min else max(0.0, (r_min - c_min) / max(r_min, 1))
                return 0.0

        # Handle non-numeric after fallback unwrap
        if not isinstance(c_val, (int, float)) or not isinstance(r_val, (int, float)):
            return 0.0

        # Numeric comparison
        try:
            if self.operator_str == "=":
                score = 1 - abs(c_val - r_val) / max(abs(r_val), 1)
                return max(0.0, min(score, 1.0))
            elif self.operator_str == ">=":
                return 1.0 if c_val >= r_val else max(0.0, c_val / max(r_val, 1))
            elif self.operator_str == "<=":
                return 1.0 if c_val <= r_val else max(0.0, r_val / max(c_val, 1))
        except:
            return 0.0

        return 0.0


    def __repr__(self):
        return f"<Rule {self.rule_key} {self.operator_str} on {self.attribute_key}>"

class MatchingRules:
    def __init__(self, rules_config: Dict, mapping_config: Dict):
        self.rules_config = rules_config
        self.mapping_config = mapping_config

    def get_rules_for(self, product_group: str, product_family: str) -> List[MatchingRule]:
        rules = []
        rule_def = self.rules_config.get(product_group)
        family_mapping = self.mapping_config.get(product_group, {}).get(product_family, {})
        if not rule_def or not family_mapping:
            return []

        for rule_key, operator_str in rule_def['core'].items():
            attr_key = family_mapping['core'].get(rule_key)
            if attr_key:
                rules.append(MatchingRule(rule_key, attr_key, operator_str, optional=False))

        for rule_key, operator_str in rule_def.get('optional', {}).items():
            attr_key = family_mapping['optional'].get(rule_key)
            if attr_key:
                rules.append(MatchingRule(rule_key, attr_key, operator_str, optional=True))

        return rules


class MatchingEngine:
    def __init__(self, rules: MatchingRules):
        self.rules = rules

    def match(self, source: Component, candidates: List[Component], top_k: int = 5) -> List[tuple]:
        group = source.get("Product_Group")
        family = source.get("Product_Family")
        rules = self.rules.get_rules_for(group, family)
        
        # Filter candidates by same Product_Family
        candidates = [c for c in candidates if c.get("Product_Family") == source.get("Product_Family")]

        print("⚙️  Applying rules:")
        for r in rules:
            print("   ", r)

        results = []
        for candidate in candidates:
            total_score = 0.0
            for rule in rules:
                s = rule.score(candidate, source)
                weight = 0.5 if rule.optional else 1.0
                total_score += s * weight
            final_score = total_score
            results.append((candidate, final_score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
with open("matchmaking/matching_rules.json", "r") as f:
    matching_rules = json.load(f)

with open("matchmaking/mappings.json", "r") as f:
    mappings = json.load(f)
    
with open("matchmaking/components.json", "r") as f:
    components = json.load(f)
    components = [Component(comp) for comp in components]
           
rules = MatchingRules(matching_rules, mappings)
engine = MatchingEngine(rules)

def match_wuerth_components(source: Dict[str, Any], top_k: int = 5) -> List[tuple]:
    
    if source.get("Product_Group") not in mappings.keys():
        raise ValueError(f"Product group {source.get('Product_Group')} not found in mappings.")
    
    if source.get("Product_Family") not in mappings[source.get("Product_Group")].keys():
        raise ValueError(f"Product family {source.get('Product_Family')} not found in mappings for group {source.get('Product_Group')}.")
    
    component = Component(source)
    
    matches = engine.match(component, components, top_k=top_k)
    return matches