import React, { useState, useEffect, useContext } from 'react';
import { TranslationsContext } from '../../TranslationsContext';
import Modal from '../Modal/Modal';

import './Field.less';

const isValidEmail = email => {
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
};

const Field = ({
  name,
  label,
  value,
  onChange,
  required,
  errors,
  type = 'text',
  options = [], //for type 'multiselect'
  confirmRemove = false, //for type 'multiselect. If true ask user if he really want to uncheck option
  tabIndex,
}) => {
  const getTranslationFor = useContext(TranslationsContext);
  const otherProps = { tabIndex };

  const readBase64File = (name, file) => {
    if (file) {
      // Make new FileReader
      let reader = new FileReader();

      // Convert the file to base64 text
      reader.readAsDataURL(file);

      // on reader load somthing...
      reader.onload = () => {
        // Make a fileInfo Object
        const base64String = reader.result
          .replace('data:', '')
          .replace(/^.+,/, '');
        let fileInfo = {
          name: file.name,
          type: file.type,
          size: file.size,
          base64: base64String,
          file: file,
        };
        onChange(name, fileInfo);
      };
    } else {
      onChange(name, null);
    }
  };

  return (
    <div className={`field ${type}`}>
      {/* ------- checkbox -------- */}
      <label htmlFor={`formfield-${name}`} className="horizontal">
        {type == 'checkbox' && (
          <input
            id={`formfield-${name}`}
            name={name}
            checked={value || false}
            onChange={event => {
              onChange(name, event.target.checked);
            }}
            type="checkbox"
            {...otherProps}
          />
        )}
        {label}
        {required && (
          <span
            className="required horizontal"
            title={getTranslationFor('Required', 'Obbligatorio')}
          >
            &nbsp;
          </span>
        )}
      </label>

      {errors[name] && <div className="fieldErrorBox">{errors[name]}</div>}

      {/* ------- text -------- */}
      {type == 'text' && (
        <input
          id={`formfield-${name}`}
          name={name}
          value={value ?? ''}
          onChange={event => {
            onChange(name, event.target.value);
          }}
          type="text"
          {...otherProps}
        />
      )}

      {/* ------- multiselect -------- */}
      {type == 'multiselect' && (
        <div className="multiselection">
          {options.map((opt, index) => (
            <span className="option" key={name + '-opt-' + index}>
              <input
                type="checkbox"
                id={`formfield-${name}-opt-${index}`}
                name={`formfield-${name}-list`}
                className="checkbox-widget tuple-field"
                value={opt}
                checked={value?.indexOf(opt) >= 0 ? 'checked' : false}
                onChange={() => {
                  let v = JSON.parse(JSON.stringify(value ?? []));
                  if (v.indexOf(opt) >= 0) {
                    if (confirmRemove) {
                      if (
                        window.confirm(
                          `${getTranslationFor(
                            'Are you sure you want to uncheck this item',
                            'Are you sure you want to uncheck this item',
                          )}: ${opt}?`,
                        )
                      ) {
                        //remove item
                        v.splice(v.indexOf(opt), 1);
                      } else {
                        //do nothing
                      }
                    }
                  } else {
                    v.push(opt);
                  }
                  onChange(name, v);
                }}
                {...otherProps}
              />
              <label htmlFor={`formfield-${name}-opt-${index}`}>
                <span className="label">{opt}</span>
              </label>
            </span>
          ))}
        </div>
      )}

      {/* ------- file -------- */}
      {type == 'file' && (
        <div className="file-input">
          <input
            id={`formfield-${name}`}
            name={name}
            onChange={event => {
              readBase64File(name, event.target.files?.[0]);
            }}
            type="file"
            {...otherProps}
          />
          {value && (
            <div className="file-value">
              {value.name} ({Math.ceil(value.size / 1000)} kb){' '}
              <button
                onClick={() => onChange(name, null)}
                className="plone-btn plone-btn-xs"
                title={getTranslationFor('Remove file', 'Remove file')}
              >
                {' '}
                x
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
export default Field;
