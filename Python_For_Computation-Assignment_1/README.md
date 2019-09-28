Python For Computation - Coursework

Assignment Instructions:

Answer all of the following questions:

Question 1 – Anagram (Total 15 Marks)

You need to create a function that accepts two variables (A, B). A and B are called anagrams
if they contain all same characters in the same frequencies. For example, the anagrams of
DOG are DOG, ODG, GOD, DGO, OGD and GDO. If A and B are anagrams the function will print
“Anagrams” otherwise, print “Not anagrams” instead.
Constraints: The comparison should NOT be case sensitive.

Question 2 – Credit Card (Total 15 Marks)

You are working in a bank and part of your job is to develop tools to facilitate your colleagues’
job. John your co-worker is working in the credit card department and he received an N
number of credit cards number that needs to be validated against certain criteria. Your task
is to develop a function to run through these credit cards numbers and print ALL at once, list
of the credit cards with validation status. (Hint: you can use regular expressions)
Constraints: The input may be in a nested list or list

Input:
[378282246310005, 30569309025904, 6011111111111117, 5123-2332-3232-3213]
OR
[378282246310005, [30569309025904, 6011111111111117], 5123-2332-3232-3213]

Example of the output:
378282246310005 Invalid
30569309025904 Invalid
6011111111111117 Invalid
5123-2332-3232-3213 valid

The criteria are:
• It must start with a 4,5 or 6
• It must be exactly 16 digits
• It must be numbers only
• It can have a digits in groups of 4, separated by one hyphen “-“
• It should not contain any other characters.
• It should not contain “four” repeated numbers

Question 3 – Twitter collection and SQL (Total 15 Marks)

You need to build a Python script capable of collecting data from Twitter's Stream API for a
given keyword, that then stores this data in an SQLite database. Alongside this, you should
apply analyse the sentiment of the tweet text and store the output with the tweet data. When
storing each tweet, include the following:

• Tweet ID
• Tweet Text
• Created at
• Location
• Geo coordinates
• Number of followers for the user
• Number of friends.
• Sentiment Analysis

Test your code against the keyword (Trump)
The dataset should be at least 10,000 tweets.

Question 4 – Data structure and algorithms (Total 15 Marks)

Using the dataset collected from Question 3:

• Create a Python script to export the data from SQLite to CSV file.
• Create a Python script to read and generate the following from the data:
o A map showing the frequency of tweets by location (optional)
o A map showing the number of positive and negative tweets by location
(optional)
o Graph of the frequency of the tweet over time
o Graph of the positive and negative tweets overtime.

Note:
• Your script should be able to save the file to folder as image.
• You will need to use matplotlib