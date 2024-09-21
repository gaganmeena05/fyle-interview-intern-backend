SELECT student_id, count(*)
FROM assignments
WHERE state IS 'GRADED'
GROUP BY student_id