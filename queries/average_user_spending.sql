-- Get the average spending for a region for users mimicing a specific candidate.
-- Example Input: Region ID: 5, Candidate ID: 1

SELECT avg(spending) AS average_spending 
FROM mimics
INNER JOIN 
spendings
ON spendings.user_id = mimics.user_id
WHERE mimics.mimics = 1
AND spendings.region_id = 5;

