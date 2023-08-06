import React, { useState, useEffect } from 'react';
import { array } from 'prop-types';

import apiFetch from './utils/apiFetch';

export const ApiContext = React.createContext({});

export const ApiProvider = ApiContext.Provider;
export const ApiConsumer = ApiContext.Consumer;

export const DEFAULT_B_SIZE = 25;
export const DEFAULT_SORT_ON = 'date';
export const DEFAULT_SORT_ORDER = 'descending';

function ApiWrapper({ endpoint, children }) {
  const [data, setData] = useState({});
  const [portalUrl, setPortalUrl] = useState(null);

  const [query, setQuery] = useState({});

  const [apiErrors, setApiErrors] = useState(null);
  const [loading, setLoading] = useState(false);
  const [b_size, setB_size] = useState(DEFAULT_B_SIZE);

  const [sort_on, setSort_on] = useState(DEFAULT_SORT_ON);
  const [sort_order, setSort_order] = useState(DEFAULT_SORT_ORDER);

  const handleApiResponse = res => {
    if (res && (res.status == 204 || res.status == 200)) {
      //ok
    } else {
      setApiErrors(
        res
          ? { status: res.status, statusText: res.statusText }
          : { status: '404', statusText: '' },
      );
    }
  };

  const fetchApi = (b_start = 0) => {
    if (portalUrl) {
      setLoading(true);
      apiFetch({
        url: portalUrl + '/@' + endpoint,
        params: {
          b_size,
          b_start,
          sort_on,
          sort_order,
          ...query,
          ...(query.text && query.text.length > 0
            ? { text: query.text + '*' }
            : {}),
        },
        method: 'GET',
      })
        .then(data => {
          if (data === undefined) {
            setApiErrors({ status: 500, statusText: 'Error' });
            setLoading(false);
            return;
          }
          handleApiResponse(data);
          setData(data.data);
          setLoading(false);
        })
        .catch(error => {
          setLoading(false);
          setApiErrors(
            error
              ? { status: error.status, statusText: error.statusText }
              : { status: '404', statusText: '' },
          );
        });
    }
  };

  useEffect(() => {
    const portalUrl = document
      .querySelector('body')
      .getAttribute('data-portal-url');
    if (!portalUrl) {
      return;
    }

    setPortalUrl(portalUrl);
  }, []);

  useEffect(() => {
    if (portalUrl) {
      fetchApi();
    }
  }, [portalUrl, b_size, sort_on, sort_order, query]);

  const handlePageChange = page => {
    fetchApi(b_size * (page - 1), query);
  };

  const setSorting = (column, order) => {
    setSort_on(column);
    setSort_order(order === 'asc' ? 'ascending' : 'descending');
  };

  return (
    <ApiProvider
      value={{
        fetchApi,
        data,
        query,
        setQuery,
        portalUrl,
        handleApiResponse,
        setB_size,
        b_size,
        setSorting,
        sort_on,
        sort_order,
        handlePageChange,
        apiErrors,
        setApiErrors,
        loading,
        endpoint,
      }}
    >
      {children}
    </ApiProvider>
  );
}

ApiWrapper.propTypes = {
  children: array,
};

export default ApiWrapper;
