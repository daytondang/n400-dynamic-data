import os
import json
from datetime import datetime
from scraper import PoliticalDataScraper
from validator import DataValidator
from generator import JsonGenerator
from git_handler import GitHandler

def main():
    print("Starting data update process...")
    
    # Initialize components
    scraper = PoliticalDataScraper()
    validator = DataValidator()
    generator = JsonGenerator()
    git_handler = GitHandler()

    try:
        # Collect data
        print("Collecting political data...")
        political_data = scraper.collect_political_data()
        
        # Validate data
        print("Validating data...")
        if not validator.validate_political_data(political_data):
            raise ValueError("Data validation failed")

        # Generate JSON files
        print("Generating JSON files...")
        generator.generate_political_data(political_data)
        
        # Update version
        version_data = {
            "last_updated": datetime.utcnow().isoformat(),
            "version": datetime.utcnow().strftime("%Y%m%d%H%M"),
        }
        generator.generate_version_data(version_data)

        # Git operations
        if git_handler.has_changes():
            print("Changes detected, updating repository...")
            git_handler.commit_and_push()
            print("Repository updated successfully")
        else:
            print("No changes detected")

    except Exception as e:
        print(f"Error during update process: {str(e)}")
        raise

if __name__ == "__main__":
    main()
