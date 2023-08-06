import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FiltersWrapper from './components/FiltersWrapper';
import ResultsWrapper from './components/ResultsWrapper';
import TranslationsWrapper from '../TranslationsContext';
import queryString from 'query-string';
import moment from 'moment';

import './App.less';

const App = () => {
  const [isFetching, setFetching] = useState(false);
  const [formParameters, setFormParameters] = useState([]);
  const [queryParameters, setQueryParameters] = useState({
    b_start: 0,
    b_size: 20,
  });

  const portalUrl = document.body
    ? document.body.getAttribute('data-portal-url') || ''
    : '';
  useEffect(() => {
    setFetching(true);
    axios({
      method: 'GET',
      headers: {
        'content-type': 'application/json',
        Accept: 'application/json',
      },
      url: `${portalUrl}/@search_comunicati_parameters`,
    }).then(({ status, statusText, data }) => {
      if (status !== 200) {
        console.error(statusText);
      } else {
        setFormParameters(data);
        setFetching(false);
        initializeQueryParameters(data);
      }
    });
  }, []);

  const initializeQueryParameters = parameters => {
    const queryString = new URLSearchParams(window.location.search);
    const newParameters = parameters.reduce((accumulator, parameter) => {
      switch (parameter.type) {
        case 'text':
          accumulator[parameter.id] = queryString.get(parameter.id) || '';
          break;
        case 'date':
          const parameterId = parameter.id;

          accumulator[parameter.id] = {};
          const [from, to] = queryString.getAll(`${parameterId}.query`);
          if (from) {
            accumulator[parameterId] = {
              from: moment(from),
              to: to && moment(to),
            };
          }
          break;
        default:
          if (!queryString.get(parameter.id)) {
            //  empty querystring
            if (parameter.default) {
              accumulator[parameter.id] = parameter.default;
            } else {
              accumulator[parameter.id] = [];
            }
          } else {
            accumulator[parameter.id] = queryString.getAll(parameter.id);
          }
          break;
      }

      return accumulator;
    }, {});
    setQueryParameters({ ...queryParameters, ...newParameters });
  };

  const updateQueryParameters = parameter => {
    const newQueryParameters = { ...queryParameters, ...parameter };
    setQueryParameters(newQueryParameters);

    // convert date field into a qs-like one
    const qsParameters = { ...newQueryParameters };
    if (qsParameters.created) {
      const { from, to } = qsParameters.created;
      if (from) {
        if (to) {
          qsParameters['created.query'] = [
            from.format('YYYY-MM-DD 00:00:00'),
            to.format('YYYY-MM-DD 23:59:59'),
          ];
          qsParameters['created.range'] = 'min:max';
        } else {
          qsParameters['created.query'] = from.format('YYYY-MM-DD 00:00:00');
          qsParameters['created.range'] = 'min';
        }
      }
      delete qsParameters.created;
    }
    history.pushState(
      { id: 'comunicati-search' },
      'Comunicati Search',
      `${portalUrl}/comunicati-search?${queryString.stringify(qsParameters)}`,
    );
  };

  const resetQueryParameters = () => {
    const newQueryParameters = { b_start: 0, b_size: 20 };
    setQueryParameters(newQueryParameters);
    history.pushState(
      { id: 'comunicati-search' },
      'Comunicati Search',
      `${portalUrl}/comunicati-search`,
    );
  };

  return (
    <TranslationsWrapper>
      <FiltersWrapper
        updateQueryParameters={updateQueryParameters}
        resetQueryParameters={resetQueryParameters}
        formParameters={formParameters}
        queryParameters={queryParameters}
        isFetching={isFetching}
      ></FiltersWrapper>
      <ResultsWrapper
        queryParameters={queryParameters}
        updateQueryParameters={updateQueryParameters}
      ></ResultsWrapper>
    </TranslationsWrapper>
  );
};
export default App;
