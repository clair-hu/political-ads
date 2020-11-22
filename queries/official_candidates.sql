-- Returns the list of official candidates.

SELECT user_id, user_name
FROM users
WHERE is_official = true
LIMIT 10;

