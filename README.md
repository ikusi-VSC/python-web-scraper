Python Web Scraper

A lightweight multi-page web scraper built with Python, Requests, BeautifulSoup, and pandas.

This project demonstrates a practical scraping workflow: requesting web pages, validating responses, parsing structured HTML with CSS selectors, handling pagination, resolving relative URLs, tolerating missing fields, and collecting the final results into a pandas DataFrame.

Features

- HTTP requests with retry handling
- Handles common request failures:
  - Timeout
  - Connection errors
  - HTTP errors
  - Other Requests exceptions
- Basic response validation through HTTP status and Content-Type
- HTML parsing with BeautifulSoup
- CSS selector based data extraction
- Graceful handling of missing HTML elements
- Multi-page pagination
- Relative URL resolution with "urljoin"
- Support for HTML "<base>" URLs
- Fallback pagination discovery when the primary next-page request fails
- Final data aggregation with pandas

Data Collected

The scraper extracts the following fields from each product:

Field| Description
"product"| Product name
"price"| Product price
"category"| Product category
"id"| Product data ID
"rating"| Product rating
"url"| Absolute product detail URL
"reviews"| Review information

Missing fields are represented as "None" rather than causing the entire page to fail.

Project Structure

python-web-scraper/
├── web_scraper.py
└── README.md

Requirements

- Python 3.9+
- requests
- beautifulsoup4
- pandas

Install the dependencies with:

pip install requests beautifulsoup4 pandas

Usage

The current version is configured to run against a local HTML test site:

http://127.0.0.1:8000/page1.html

Start a local HTTP server containing the test pages:

python -m http.server 8000

Then run:

python web_scraper.py

The scraper follows pagination links, collects the product records from each page, and outputs the final pandas DataFrame.

Pagination Handling

The scraper first attempts to follow the page's primary ".next" link.

If that request fails after retries, it falls back to other pagination links (such as "a.page") and attempts to continue from an available page.

This provides basic fault tolerance without introducing a browser automation framework or a complex scraping infrastructure.

URL Handling

Relative links are converted to absolute URLs with "urljoin".

The helper also checks for an HTML "<base href="...">" element before resolving relative paths. This allows the scraper to work with pages whose base URL differs from the current request URL.

Scope

This project focuses on the fundamentals of reliable HTML scraping and data collection.

It does not attempt to implement advanced anti-bot bypassing, proxy rotation, CAPTCHA solving, or browser automation. The goal is to demonstrate clean request handling, structured HTML extraction, pagination, and data processing.

Example Output

A successful run against the test scenario produces a pandas DataFrame containing six product records and seven columns.

License

This project is provided for portfolio and learning purposes.
