# Requirement

## Data Source

Baidu Baike(no less than 10000 entries) and Baidu Zhidao(no less than 10000 questions).  The number of entries or questions under each category in Baidu Baike or Baidu Zhidao should be similar.

For Baike, each entry includes title, subtitles, descriptions. [https://baike.baidu.com](https://baike.baidu.com)

For Zhidao, each question has different replies. [https://zhidao.baidu.com](https://zhidao.baidu.com)

## Supported queries

- Ask a **question** in the Baidu Zhidao, and the system should return a ranked list of all **similar questions(with their answers)**. If there are any **Baidu Baike entries** or **images** related to the question, return them.
- Ask a **keyword**, and the system should return a ranked list of **Baidu Baike entries** and **questions along with their answers in Zhidao**. If there are any related **images**, return them. 
-  Let user enter keyword for a **particular region**, e.g. search in the Baidu Baike, the question of Baidu Zhidao, the answer of Baidu Zhidao or the images.  

Notice: As each question in Baidu Zhidao has different answers, we should delete **unrelated answers** and recommend a ranked list of answers. (Hint: we can consider whether the answer is accepted by the question owner or the number of times the answer is considered useful).