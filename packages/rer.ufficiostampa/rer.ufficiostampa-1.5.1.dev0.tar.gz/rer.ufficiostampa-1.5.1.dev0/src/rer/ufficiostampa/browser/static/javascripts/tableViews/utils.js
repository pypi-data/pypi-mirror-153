import { useState, useEffect } from 'react';
export const getUserFieldsLables = getTranslationFor => {
  return {
    name: getTranslationFor('Name', 'Name'),
    surname: getTranslationFor('Surname', 'Surname'),
    email: getTranslationFor('email', 'E-mail'),
    phone: getTranslationFor('phone', 'Phone'),
    newspaper: getTranslationFor('newspaper', 'Newspaper name'),
    channels: getTranslationFor('channels', 'Channels'),
  };
};

export const getHistoryFieldsLables = getTranslationFor => {
  return {
    type: getTranslationFor('Type', 'Type'),
    title: getTranslationFor('label_title', 'Title'),
    number: getTranslationFor('Number', 'Number'),
    recipients: getTranslationFor('Recipients', 'Recipients'),
    date: getTranslationFor('Date', 'Date'),
    completed_date: getTranslationFor('Completed Date', 'Completed Date'),
    status: getTranslationFor('Status', 'Status'),
    channels: getTranslationFor('subscription_channels_label', 'Channels'),
  };
};

export const useDebounce = (value, delay) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value]);

  return debouncedValue;
};
