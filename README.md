# Web Scraper (V1) 💀

## Overview
![image](https://github.com/user-attachments/assets/2c1e9f7d-4fa3-4192-89cc-5f732fb59175)

This project is a **powerful web scraper** built using Python. It is designed to efficiently extract metadata, download images, fetch links, and store the collected data in both CSV and JSON formats for further use. Additionally, the scraper features a **Tkinter-based GUI** that provides a user-friendly interface, making it accessible to both developers and non-programmers. With support for multithreading, the tool ensures high performance and quick data processing even on websites with a large number of links and images.

---

## Features

- **Extracts Metadata:**  
  Retrieves key information from webpages, including the page title, meta descriptions, keywords, OpenGraph tags, and Twitter metadata. This functionality is essential for tasks like SEO analysis, content research, and competitive analysis.

- **Downloads Images:**  
  Automatically downloads all images found on the target website. The images are stored in structured folders based on the site name, ensuring clarity and easy access. Duplicate images are avoided to optimize storage and reduce redundant data.

- **Fetches All Links:**  
  Extracts all hyperlinks present on a webpage and processes each link to gather additional metadata. This enables users to perform a comprehensive site crawl and data extraction from multiple pages.

- **Saves Data in CSV and JSON:**  
  The scraped data is stored in both CSV and JSON formats inside a structured directory (`SITE/{site_name}`). This dual-format output facilitates seamless integration with various data analysis tools and workflows.

- **Multithreading for High Performance:**  
  Leveraging Python’s multithreading capabilities, the scraper can process multiple links and download images concurrently. This significantly reduces the total execution time, making it ideal for large-scale web scraping tasks.

- **GUI Interface:**  
  A modern, aesthetically pleasing Tkinter-based graphical user interface allows users to enter the URL, initiate the scraping process, and view real-time log updates. The built-in console log displays progress updates, errors, and other important messages, enhancing the user experience.

- **Error Handling and Logging:**  
  The scraper is equipped with comprehensive error handling using custom logging functions that display messages in different colors based on the type of notification (e.g., errors, warnings, progress updates). This makes troubleshooting easier and improves overall usability.

---

## Functions Explained

The project is structured into two main components: **scraper_functions.py** (which contains all the backend scraping logic) and **main.py** (which builds the GUI and manages user interaction). Below is a detailed breakdown of the functions included in the project:

| **Function**                                                                   | **Description**                                                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `get_page_info(url)`                                                           | **Purpose:** Extracts metadata from a given webpage. <br> **Details:** Sends an HTTP request to the URL and parses the returned HTML using BeautifulSoup. Retrieves the page title and meta tags such as description, keywords, OpenGraph, and Twitter data. |
| `sanitize_filename(filename)`                                                  | **Purpose:** Ensures file names are safe for use on any operating system. <br> **Details:** Removes any invalid characters (e.g., `<>:"/\\|?*`) from file names to avoid issues during file creation or saving.                                     |
| `download_images(url, folder_name, downloaded_images, log_func)`               | **Purpose:** Downloads images from a webpage. <br> **Details:** Retrieves all `<img>` tags from the page, constructs absolute URLs for relative paths, and downloads each image if not already downloaded. Images are stored in a dedicated media folder.     |
| `save_to_csv(data, site_name)`                                                 | **Purpose:** Saves the scraped data in CSV format. <br> **Details:** Organizes data into rows and writes it into a CSV file under the directory `SITE/{site_name}`, making the data easily accessible for further analysis or reporting.             |
| `save_to_json(data, site_name)`                                                | **Purpose:** Saves the scraped data in JSON format. <br> **Details:** Dumps the data into a JSON file with proper indentation and formatting, stored under `SITE/{site_name}`. This is useful for integrations with other applications or APIs.     |
| `fetch_links(url, log_func, scraped_data, folder_name, downloaded_images)`       | **Purpose:** Extracts and processes all hyperlinks from a webpage. <br> **Details:** Uses BeautifulSoup to locate all `<a>` tags, extracts the `href` attribute, and then uses multithreading (via ThreadPoolExecutor) to process each link concurrently.  |
| `process_link(full_url, log_func, scraped_data)`                               | **Purpose:** Processes a single hyperlink. <br> **Details:** For each link, it calls `get_page_info` to retrieve metadata and logs the progress. The scraped information is then appended to the aggregated data list for later storage.                |
| `scrape_website(url, log_func)`                                                | **Purpose:** Main orchestrator of the scraping process. <br> **Details:** Determines the site name from the URL, initializes data structures (for storing images and scraped data), calls functions to fetch links and download images, and finally saves the data. |
| `log_func(message, color)`                                                     | **Purpose:** Provides custom logging with colored output. <br> **Details:** Displays messages to the console with specific colors to denote different types of messages (e.g., errors in red, success in green), enhancing readability during runtime.    |

---

## GUI Interface

The GUI component (defined in **main.py**) provides a graphical layer over the scraping functions, featuring:

- **Input Field:**  
  A text entry widget where users can input the URL of the website they wish to scrape.

- **Start Button:**  
  Initiates the scraping process. When clicked, it disables the input field and start button to prevent multiple concurrent operations and changes the button text to indicate that scraping is in progress.

- **Stop Button:**  
  Provides the ability to gracefully halt the scraping process. Once clicked, it attempts to join the scraping thread and resets the interface.

- **Console Log:**  
  A scrolling text widget that displays real-time logs including information about fetched links, downloaded images, progress updates, and any error messages encountered during the scraping process.

- **Close Program Button:**  
  Allows the user to exit the application gracefully.

The GUI is built using Tkinter and is enhanced with custom themes and styling from the `ttkthemes` package, making the user interface both modern and responsive.

---

## Usage & Applications

This web scraper can be used in various scenarios, including:

- **SEO Analysis:**  
  Extract metadata from websites to evaluate their SEO structure and performance. This is particularly useful for digital marketers and SEO specialists.

- **Web Archiving:**  
  Save website content and structure in a persistent format (CSV/JSON) for archival or offline browsing purposes.

- **Research & Data Collection:**  
  Collect data from multiple websites for academic research, market analysis, or competitive intelligence. The structured output can be directly imported into data analysis tools.

- **Image Scraping:**  
  Automatically download images from websites for content creation, analysis, or reuse. The scraper ensures that images are organized and duplicates are avoided.

- **Automated Data Extraction:**  
  Use the tool as a backend component in larger automation workflows, integrating with other systems via its CSV/JSON outputs.

---

## How to Run

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/BOSS294/Web-Scrapper.git
   cd Web-Scrapper
   ```

2. **Install Dependencies:**

   Ensure you have Python 3 installed. Then, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Scraper:**

   Launch the application by running the main Python file:

   ```bash
   python main.py
   ```

   The GUI window will appear, allowing you to input a URL and start scraping.

---

## Technology Stack

- **Python 3:** The core programming language used for scripting and application logic.
- **Tkinter:** For creating the GUI interface.
- **BeautifulSoup & Requests:** For web scraping and HTML parsing.
- **Selenium & WebDriver Manager:** For handling dynamic web content (if needed).
- **ThreadPoolExecutor:** For concurrent processing of multiple links.
- **CSV & JSON Modules:** For structured data storage.
- **ttkthemes:** For enhancing the look and feel of the Tkinter GUI.

---

## Future Roadmap

- **Enhanced Error Handling:**  
  Implement more robust error and exception management to handle various edge cases (e.g., network failures, unexpected HTML structures).

- **Progress Indicators:**  
  Add progress bars and visual indicators within the GUI to display real-time scraping progress.

- **Customization Options:**  
  Allow users to customize output directories, file naming conventions, and select specific types of data to scrape.

- **Support for JavaScript-Heavy Sites:**  
  Further integrate Selenium or headless browsers to scrape sites that rely heavily on JavaScript for content loading.

- **Automated Scheduling:**  
  Enable scheduled scraping tasks that can run at predefined intervals.

- **User Authentication:**  
  Incorporate options to scrape data from websites that require user authentication.

---

## Contributing

Contributions are welcome! If you have suggestions, improvements, or bug fixes, please feel free to fork the repository and submit a pull request. Here’s how you can contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch.
4. Open a pull request describing your changes.

For any major changes, please open an issue first to discuss what you would like to change.

---

## Author

👨‍💻 **Made By:** Mayank Chawdhari

Feel free to reach out if you have any questions or need further assistance with the project.

---

