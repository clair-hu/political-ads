-- Get the total spending for a specific user.
-- Example Input: User_id: 1

SELECT SUM(spending) AS total
FROM spendings
WHERE user_id = 1
LIMIT 10;
