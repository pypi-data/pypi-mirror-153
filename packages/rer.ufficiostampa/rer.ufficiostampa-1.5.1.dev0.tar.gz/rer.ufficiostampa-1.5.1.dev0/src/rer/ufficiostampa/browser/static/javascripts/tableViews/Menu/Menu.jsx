import React, { useContext, useState } from 'react';
import { TranslationsContext } from '../../TranslationsContext';
import { ApiContext } from '../../ApiContext';
import apiFetch from '../../utils/apiFetch';
import { downloadCSV } from '../CSV/ExportCSV';
import PropTypes from 'prop-types';

import './Menu.less';

const Menu = ({ editUser, setShowImportCSV }) => {
  const getTranslationFor = useContext(TranslationsContext);
  const {
    portalUrl,
    fetchApi,
    handleApiResponse,
    apiErrors,
    endpoint,
    setApiErrors,
    query,
  } = useContext(ApiContext);

  const isSubscriptionPanel = endpoint === 'subscriptions';
  const deleteLabel = isSubscriptionPanel
    ? 'Delete all subscriptions'
    : 'Delete all history';

  const confirmDeleteLabel = isSubscriptionPanel
    ? 'Are you sure you want to delete all subscriptions?'
    : 'Are you sure you want to delete all history?';

  const deleteAllUsers = () => {
    if (
      window.confirm(getTranslationFor(confirmDeleteLabel, confirmDeleteLabel))
    ) {
      let fetches = [
        apiFetch({
          url: portalUrl + '/@' + endpoint + '-clear',
          method: 'GET',
        }),
      ];

      Promise.all(fetches).then(data => {
        handleApiResponse(data[0]);
        fetchApi();
      });
    }
  };

  const isManager = document
    .querySelector('body')
    .classList.contains('userrole-manager');

  return (
    <>
      <div className="ufficiostampa-menu-wrapper">
        <div className="left-zone">
          {isSubscriptionPanel && (
            <>
              <button
                onClick={() => editUser()}
                className="plone-btn plone-btn-primary context"
              >
                {getTranslationFor('Add Subscriber', 'Add subscriber')}
              </button>
              <button
                className="plone-btn plone-btn-primary context"
                onClick={() => setShowImportCSV(true)}
              >
                {getTranslationFor('Import from CSV', 'Import from CSV')}
              </button>
            </>
          )}
          <button
            onClick={() =>
              downloadCSV({
                portalUrl,
                endpoint,
                setApiErrors,
                getTranslationFor,
                query,
              })
            }
            className="plone-btn plone-btn-primary context"
          >
            {getTranslationFor('Export in CSV', 'Export in CSV')}
          </button>

          {isSubscriptionPanel && (
            <a
              href={`${portalUrl}/ufficiostampa-settings`}
              className="plone-btn plone-btn-primary context"
            >
              <span>{getTranslationFor('Settings', 'Settings')}</span>
            </a>
          )}
        </div>
        {isManager && (
          <div className="right-zone">
            <button
              onClick={() => deleteAllUsers()}
              className="plone-btn plone-btn-danger"
            >
              {getTranslationFor(deleteLabel, deleteLabel)}
            </button>
          </div>
        )}
      </div>

      {apiErrors && (
        <div className="errors">
          <dl className="portalMessage error" role="alert">
            <dt>Error. Status code: {apiErrors.status}</dt>
            <dd>{apiErrors.statusText}</dd>
          </dl>
        </div>
      )}
    </>
  );
};

Menu.propTypes = {
  editUser: PropTypes.func,
  setShowImportCSV: PropTypes.func,
};

export default Menu;
