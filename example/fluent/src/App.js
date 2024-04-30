import { FluentProvider, webLightTheme } from '@fluentui/react-components';
import React from 'react';

import {
  Button,
  makeStyles,
  shorthands,
  teamsDarkTheme,
  teamsLightTheme,
  tokens,
} from "@fluentui/react-components";

const useStyles = makeStyles({
  button: {
    marginTop: "5px",
  },
  provider: {
    ...shorthands.border("1px"),
    ...shorthands.borderRadius("5px"),
    ...shorthands.padding("5px"),
  },
  text: {
    backgroundColor: tokens.colorBrandBackground2,
    color: tokens.colorBrandForeground2,
    fontSize: "20px",
    ...shorthands.border("1px"),
    ...shorthands.borderRadius("5px"),
    ...shorthands.padding("5px"),
  },
});
const handleClick = () => {
  window.call_python('hahaha')
};
const handleClick2 = () => {
  window.call_python('hahaha2')
};
const handleClick3 = () => {
  window.call_python('hahaha3','dsdsd',1)
};
export const Default = () => {
  const styles = useStyles();
  return (
    <>
      <div>
        <FluentProvider className={styles.provider} theme={webLightTheme}>
          <div className={styles.text}>Web Light Theme</div>
          <Button className={styles.button} onClick={handleClick}>Web Light Theme</Button>
        </FluentProvider>
      </div>
      <div>
        <FluentProvider className={styles.provider} theme={teamsLightTheme}>
          <div className={styles.text}>Teams Light Theme</div>
          <Button className={styles.button} onClick={handleClick2}>Teams Light Theme</Button>
        </FluentProvider>
      </div>
      <div>
        <FluentProvider className={styles.provider} theme={teamsDarkTheme}>
          <div className={styles.text}>Teams Dark Theme</div>
          <Button className={styles.button} onClick={handleClick3}>Teams Dark Theme</Button>
        </FluentProvider>
      </div>
    </>
  );
};

function App() {
  return (
    <div>
      <Default></Default>
    </div>
  );
}

export default App;