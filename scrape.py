import argparse

from conventionalscraper import ConventionalScraper
from op25formatter import Op25Formatter
from systemscraper import SystemScraper


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape radioreference.com and optionally export for OP25.",
        epilog="Example:\n  python scrape.py --url https://www.radioreference.com/db/sid/6253 --op25",
    )
    parser.add_argument("-u", "--url", help="Radio Reference URL", required=True)
    parser.add_argument("-o", "--out_dir", help="Name of output directory")
    parser.add_argument("--op25", help="Export for OP25", action="store_true")
    args = parser.parse_args()

    if "/sid" in args.url:
        print(f"Scraping {args.url}...")
        scraper = SystemScraper(args.url, args.out_dir)
        scraper.scrape()
        if args.op25:
            Op25Formatter(scraper.out_dir).format()
        print(f"Exported to {scraper.out_dir}")
    elif "ctid" in args.url:
        print(f"Scraping {args.url}...")
        scraper = ConventionalScraper(args.url, args.out_dir)
        scraper.scrape()
        print(f"Exported to {scraper.out_dir}")
    else:
        raise ValueError("Can't scrape this URL")
