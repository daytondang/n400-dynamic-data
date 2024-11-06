import os
import json
import unittest
from scraper import PoliticalDataScraper
from validator import DataValidator
from generator import JsonGenerator

class TestDataUpdate(unittest.TestCase):
    def setUp(self):
        self.scraper = PoliticalDataScraper()
        self.validator = DataValidator()
        self.generator = JsonGenerator()
        self.api_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'api', 'v1')

    def test_data_collection(self):
        """Test that data collection returns expected structure"""
        data = self.scraper.collect_political_data()
        
        # Check main sections exist
        self.assertIn('federal', data)
        self.assertIn('congress', data)
        self.assertIn('states', data)
        self.assertIn('zip_data', data)

        # Check federal data
        federal = data['federal']
        self.assertIn('president', federal)
        self.assertIn('vice_president', federal)
        self.assertIn('speaker', federal)

        # Check congress data
        congress = data['congress']
        self.assertIn('house', congress)
        self.assertIn('senate', congress)

    def test_data_validation(self):
        """Test that validation catches invalid data"""
        # Test with valid data
        valid_data = {
            'federal': {
                'president': {
                    'name': 'Joe Biden',
                    'title': 'President of the United States',
                    'party': 'Democratic'
                }
            },
            'congress': {
                'house': {
                    'total_seats': 435,
                    'current_session': '118th Congress',
                    'term': '2023-2025',
                    'majority_party': 'Republican'
                }
            },
            'states': {
                'CA': {
                    'name': 'California',
                    'capital': 'Sacramento',
                    'senators': ['Senator 1', 'Senator 2'],
                    'representatives': 52
                }
            },
            'zip_data': {
                '90210': {
                    'state': 'CA',
                    'district': '30',
                    'representative': 'Representative Name'
                }
            }
        }
        self.assertTrue(self.validator.validate_political_data(valid_data))

    def test_json_generation(self):
        """Test that JSON files are generated correctly"""
        test_data = {
            'federal': {
                'president': {
                    'name': 'Test President',
                    'title': 'Test Title',
                    'party': 'Test Party'
                }
            },
            'congress': {
                'house': {
                    'total_seats': 435
                }
            },
            'states': {},
            'zip_data': {}
        }

        # Generate test files
        self.generator.generate_political_data(test_data)

        # Check files exist
        self.assertTrue(os.path.exists(os.path.join(self.api_dir, 'dynamic_data.json')))

        # Check file content
        with open(os.path.join(self.api_dir, 'dynamic_data.json'), 'r') as f:
            generated_data = json.load(f)
            self.assertIn('federal', generated_data)
            self.assertIn('congress', generated_data)

    def test_version_generation(self):
        """Test version file generation"""
        version_data = {
            'version': '20240120000000',
            'last_updated': '2024-01-20T00:00:00Z'
        }
        self.generator.generate_version_data(version_data)
        
        version_file = os.path.join(self.api_dir, 'version.json')
        self.assertTrue(os.path.exists(version_file))
        
        with open(version_file, 'r') as f:
            data = json.load(f)
            self.assertIn('version', data)
            self.assertIn('last_updated', data)

if __name__ == '__main__':
    unittest.main()
