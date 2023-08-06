import React from 'react';
import { array, string, object, oneOfType, func, bool } from 'prop-types';
import TextField from '../fields/TextField';
import SelectField from '../fields/SelectField';
import CheckboxField from '../fields/CheckboxField';
import DateField from '../fields/DateField';

import './index.less';

const FormFieldWrapper = ({
  parameter,
  value,
  updateQueryParameters,
  isMobile,
}) => {
  let FieldComponent = '';
  let className = '';
  if (parameter.hidden) {
    return '';
  }
  switch (parameter.type) {
    case 'select':
      FieldComponent = SelectField;
      className = 'select';
      break;
    case 'checkbox':
      FieldComponent = CheckboxField;
      className = 'checkbox';
      break;
    case 'date':
      FieldComponent = DateField;
      className = 'date';
      break;
    default:
      FieldComponent = TextField;
      className = 'text';
  }
  return (
    <div className={`field ${className}-field`}>
      <FieldComponent
        parameter={parameter}
        value={value}
        updateQueryParameters={updateQueryParameters}
        isMobile={isMobile}
      />
    </div>
  );
};

FormFieldWrapper.propTypes = {
  parameter: object,
  updateQueryParameters: func,
  value: oneOfType([string, array, object]),
  isMobile: bool,
};

export default FormFieldWrapper;
