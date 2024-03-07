-- (1) Top Selling Genres:
-- Query: Determine the top-selling genres based on the number of tracks sold.
-- Analysis: Identifies the most popular music genres among customers.

SELECT g.name AS genre,
       COUNT(il.track_id) AS track_count
FROM invoice_line il
INNER JOIN track t ON il.track_id = t.track_id
INNER JOIN genre g ON t.genre_id = g.genre_id
GROUP BY g.genre_id
ORDER BY track_count DESC
LIMIT 5;


-- (2) Customer Sales Distribution:
-- Query: Analyze the distribution of sales among customers.
-- Analysis: Identifies the top-spending customers and their contribution to total revenue.

SELECT c.first_name || ' ' || c.last_name AS customer_name,
       SUM(i.total) AS total_spent
FROM customer c
INNER JOIN invoice i ON c.customer_id = i.customer_id
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 10;


-- (3) Top Selling Tracks (using a Subquery):
-- Query: Identify the top-selling tracks based on the number of times they were purchased, along with their genres.
-- Analysis: This query will use a subquery to calculate the sales count for each track, and then join the track information including genre.

SELECT t.name AS track_name,
       g.name AS genre,
       sales_count
FROM (
    SELECT il.track_id, 
           COUNT(il.track_id) AS sales_count
    FROM invoice_line il
    GROUP BY il.track_id
    ORDER BY sales_count DESC
    LIMIT 10
) AS top_tracks
JOIN track t ON top_tracks.track_id = t.track_id
JOIN genre g ON t.genre_id = g.genre_id;


-- (4) Sales Trend Over Time:
-- Query: Analyze the trend of sales over different time periods (e.g., monthly, yearly).
-- Analysis: Helps identify seasonal trends and overall sales patterns.

SELECT strftime('%Y-%m', invoice_date) AS month,
       SUM(total) AS monthly_sales
FROM invoice
GROUP BY month
ORDER BY month;