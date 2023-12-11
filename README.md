SOURCE
===
https://www.reddit.com/r/StarVStheForcesofEvil/comments/clnrdv/link_compendium_of_questions_and_answers_from_the/?

PLAN
===
Compile Q&As from the source
Store Q&As into database format using either sqlite3 or sqlalchemy module
Transform database data into a format usable by TeX
Write TeX document that displays the data
Create separate output files for each interviewee

TABLES
===
(All of these are strings, more or less.)
interviewee
- primary_key := interviewee_name

question_and_answer
- foreign_key := interviewee_name
- primary_key := interviewer_name
- field1 := question
- field2 := answer
- field3 := url
