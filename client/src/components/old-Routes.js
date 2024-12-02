import React from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';
import Financials from './Financials';
import Keywords from './Keywords';
// import Note from './Note';
import Map from './Map';
function Routes({ company, apiInfo }) {
    if (!currentUser) return <Redirect to="/" />;
  
    return (
      <Switch>
        <Route exact path="/">
          <Financials apiInfo={apiInfo} />
        </Route>
        <Route path="/keywords">
          <Keywords company={company} />
        </Route>
        <Route path="/map">
          <Map company={company} />
        </Route>
      </Switch>
    );
  }
  
  export default Routes;