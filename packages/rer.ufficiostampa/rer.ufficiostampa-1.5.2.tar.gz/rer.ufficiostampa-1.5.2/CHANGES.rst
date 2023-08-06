Changelog
=========


1.5.1 (2022-06-06)
------------------

- Pass query to export-csv endpoint to export only selected subscribers.
  [cekk]


1.5.0 (2022-03-10)
------------------

- Add versioning for Comunicato and Invito.
  [cekk]
- Add solrpush behavior for additional fields.
  [cekk]

1.4.0 (2022-01-20)
------------------

- New search endpoint for comunicati (@search-comunicati). This is needed because new rer.sitesearch overrides @search endpoint and always search on SOLR.
  [cekk]


1.3.0 (2022-01-20)
------------------

- Normalize title and description on save.
  [cekk]
- Add effective date in Comunicato view.
  [cekk]

1.2.2 (2021-11-04)
------------------

- Arguments field is now required.
  [cekk]


1.2.1 (2021-09-16)
------------------

- Cleanup subject string before send, to remove strange characters.
  [cekk]


1.2.0 (2021-09-02)
------------------

- Cleanup channels (remove duplicated ones).
  [cekk]
- Refactor how to perform queries (to handle also unicode problems).
  [cekk]
- Accessibilty fixes: modal focus trap + select keyboard events
  [nzambello]


1.1.0 (2021-08-05)
------------------

- Disallow add new items in *arguments* field.
  [cekk]
- Export in csv also title and number.
  [cekk]
- Correctly wrap search terms with "*'*" in it.
  [cekk]
- Customize social viewlets to fix title and description meta tags (and also add a light dependency with rer.agidtheme.base).
  [cekk]
- Add dependency to ftfy to better encode csv exports.
  [cekk]

1.0.1 (2021-07-09)
------------------

- Fix import for python2 and sort indexes.
  [cekk]


1.0.0 (2021-05-26)
------------------

- Initial release.
  [cekk]
