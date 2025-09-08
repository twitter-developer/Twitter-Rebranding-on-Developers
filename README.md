# Understanding the Effects of Twitter/X's Rebranding on Developers

This project collects and analyzes data from three social media platforms: **Twitter/X**, **Mastodon**, and **Bluesky**. The goal is to understand how Twitter/X's rebranding has affected developers' online behavior and communication patterns.  

The dataset includes anonymized CSV files located in the `data/` folder. These provide a small sample of the collected data. The full anonymized dataset will be released upon the acceptance of the associated research paper.  

## Project Structure

- `data/` - Contains anonymized CSV files
- `collect_data/` - Scripts for collecting social media data
- `code/` - Scripts used for data processing and analysis
- `README.md` - This file


`collect_data/`

- **Twitter.py**  
  - Fill in your token, username, and password in the script to access Twitter/X API.  

- **Mastodon.py** and **Bluesky.py**    
  - Fill in your token to access Mastodon API. 

- **Bluesky.py**  
  - Fill in your username, and password to access Bluesky API.
    
`code/`

Contains all scripts utilized in the paper for data processing, analysis, and visualization for **RQ1** and **RQ2**, as well as for mapping developers from Twitter/X to Mastodon and Bluesky for **RQ3**.

For **RQ3**, content similarity is performed using **CCFinderX**.  
- Refer to the [CCFinderX Tutorial](https://github.com/jbanaszczyk/CCFinderX/wiki/Tutorial-of-ccfx) for instructions on running the tool and analyzing content similarities.  

## How to Use

1. Navigate to the `collect_data/` folder.  
2. Update scripts with your API credentials (for Twitter/X).  
3. Modify the `keyword` parameters as needed for Mastodon and Bluesky.  
4. Run the scripts to collect data.  
5. Process and analyze data using the scripts in `code/`.  

---

This README provides a quick overview of the project structure and how to reproduce the data collection and analysis.
