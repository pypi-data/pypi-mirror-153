import React, { useContext } from 'react';
import { object } from 'prop-types';
import format from 'date-fns/format';
import isAfter from 'date-fns/isAfter';

import { TranslationsContext } from '../../../TranslationsContext';

import './index.less';

const ResultItem = ({ data }) => {
  const getTranslationFor = useContext(TranslationsContext);
  const { effective } = data;

  let effectiveDateItem = '';
  if (effective) {
    const effectiveDate = new Date(effective);
    if (isAfter(effectiveDate, new Date(1969, 11, 31))) {
      effectiveDateItem = (
        <p>
          <span className="labelTB">
            {getTranslationFor('comunicato_published_on', '')}
          </span>
          &nbsp;
          <span>{format(new Date(effective), 'dd/MM/yyyy')}</span>
        </p>
      );
    }
  }
  return (
    <div className="search-result">
      <h3 className="comunicatoTitle">
        <a className={`state-${data.review_state}`} href={data['@id']}>
          <span>{data.title}</span>
        </a>
      </h3>
      <div className="resultDetail">
        {data.description}
        <div className="resultDates">{effectiveDateItem}</div>
      </div>
    </div>
  );
};

ResultItem.propTypes = {
  data: object,
};

export default ResultItem;
