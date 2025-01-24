import React from 'react';
import { Switch, Route, BrowserRouter, Redirect } from 'react-router-dom';

import CompanyInfo from './CompanyInfo';
import Keywords from './Keywords';
import Financials from './Financials';
import KeywordTool from './KeywordTool';

function Routes({ company, shares, price }) {
  const CompanyPage = ({ company, shares, price }) => (
    <>
      <CompanyInfo company={company}/> 
      <Keywords company={company} />
      <Financials company={company} shares={shares} price={price}/>
    </>
  );

  const NotFound = () => (
    <div>
      <h1>404 - Page Not Found</h1>
      <p>The page you're looking for doesn't exist.</p>
    </div>
  );
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/" render={()=> <CompanyPage company={company} shares={shares} price={price}/>}/>
        <Route path="/keyword-tool" render={()=> <KeywordTool/>} />
        <Route render={() => <NotFound />} />
      </Switch>
    </BrowserRouter>
  );
}
  
  export default Routes;