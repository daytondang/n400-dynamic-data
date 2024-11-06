from typing import Dict, Any, List
import re

class DataValidator:
    def __init__(self):
        self.required_federal_fields = ['president', 'vice_president', 'speaker']
        self.required_congress_fields = ['house', 'senate']
        self.required_state_fields = ['name', 'capital', 'senators', 'representatives']
        self.required_zip_fields = ['state', 'district', 'representative']

    def validate_political_data(self, data: Dict[str, Any]) -> bool:
        """
        Validates the complete political data structure
        Returns True if valid, False otherwise
        """
        try:
            # Check main structure
            required_sections = ['federal', 'congress', 'states', 'zip_data']
            for section in required_sections:
                if section not in data:
                    print(f"Missing required section: {section}")
                    return False

            # Validate each section
            validations = [
                self._validate_federal_data(data['federal']),
                self._validate_congress_data(data['congress']),
                self._validate_states_data(data['states']),
                self._validate_zip_data(data['zip_data'])
            ]

            return all(validations)

        except Exception as e:
            print(f"Validation error: {str(e)}")
            return False

    def _validate_federal_data(self, data: Dict[str, Any]) -> bool:
        """
        Validates federal government data
        """
        for position in self.required_federal_fields:
            if position not in data:
                print(f"Missing federal position: {position}")
                return False
            
            position_data = data[position]
            if not isinstance(position_data, dict):
                print(f"Invalid data type for {position}")
                return False
            
            required_fields = ['name', 'title', 'party']
            for field in required_fields:
                if field not in position_data:
                    print(f"Missing field {field} in {position}")
                    return False
                
                if not isinstance(position_data[field], str):
                    print(f"Invalid type for {field} in {position}")
                    return False

        return True

    def _validate_congress_data(self, data: Dict[str, Any]) -> bool:
        """
        Validates Congress data
        """
        for chamber in self.required_congress_fields:
            if chamber not in data:
                print(f"Missing chamber: {chamber}")
                return False
            
            chamber_data = data[chamber]
            required_fields = ['total_seats', 'current_session', 'term', 'majority_party']
            
            for field in required_fields:
                if field not in chamber_data:
                    print(f"Missing field {field} in {chamber}")
                    return False

        return True

    def _validate_states_data(self, data: Dict[str, Any]) -> bool:
        """
        Validates state-specific data
        """
        if not data:
            print("States data is empty")
            return False

        for state_code, state_data in data.items():
            if not self._is_valid_state_code(state_code):
                print(f"Invalid state code: {state_code}")
                return False

            for field in self.required_state_fields:
                if field not in state_data:
                    print(f"Missing field {field} in state {state_code}")
                    return False

            # Validate senators list
            if not isinstance(state_data['senators'], list):
                print(f"Senators must be a list for state {state_code}")
                return False

            if len(state_data['senators']) != 2:
                print(f"Each state must have exactly 2 senators: {state_code}")
                return False

        return True

    def _validate_zip_data(self, data: Dict[str, Any]) -> bool:
        """
        Validates ZIP code mapping data
        """
        if not data:
            print("ZIP data is empty")
            return False

        for zip_code, zip_data in data.items():
            if not self._is_valid_zip(zip_code):
                print(f"Invalid ZIP code: {zip_code}")
                return False

            for field in self.required_zip_fields:
                if field not in zip_data:
                    print(f"Missing field {field} in ZIP {zip_code}")
                    return False

        return True

    def _is_valid_state_code(self, code: str) -> bool:
        """
        Validates state code format (2 uppercase letters)
        """
        return bool(re.match(r'^[A-Z]{2}$', code))

    def _is_valid_zip(self, zip_code: str) -> bool:
        """
        Validates ZIP code format (5 digits)
        """
        return bool(re.match(r'^\d{5}$', zip_code))
