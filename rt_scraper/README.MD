# Rotten tomatoes scraper

The files are:
  util.py                   - Unchanged, copied from pa2
  create_movies_table.sql   - SQL statements to create all_movie_page table and import information
  rotten_tomatoes.db        - rotten tomatoes SQL database
  scrape_strategy.txt       - strategy to scrape rotten tomatoes
  scraper.py                - actual scraper and wrier for all_movies_page.csv
  all_movies_page.csv       - Information scraped from main movies page
  
# Issues
  - Number of movies scraped doens't match?
  
# Still to do
  - use urls gained from main page scraping to scrape movie level data
  - decide on actor/director scraping
