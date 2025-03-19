from argparse import ArgumentParser

from op25formatter import Op25Formatter
from systemscraper import SystemScraper

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--url", help="Radio Reference URL", required=True)
    parser.add_argument("--outdir", help="Name of out directory")
    parser.add_argument("--format", help="Data format")
    args = parser.parse_args()

    if "/sid" in args.url:
        scraper = SystemScraper(args.url, args.outdir)
        scraper.scrape()
        if args.format == "op25":
            Op25Formatter(scraper.outdir).format()
    else:
        raise ValueError("Can't scrape this URL")
