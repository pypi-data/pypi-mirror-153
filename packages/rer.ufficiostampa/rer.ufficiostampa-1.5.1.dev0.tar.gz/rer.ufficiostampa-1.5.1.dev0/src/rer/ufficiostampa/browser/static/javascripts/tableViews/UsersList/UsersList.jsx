import React, { useState, useContext } from 'react';
import DataTable from 'react-data-table-component';
import Select from 'react-select';
import { TranslationsContext } from '../../TranslationsContext';
import {
  ApiContext,
  DEFAULT_SORT_ON,
  DEFAULT_SORT_ORDER,
} from '../../ApiContext';
import apiFetch from '../../utils/apiFetch';
import { getUserFieldsLables, useDebounce } from '../utils';
import './Users.less';

const UsersList = ({ editUser }) => {
  const getTranslationFor = useContext(TranslationsContext);
  const {
    data,
    query,
    setQuery,
    portalUrl,
    fetchApi,
    loading,
    handleApiResponse,
    setB_size,
    handlePageChange,
    b_size,
    setSorting,
  } = useContext(ApiContext);

  const labels = getUserFieldsLables(getTranslationFor);
  const [textTimeout, setTextTimeout] = useState(0);
  const [resetPaginationToggle, setResetPaginationToggle] = useState(false);
  const [toggleCleared, setToggleCleared] = useState(false);
  const [selectedRows, setSelectedRows] = React.useState([]);

  //------------------COLUMNS----------------------
  // const ChannelsCellView = (row, index, column, id) => {
  //   return (
  //     <div className="channels">
  //       {row.channels
  //         ? row.channels.map((channel, index) => {
  //             return (
  //               <span key={index}>
  //                 {channel}
  //                 {index < row.channels.length - 1 ? ',' : ''}{' '}
  //               </span>
  //             );
  //           })
  //         : []}
  //     </div>
  //   );
  // };

  const columns = [
    { name: labels.name, selector: 'name', sortable: true },
    { name: labels.surname, selector: 'surname', sortable: true },
    { name: labels.email, selector: 'email', sortable: false },
    { name: labels.phone, selector: 'phone', sortable: false, width: '180px' },
    { name: labels.newspaper, selector: 'newspaper', sortable: true },
    // {
    //   name: labels.channels,
    //   selector: 'channels',
    //   sortable: true,
    //   cell: ChannelsCellView,
    // },
    {
      name: getTranslationFor('Actions', 'Actions'),
      button: true,
      cell: row => (
        <button
          className="action editItem plone-btn plone-btn-primary plone-btn-link"
          onClick={() => {
            editUser(row);
          }}
          title={getTranslationFor('Edit', 'Edit')}
        >
          <span className="glyphicon glyphicon-pencil"></span>
        </button>
      ),
      width: '100px',
    },
  ];
  const CustomSortIcon = (
    <i aria-hidden={true} className="glyphicon glyphicon-triangle-bottom"></i>
  );

  //------------ROW SELECTION------------
  const handleRowSelected = React.useCallback(state => {
    setSelectedRows(state.selectedRows);
  }, []);

  const contextActions = React.useMemo(() => {
    const handleDelete = () => {
      // eslint-disable-next-line no-alert
      if (
        window.confirm(
          `${getTranslationFor(
            'Are you sure you want to delete this subscribed users?',
            'Are you sure you want to delete this subscribed users?',
          )} \n${selectedRows
            .map(r => r.name + ' ' + r.surname + ' (' + r.email + ')')
            .join('\n')}`,
        )
      ) {
        setToggleCleared(!toggleCleared);

        //call delete foreach item selected
        let url = portalUrl + '/@subscriptions';
        let method = 'DELETE';
        let fetches = [];

        selectedRows.forEach(r => {
          fetches.push(
            apiFetch({
              url: url + '/' + r.id,
              method: method,
            }),
          );
        });

        Promise.all(fetches).then(data => {
          handleApiResponse(data[0]);
          fetchApi();
        });
      }
    };

    return (
      <button
        key="delete"
        onClick={handleDelete}
        className="plone-btn plone-btn-danger"
      >
        {getTranslationFor('Delete', 'Delete')}
      </button>
    );
  }, [data.items, selectedRows, toggleCleared]);

  //------------FILTERING-----------

  const SubHeaderComponent = React.useMemo(() => {
    const handleClearText = () => {
      setResetPaginationToggle(!resetPaginationToggle);
      const newFilters = { ...query, text: '' };
      setQuery(newFilters);
    };

    const delayTextSubmit = value => {
      const newFilters = { ...query, text: value };
      if (textTimeout) {
        clearInterval(textTimeout);
      }
      const timeout = setTimeout(() => {
        setQuery(newFilters);
      }, 1000);
      setTextTimeout(timeout);
    };

    return (
      <>
        <div className="search-wrapper">
          <Select
            isMulti={false}
            isClearable={true}
            inputId="type"
            name={'type'}
            options={
              data.channels
                ? data.channels.map(channel => ({
                    value: channel,
                    label: channel,
                  }))
                : []
            }
            onChange={options => {
              const newFilters = {
                ...query,
                channels: options ? options.value : null,
              };
              setQuery(newFilters);
            }}
            aria-label="Seleziona un canale"
            className="type-select"
            placeholder={getTranslationFor(
              'Select a channel',
              'Select a channel',
            )}
          />
          <input
            id="search"
            type="text"
            placeholder={getTranslationFor(
              'Filter subscribers',
              'Filter subscribers',
            )}
            aria-label={getTranslationFor('Search...', 'Search...')}
            value={query.text || ''}
            //onChange={e => delayTextSubmit(e.target.value)}
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
    <div className="ufficio-stampa-users-list">
      <DataTable
        // noHeader
        columns={columns}
        data={data.items}
        striped={true}
        highlightOnHover={true}
        pointerOnHover={false}
        noDataComponent={getTranslationFor(
          'No subscribers found',
          'No subscribers found',
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
        sortIcon={CustomSortIcon}
        onSort={(column, direction) => setSorting(column.selector, direction)}
        paginationResetDefaultPage={resetPaginationToggle} // optionally, a hook to reset pagination to page 1
        subHeader
        subHeaderComponent={SubHeaderComponent}
        selectableRows
        onSelectedRowsChange={handleRowSelected}
        contextActions={contextActions}
        clearSelectedRows={toggleCleared}
        contextMessage={{
          singular: getTranslationFor('item_selected', 'item selected'),
          plural: getTranslationFor('items_selected', 'items selected'),
          message: '',
        }}
      />
    </div>
  );
};
export default UsersList;
