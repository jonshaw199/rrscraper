
# RadioReference Scraper

A simple Python script to scrape data from radioreference.com and export it in various formats.

This does not crawl the site, it scrapes a single page like a trunked system (URL with `/sid`), county (URL with `/ctid`), or agency (URL with `/aid`). For scanning multiple systems, counties, or agencies simultaneously, you would need to merge the outputs of the script as necessary.

## Features

- Scrapes Radio Reference tables at a given URL and exports the raw data in CSV format
  - Can give it a trunked system URL (`/sid`), county URL (`/ctid`), or agency URL (`/aid`); see examples below
- Optionally formats CSV/TSV data for use with the following applications:
  - [OP25](https://github.com/boatbod/op25)
  - [Chirp Next](https://chirpmyradio.com/projects/chirp/wiki/ChirpNextBuild)
  - More will be added as needed; any and all contributions welcome

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
- `--op25`: (Optional) If specified, the data will be formatted for use with OP25 (only applicable to trunked systems: `/sid`)
- `--chirp`: (Optional) If specified, the data will be formatted for use with Chirp Next (only applicable to conventional systems: `/ctid`, `/aid`)

### Example Usage

#### Scraping a trunked system:

```bash
python scrape.py --url https://www.radioreference.com/db/sid/6253
```

This command will scrape the specified system from Radio Reference and save the data to the default output directory.

#### Scraping a trunked system and formatting for OP25:

```bash
python scrape.py --url https://www.radioreference.com/db/sid/6253 --op25
```

This command will scrape the specified system from Radio Reference and export the data in OP25 format.

#### Scraping a county:

```bash
python scrape.py --url https://www.radioreference.com/db/browse/ctid/211
```

#### Scraping a county and formatting for Chirp Next

```bash
python scrape.py --url https://www.radioreference.com/db/browse/ctid/211 --chirp
```

#### Scraping an agency:

```bash
python scrape.py --url https://www.radioreference.com/db/aid/9210
```

#### Scraping an agency and formatting for Chirp Next

```bash
python scrape.py --url https://www.radioreference.com/db/aid/9210 --chirp
```

## License

MIT License
