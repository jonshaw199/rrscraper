
# RadioReference Scraper

A simple Python script to scrape data from radioreference.com and optionally export it for [OP25](https://github.com/boatbod/op25).

## Features

- Scrapes Radio Reference data for a given URL and exports the raw data in CSV format
  - ~Only supports systems for now (URLs with `/sid`)~
  - Now supports scraping county pages (URLs with `/ctid`) and agency pages (URLs with `/aid`) too
- Optionally formats and exports TSV data for use with [OP25](https://github.com/boatbod/op25)

## Requirements

- Python 3.x
- Pipenv (for managing dependencies)

To install the required dependencies with Pipenv, run:

```bash
pipenv install
```

Alternatively, if you don't use Pipenv, you can install dependencies with `pip` by using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Dependencies

- `bs4`: BeautifulSoup for parsing HTML.
- `requests`: HTTP requests library for fetching data.

## Usage

Run the script with the following arguments:

```bash
python scrape.py --url <Radio Reference URL> --out_dir <output directory> [--op25]
```

### Arguments

- `--url`: (Required) The URL of the Radio Reference system, county, or agency (e.g., `https://www.radioreference.com/db/sid/6253`).
- `--out_dir`: (Optional) Directory to save the scraped data. If not provided, a default directory will be used.
- `--op25`: (Optional) If specified, the data will be formatted for use with OP25.

### Example Usage

#### Scraping a Radio Reference System:

```bash
python scrape.py --url https://www.radioreference.com/db/sid/6253
```

This command will scrape the specified system from Radio Reference and save the data to the default output directory.

#### Scraping and Exporting for OP25:

```bash
python scrape.py --url https://www.radioreference.com/db/sid/6253 --op25
```

This command will scrape the specified system from Radio Reference and export the data in OP25 format.

#### Scraping a county:

```bash
python scrape.py --url https://www.radioreference.com/db/browse/ctid/211
```

#### Scraping an agency:

```bash
python scrape.py --url https://www.radioreference.com/db/aid/9210
```

## License

MIT License