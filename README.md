# N-400 Dynamic Data API

This repository maintains a static API for N-400 dynamic data (political figures, representatives, etc.) using GitHub Pages.

## Structure

```
/api/v1/
  dynamic_data.json     # Federal officials (President, VP, etc.)
  states_data.json      # State-specific information
  zip_data_index.json   # Index of ZIP code data files
  zip_data_*.json       # ZIP code to representative mapping (by state)
  version.json         # Current version information
```

## Setup

1. Create a new repository
2. Clone the repository:
```bash
git clone https://github.com/your-username/n400-dynamic-data.git
cd n400-dynamic-data
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Enable GitHub Pages:
   - Go to repository Settings
   - Navigate to Pages section
   - Select 'gh-pages' branch
   - Save

## Usage

### Accessing the API

Base URL: `https://your-username.github.io/n400-dynamic-data/api/v1/`

Example endpoints:
- `dynamic_data.json` - Current political figures
- `states_data.json` - State information
- `zip_data_index.json` - ZIP code data index
- `zip_data_ca.json` - California ZIP code data

### Local Development

1. Run update script:
```bash
python scripts/main.py
```

2. Check generated files in `/api/v1/` directory

### Automatic Updates

The data is automatically updated daily via GitHub Actions. You can also trigger manual updates:
1. Go to Actions tab
2. Select "Update Political Data"
3. Click "Run workflow"

## Data Sources

The script collects data from:
- congress.gov
- house.gov
- senate.gov
- Official state websites

## File Formats

### dynamic_data.json
```json
{
  "federal": {
    "president": {
      "name": "Joe Biden",
      "title": "President of the United States",
      "party": "Democratic",
      "term_start": "2021",
      "term_end": "2025"
    },
    ...
  },
  "congress": {
    "house": {
      "total_seats": 435,
      ...
    },
    ...
  }
}
```

### states_data.json
```json
{
  "states": {
    "CA": {
      "name": "California",
      "capital": "Sacramento",
      "senators": ["...", "..."],
      "representatives": 52
    },
    ...
  }
}
```

### zip_data_*.json
```json
{
  "state": "CA",
  "zip_codes": {
    "90210": {
      "state": "CA",
      "district": "28",
      "representative": "..."
    },
    ...
  }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a Pull Request

## License

MIT License
