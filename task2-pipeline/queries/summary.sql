SELECT
  source_name,
  COUNT(*)                                         AS total_articles,
  ROUND(AVG(title_word_count), 1)                  AS avg_title_words,
  COUNTIF(has_description)                         AS articles_with_description,
  MIN(published_at)                                AS earliest_article,
  MAX(published_at)                                AS latest_article
FROM
  `tacheon-assessment.news_pipeline.articles_raw`
GROUP BY
  source_name
ORDER BY
  total_articles DESC
LIMIT 10;