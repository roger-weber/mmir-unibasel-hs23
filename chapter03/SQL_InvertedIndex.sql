-- 1. create schema for inverted index
--    document table can have additional attributes to title and year
--    creation of auto incremented doc IDs depends on database product
CREATE TABLE document(id SERIAL PRIMARY KEY, title TEXT, year INTEGER)
CREATE TABLE vocabulary(term TEXT PRIMARY KEY, df INTEGER, idf REAL)
CREATE TABLE posting(term TEXT, docId INTEGER, tf INTEGER)
CREATE TEMPORARY TABLE query(term TEXT, tf INTEGER)
CREATE INDEX inverted_list ON posting(term)

-- 2. rebuild index from documents
--    delete all existing data
DELETE FROM posting
DELETE FROM vocabulary
DELETE FROM document


-- 3. iterate over all documents in collection (outside of database)
--    fetch id after next insert (database dependent)
INSERT INTO document(title, year) VALUES (:title, :year)

--    for each document create a bag-of-word representation
INSERT INTO posting(term, docId, tf) VALUES(:term, :id, :tf)


-- 4. build vocabulary (table vocabulary)
--    fetch number of documents --> ndocs
SELECT count(*) AS count FROM document

--    insert terms from posting table into vocabulary table
INSERT INTO vocabulary(term, df, idf) 
      SELECT term, 
             count(*), 
             ln(1.0 * (:ndocs + 1) / (count(*) + 1)) 
        FROM posting 
    GROUP BY term


-- 5. boolean query with 2 terms
--    :term1 AND :term2
SELECT d.* 
  FROM document d, posting a, posting b 
 WHERE a.term = :term1 AND
       b.term = :term2 AND
       a.docId = b.docId AND
       a.docId = d.id

--    :term1 OR :term2
SELECT d.* 
  FROM document d, posting a 
 WHERE a.term IN ('star', 'wars') AND
       a.docId = d.id


-- 6. boolean query with arbitrary number of terms
--    add query terms to temporary table
DELETE FROM query
INSERT INTO query(term, tf) VALUES(:term, 1)

--    AND(:term1, :term2, ...)
  SELECT d.* 
    FROM document d, posting p, query q 
   WHERE p.term = q.term AND
         p.docId = d.id
GROUP BY p.docId
  HAVING COUNT(p.term) = (SELECT COUNT(*) FROM query)

--    OR(:term1, :term2, ...)
  SELECT d.* 
    FROM document d, posting p, query q 
   WHERE p.term = q.term AND
         p.docId = d.id
GROUP BY p.docId


-- 7. vector space model with dot product
--    add query terms to temporary table
DELETE FROM query
INSERT INTO query(term, tf) VALUES(:term,:tf)

--    calculate dot product and order by score
   SELECT SUM(p.tf * v.idf * q.tf * v.idf) AS score, d.*
     FROM document d, posting p, query q, vocabulary v
     WHERE p.term = q.term AND
         p.term = v.term AND
         p.docId = d.id
GROUP BY p.docId
ORDER BY 1 DESC


-- 8. adding predicates (example with vector space model)
--    add predicates on attributes in document table
  SELECT SUM(p.tf * v.idf * q.tf * v.idf) AS score, d.*
    FROM document d, posting p, query q, vocabulary v
   WHERE p.term = q.term AND
         p.term = v.term AND
         p.docId = d.id AND
         d.year > 1990
GROUP BY p.docId
ORDER BY 1 DESC