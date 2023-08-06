import React, { useState } from 'react';
import TranslationsWrapper from '../TranslationsContext';
import ApiWrapper from '../ApiContext';
import Menu from './Menu/Menu';
import UsersList from './UsersList/UsersList';
import HistoryList from './HistoryList/HistoryList';
import EditUser from './EditUser/EditUser';
import ImportCSV from './CSV/ImportCSV';
import './App.less';

const App = ({ appType }) => {
  const [user, setUser] = useState(null);
  const [showImportCSV, setShowImportCSV] = useState(false);

  const endpoint = appType == 'history' ? 'send-history' : 'subscriptions';

  let children = null;
  if (appType == 'channels') {
    children = (
      <React.Fragment>
        <Menu
          editUser={() => setUser({})}
          setShowImportCSV={setShowImportCSV}
        />
        <UsersList editUser={u => setUser(u)} />
        <EditUser user={user} />
        <ImportCSV showModal={showImportCSV} setShowModal={setShowImportCSV} />
      </React.Fragment>
    );
  } else {
    children = (
      <React.Fragment>
        <Menu />
        <HistoryList />
      </React.Fragment>
    );
  }

  return (
    <TranslationsWrapper>
      <ApiWrapper endpoint={endpoint}>{children}</ApiWrapper>
    </TranslationsWrapper>
  );
};
export default App;
