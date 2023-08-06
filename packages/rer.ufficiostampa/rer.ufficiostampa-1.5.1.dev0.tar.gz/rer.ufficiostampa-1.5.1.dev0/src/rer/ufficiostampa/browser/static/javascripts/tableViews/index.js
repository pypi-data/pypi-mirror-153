import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

const rootElement = document.getElementById('management-wrapper');

ReactDOM.render(<App appType={rootElement.dataset.appType} />, rootElement);
