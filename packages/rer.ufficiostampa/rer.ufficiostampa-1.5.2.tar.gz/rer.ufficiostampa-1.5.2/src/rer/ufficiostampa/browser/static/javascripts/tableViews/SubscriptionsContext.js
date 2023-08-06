import React, { useState, useEffect } from 'react';
import { array } from 'prop-types';

import apiFetch from './utils/apiFetch';

export const SubscriptionsContext = React.createContext({});

export const SubscriptionsProvider = SubscriptionsContext.Provider;
export const SubscriptionsConsumer = SubscriptionsContext.Consumer;

export const DEFAULT_B_SIZE = 25;
export const DEFAULT_SORT_ON = 'surname';
export const DEFAULT_SORT_ORDER = 'ascending';

function SubscriptionsWrapper({ children }) {
  const [subscriptions, setSubscriptions] = useState({});
  const [portalUrl, setPortalUrl] = useState(null);

  const [apiErrors, setApiErrors] = useState(null);
  const [loading, setLoading] = useState(false);
  const [b_size, setB_size] = useState(DEFAULT_B_SIZE);

  const [sort_on, setSort_on] = useState(DEFAULT_SORT_ON);
  const [sort_order, setSort_order] = useState(DEFAULT_SORT_ORDER);

  const handleApiResponse = res => {
    if (res?.status == 204 || res?.status == 200) {
      //ok
    } else {
      setApiErrors(
        res
          ? { status: res.status, statusText: res.statusText }
          : { status: '404', statusText: '' },
      );
    }
  };

  const fetchSubscriptions = (b_start = 0, query) => {
    if (portalUrl) {
      const fetches = [
        apiFetch({
          url: portalUrl + '/@subscriptions',
          params: {
            b_size,
            b_start,
            sort_on,
            sort_order,
            query,
          },
          method: 'GET',
        }),
      ];
      setLoading(true);

      Promise.all(fetches).then(data => {
        handleApiResponse(data[0]);
        setSubscriptions(data[0].data);
        setLoading(false);
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
      fetchSubscriptions();
    }
  }, [portalUrl, b_size, sort_on, sort_order]);

  const handlePageChange = page => {
    fetchSubscriptions(b_size * (page - 1));
  };

  const setSorting = (column, order) => {
    setSort_on(column);
    setSort_order(order === 'asc' ? 'ascending' : 'descending');
  };

  return (
    <SubscriptionsProvider
      value={{
        fetchSubscriptions,
        subscriptions,
        portalUrl,
        handleApiResponse,
        setB_size,
        b_size,
        setSorting,
        sort_on,
        sort_order,
        handlePageChange,
        apiErrors,
        loading,
      }}
    >
      {children}
    </SubscriptionsProvider>
  );
}

SubscriptionsWrapper.propTypes = {
  children: array,
};

export default SubscriptionsWrapper;
