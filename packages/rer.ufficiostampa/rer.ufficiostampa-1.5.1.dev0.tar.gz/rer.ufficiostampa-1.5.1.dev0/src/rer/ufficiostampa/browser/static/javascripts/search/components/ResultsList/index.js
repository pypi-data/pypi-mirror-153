import React, { useContext } from 'react';
import { shape, object, func, array, string, bool, number } from 'prop-types';
import ResultItem from '../ResultItem';
import PaginationContainer from '../PaginationContainer';
import { TranslationsContext } from '../../../TranslationsContext';

const ResultsList = ({ queryParameters, results, updatedPagination }) => {
  const getTranslationFor = useContext(TranslationsContext);
  const { error, message, items_total, items } = results;
  if (error) {
    return <p className="discreet">{message}</p>;
  }
  const resultLabel =
    items_total === 1 ? 'results_tot_label' : 'results_tot_label_multi';
  return (
    <React.Fragment>
      <div className="results-total">
        <h2 id="search-results">
          {getTranslationFor(resultLabel, '', items_total || 0)}
        </h2>
      </div>
      {items ? (
        <div className="results-wrapper">
          {items.map(data => (
            <ResultItem data={data} key={data['UID']} />
          ))}
          <PaginationContainer
            pageSize={queryParameters.b_size}
            currentPage={
              queryParameters.b_start === 0
                ? 0
                : queryParameters.b_start / queryParameters.b_size
            }
            totalResults={items_total}
            updateQueryParameters={updatedPagination}
          />
        </div>
      ) : (
        ''
      )}
    </React.Fragment>
  );
};
ResultsList.propTypes = {
  queryParameters: object,
  results: shape({
    error: bool,
    message: string,
    items_total: number,
    items: array,
  }),
  updatedPagination: func,
};

export default ResultsList;
