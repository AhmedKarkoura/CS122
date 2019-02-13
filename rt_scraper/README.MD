# Rotten tomatoes scraper

The files are:  
  - util.py                   - Unchanged, copied from pa2  
  - create_movies_table.sql   - SQL statements to create all_movie_page table and import information  
  - rotten_tomatoes.db        - rotten tomatoes SQL database  
  - scrape_strategy.txt       - strategy to scrape rotten tomatoes  
  - scraper.py                - actual scraper and wrier for all_movies_page.csv  
  - all_movies_page.csv       - Information scraped from main movies page  
  
# Issues
  - Number of movies scraped doens't match?  
  
# Still to do
  - decide on actor/director scraping
  - Create and update movie_level_data table in rotten_tomatoes.db
  - merge tables appropriately in rotten_tomatoes.db
