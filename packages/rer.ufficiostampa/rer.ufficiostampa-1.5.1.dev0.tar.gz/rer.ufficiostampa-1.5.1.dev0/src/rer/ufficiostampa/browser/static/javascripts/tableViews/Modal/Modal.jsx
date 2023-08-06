import React, { useContext, useEffect, useRef, useState } from 'react';
import { TranslationsContext } from '../../TranslationsContext';

import './Modal.less';
const ModalContext = React.createContext();

const ModalBody = ({ children }) => {
  return (
    <ModalContext.Consumer>
      {() => <div className="plone-modal-body">{children}</div>}
    </ModalContext.Consumer>
  );
};
const ModalFooter = ({ children }) => {
  return (
    <ModalContext.Consumer>
      {() => <div className="plone-modal-footer">{children}</div>}
    </ModalContext.Consumer>
  );
};
const Modal = props => {
  const { show, close, children, className, id, title } = props;
  const getTranslationFor = useContext(TranslationsContext);
  const [originalFocusedNode, setOriginalFocusedNode] = useState(null);
  const modalRef = useRef(null);

  const handleTabKey = e => {
    const modal =
      modalRef?.current ?? document.querySelector('.plone-modal-content');
    const focusableModalElements = [
      ...modal.querySelectorAll(
        'a[href], button, textarea, input[type="text"], input[type="radio"], input[type="checkbox"], input[type="file"], select',
      ),
    ].filter(e => !e.disabled);
    const firstElement = focusableModalElements[0];
    const lastElement =
      focusableModalElements[focusableModalElements.length - 1];
    const activeElement = document.activeElement;
    let activeElementIsInModal = false;
    focusableModalElements.forEach(e => {
      if (e === activeElement) {
        activeElementIsInModal = true;
      }
    });
    if (
      !e.shiftKey &&
      (activeElement === lastElement || !activeElementIsInModal)
    ) {
      console.log(
        'firstElement',
        activeElement,
        firstElement,
        lastElement,
        activeElementIsInModal,
      );
      firstElement.focus();
      return e.preventDefault();
    }

    if (
      e.shiftKey &&
      (activeElement === firstElement || !activeElementIsInModal)
    ) {
      console.log(
        'lastElement',
        activeElement,
        firstElement,
        lastElement,
        activeElementIsInModal,
      );
      lastElement.focus();
      return e.preventDefault();
    }

    let activeElementIndex = focusableModalElements.indexOf(activeElement);
    let nextFousableElement =
      focusableModalElements[activeElementIndex + (e.shiftKey ? -1 : 1)];
    if (nextFousableElement) {
      nextFousableElement.focus();
      console.log(nextFousableElement, document.activeElement);
      return e.preventDefault();
    }

    console.log('cacca');
  };

  const handleEscKey = () => {
    if (originalFocusedNode && originalFocusedNode !== document.activeElement)
      originalFocusedNode.focus();
    close();
  };

  useEffect(() => {
    if (show) {
      const keyListenersMap = new Map([
        [27, handleEscKey],
        [9, handleTabKey],
      ]);
      function keyListener(e) {
        // get the listener corresponding to the pressed key
        const listener = keyListenersMap.get(e.keyCode);
        // call the listener if it exists
        return listener && listener(e);
      }

      setOriginalFocusedNode(document.activeElement);

      document.addEventListener('keydown', keyListener);

      return () => document.removeEventListener('keydown', keyListener);
    }
  }, [show]);

  return show ? (
    <div
      className={`plone-modal-ufficio-stampa plone-modal-wrapper ${className ??
        ''}`}
    >
      <div className={`plone-modal ${show ? 'fade in' : ''}`}>
        <div
          className="plone-modal-dialog"
          role="dialog"
          aria-modal="true"
          aria-labelledby={`${id}_label`}
        >
          <div className="plone-modal-content" ref={modalRef}>
            <ModalContext.Provider {...props}>
              <div className="plone-modal-header">
                {title && <h2 id={id + '_label'}>{title}</h2>}
                <button
                  className="plone-modal-close"
                  onClick={() => {
                    close();
                  }}
                  title={getTranslationFor('Close modal', 'Chiudi')}
                >
                  ×
                </button>
              </div>
              {children}
            </ModalContext.Provider>
          </div>
        </div>
      </div>
    </div>
  ) : null;
};

Modal.Body = ModalBody;
Modal.Footer = ModalFooter;

export default Modal;
