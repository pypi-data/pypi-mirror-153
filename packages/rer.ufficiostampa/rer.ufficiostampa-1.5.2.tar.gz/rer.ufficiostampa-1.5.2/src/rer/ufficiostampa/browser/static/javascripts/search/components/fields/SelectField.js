import React, { useContext } from 'react';
import Select, { components } from 'react-select';
import { string, shape, arrayOf, func, bool } from 'prop-types';
import { TranslationsContext } from '../../../TranslationsContext';

const MultiValueLabel = props => (
  <components.MultiValueLabel {...props} className="text-primary" />
);

const ariaLiveMessages = {
  guidance: props => {
    const {
      isSearchable,
      isMulti,
      isDisabled,
      tabSelectsValue,
      context,
    } = props;
    switch (context) {
      case 'menu':
        return `Usa Su e Giù per scegliere le opzioni${
          isDisabled ? '' : ", premi Invio per selezionare l'opzione corrente"
        }, premi ESC per uscire dal menu${
          tabSelectsValue
            ? ", premi Tab per selezionare l'opzione e uscire dal menu"
            : ''
        }.`;
      case 'input':
        return `${props['aria-label'] || 'Selezione'} ha il focus ${
          isSearchable ? ', digita per affinare la lista' : ''
        }, premi Giù per aprire il menu, ${
          isMulti
            ? ' premi Sinistra per avere il focus sui valori selezionati'
            : ''
        }`;
      case 'value':
        return 'Usa Sinistra e Destra per cambiare tra i valori selezionati, premi Backspace per rimuovere il valore correntemente selezionato';
      default:
        return '';
    }
  },
  onChange: props => {
    const { action, label = '', isDisabled } = props;
    switch (action) {
      case 'deselect-option':
      case 'pop-value':
      case 'remove-value':
        return `opzione ${label}, deselezionata.`;
      case 'select-option':
        return isDisabled
          ? `opzione ${label} è disabilitata. Seleziona un\'altra opzione.`
          : `opzione ${label}, selezionata.`;
      default:
        return '';
    }
  },

  onFocus: props => {
    const {
      context,
      focused,
      options,
      label = '',
      selectValue,
      isDisabled,
      isSelected,
    } = props;

    const getArrayIndex = (arr, item) =>
      arr && arr.length ? `${arr.indexOf(item) + 1} di ${arr.length}` : '';

    if (context === 'value' && selectValue) {
      return `valore ${label} evidenziato, ${getArrayIndex(
        selectValue,
        focused,
      )}.`;
    }

    if (context === 'menu') {
      const disabled = isDisabled ? ' disabilitato' : '';
      const status = `${isSelected ? 'selezionato' : 'evidenziato'}${disabled}`;
      return `opzione ${label} ${status}, ${getArrayIndex(options, focused)}.`;
    }
    return '';
  },

  onFilter: props => {
    const { inputValue, resultsMessage } = props;
    return `${resultsMessage}${
      inputValue ? ' per il termine di ricerca ' + inputValue : ''
    }.`;
  },
};

const SelectField = ({ parameter, value = [], updateQueryParameters }) => {
  const getTranslationFor = useContext(TranslationsContext);
  const { multivalued } = parameter;
  const placeholderLabel = multivalued
    ? 'select_placeholder_multi'
    : 'select_placeholder';
  return (
    <React.Fragment>
      <label id={parameter.id + '-label'} htmlFor={parameter.id}>
        {parameter.label}
      </label>
      {parameter.help.length ? (
        <p className="discreet">{parameter.help}</p>
      ) : (
        ''
      )}
      <Select
        isMulti={multivalued}
        id={parameter.id}
        value={value.map(element => {
          return {
            value: element,
            label: element,
          };
        })}
        name={parameter.id}
        options={parameter.options}
        noOptionsMessage={() =>
          getTranslationFor('select_noOptionsMessage', 'Nessun valore')
        }
        placeholder={getTranslationFor(placeholderLabel, 'Select...')}
        ariaLiveMessages={ariaLiveMessages}
        aria-labelledby={parameter.id + '-label'}
        aria-controls="search-results-region"
        aria-atomic={true}
        screenReaderStatus={({ count }) =>
          `${count} risultat${count !== 1 ? 'i' : 'o'} disponibil${
            count !== 1 ? 'i' : 'e'
          }`
        }
        components={{
          MultiValueLabel,
        }}
        onChange={options => {
          let newValue = [];
          if (options) {
            newValue = multivalued
              ? options.map(option => option.value)
              : [options.value];
          }
          updateQueryParameters({
            [parameter.id]: newValue,
          });
        }}
      />
    </React.Fragment>
  );
};

SelectField.propTypes = {
  parameter: shape({
    id: string,
    options: arrayOf(shape({ label: string, value: string })),
    multivalued: bool,
  }),
  value: arrayOf(string),
  updateQueryParameters: func,
};

export default SelectField;
