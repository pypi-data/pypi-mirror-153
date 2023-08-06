import React, { useState, useContext } from 'react';
import DataTable from 'react-data-table-component';
import format from 'date-fns/format';
import { TranslationsContext } from '../../TranslationsContext';
import Select from 'react-select';
import {
  ApiContext,
  DEFAULT_SORT_ON,
  DEFAULT_SORT_ORDER,
} from '../../ApiContext';
import { getHistoryFieldsLables } from '../utils';
import './History.less';

const HistoryList = () => {
  const getTranslationFor = useContext(TranslationsContext);
  const {
    data,
    query,
    setQuery,
    loading,
    setB_size,
    handlePageChange,
    b_size,
    setSorting,
  } = useContext(ApiContext);

  const labels = getHistoryFieldsLables(getTranslationFor);
  const [textTimeout, setTextTimeout] = useState(0);
  const [resetPaginationToggle, setResetPaginationToggle] = useState(false);

  //------------------COLUMNS----------------------
  const StatusCell = row => {
    let statusIcon = '';
    switch (row.status) {
      case 'success':
        statusIcon = (
          <span className="glyphicon glyphicon-ok-sign success"></span>
        );
        break;
      case 'error':
        statusIcon = <span className="glyphicon glyphicon-alert error"></span>;
        break;
      case 'sending':
        statusIcon = <span className="glyphicon glyphicon-hourglass"></span>;
        break;
      default:
        statusIcon = <span>{row.status}</span>;
        break;
    }
    return <div className="status">{statusIcon}</div>;
  };

  const columns = [
    {
      name: labels.status,
      selector: 'status',
      sortable: true,
      cell: StatusCell,
      width: '50px',
    },
    {
      name: labels.type,
      selector: 'type',
      sortable: true,
      width: '150px',
    },
    {
      name: labels.channels,
      selector: 'channels',
      sortable: false,
      width: '150px',
      cell: row => <div>{row.channels.join(', ')}</div>,
    },
    {
      name: labels.date,
      selector: 'date',
      sortable: true,
      cell: row => (
        <div>{format(new Date(row.date), 'dd/MM/yyyy HH:mm:ss')}</div>
      ),
      width: '160px',
    },
    {
      name: labels.completed_date,
      selector: 'completed_date',
      sortable: true,
      cell: row => (
        <div>
          {row.completed_date
            ? format(new Date(row.completed_date), 'dd/MM/yyyy HH:mm:ss')
            : ''}
        </div>
      ),
      width: '160px',
    },
    {
      name: labels.recipients,
      selector: 'recipients',
      sortable: false,
      width: '80px',
    },
    { name: labels.number, selector: 'number', sortable: true, width: '80px' },
    {
      name: labels.title,
      selector: 'title',
      sortable: true,
      cell: row => (
        <div>
          <a href={row.url} title={row.title}>
            {row.title}
          </a>
        </div>
      ),
    },
  ];

  //------------FILTERING-----------

  const SubHeaderComponent = React.useMemo(() => {
    const handleClearText = () => {
      setResetPaginationToggle(!resetPaginationToggle);
      const newFilters = { ...query, text: '' };
      setQuery(newFilters);
    };

    return (
      <>
        <div className="search-wrapper">
          <Select
            isMulti={false}
            isClearable={true}
            inputId="type"
            name={'type'}
            options={[
              { value: 'Comunicato Stampa', label: 'Comunicato Stampa' },
              { value: 'Invito Stampa', label: 'Invito Stampa' },
            ]}
            onChange={options => {
              const newFilters = {
                ...query,
                type: options ? options.value : null,
              };
              setQuery(newFilters);
            }}
            className="type-select"
            aria-label="Seleziona una tipologia"
            placeholder={getTranslationFor('Select a type', 'Select a type')}
          />
          <input
            id="search"
            type="text"
            placeholder={getTranslationFor('Filter history', 'Filter history')}
            aria-label={getTranslationFor('Search...', 'Search...')}
            value={query.text || ''}
            onChange={e => setQuery({ ...query, text: e.target.value })}
          />
          <button
            type="button"
            onClick={handleClearText}
            title={getTranslationFor('Clear', 'Clear')}
          >
            <span
              aria-hidden={true}
              className="glyphicon glyphicon-remove"
            ></span>
          </button>
        </div>
      </>
    );
  }, [query, resetPaginationToggle, data.items]);

  return (
    <div className="ufficio-stampa-history-list">
      <DataTable
        columns={columns}
        data={data.items}
        striped={true}
        highlightOnHover={true}
        pointerOnHover={false}
        noDataComponent={getTranslationFor(
          'No send history found',
          'No send history found',
        )}
        responsive={true}
        defaultSortField={DEFAULT_SORT_ON}
        defaultSortAsc={DEFAULT_SORT_ORDER == 'ascending'}
        pagination={true}
        paginationRowsPerPageOptions={[5, 25, 50, 100]}
        paginationPerPage={b_size}
        paginationServer={true}
        paginationServerOptions={{
          persistSelectedOnPageChange: true,
          persistSelectedOnSort: false,
        }}
        paginationTotalRows={data.items_total}
        onChangeRowsPerPage={size => setB_size(size)}
        onChangePage={handlePageChange}
        progressPending={loading}
        sortServer={true}
        onSort={(column, direction) => setSorting(column.selector, direction)}
        paginationResetDefaultPage={resetPaginationToggle} // optionally, a hook to reset pagination to page 1
        subHeader
        subHeaderComponent={SubHeaderComponent}
      />
    </div>
  );
};
export default HistoryList;
