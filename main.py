from argparse import ArgumentParser
from SystemScraper import SystemScraper

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--url", help="Radio Reference URL", required=True)
    parser.add_argument("--outdir", help="Name of out directory")
    args = parser.parse_args()

    if "/sid" in args.url:
        SystemScraper(args.url).scrape()
    else:
        raise ValueError("Can't scrape this URL")
