import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Switch, Link, Outlet} from 'react-router-dom';
// import Map from "./Map";
import Shares from "./Shares";
import Financials from "./Financials"
// import Note from "./Note"
import Keywords from "./Keywords";
import Navbar from "./Navbar";

export default function App() {
    const[company, setCompany] = useState('')
    const[searchValue, setSearchValue] = useState('')
    
    /// async fetch request ////
    const fetchCompany = async (e) => {
        e.preventDefault();
        setSearchValue('');
    
        try {
            const response = await fetch('/companies', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(searchValue)
            });
    
            if (!response.ok) {
                throw new Error('Failed to find company');
            }
    
            const data = await response.json();
            setCompany(data);
        } catch (error) {
            console.error('Error searching companies:', error);
        }
    };
    useEffect(() => {
        const fetchCompanyJsonTest = async () => {
            setSearchValue('');
        
            try {
                const response = await fetch(`/companyfacts2/${company.ticker}`);
                if (!response.ok) {
                    throw new Error('Failed to find company');
                }
        
                const data = await response.json();
                console.log(data);
            } catch (error) {
                console.error('Error searching companies:', error);
            }
        };
        fetchCompanyJsonTest()
    }, [company.ticker]);
   
        // <Router>
        //     <Navbar />
            
        //     <Switch>
        //         <Route path="/financials" render={() => <Financials apiInfo={apiInfo}/>} />
        //         <Route path="/keywords" render={() => <Keywords company={company} />} />
        //         {/* <Route path="/comments" render={() => <Note company={company} />} />
        //         <Route path="/map" render={() => <Map company={company} />} /> */}
        //     </Switch>
        // </Router>
    return(
        <>
            <form id='company-search-form' onSubmit={fetchCompany}>
                <input id='company-input' type='text' value={searchValue} onChange={(e)=> setSearchValue(e.target.value)} placeholder="(AAPL, BRK-B, NVDA etc...)"/>
                <input id='company-submit-button' type='submit' value="Search Company Symbol"/>
                <h1 id = "co-header">{company && company.name} - ({company && company.ticker} - {company && company.cik})</h1>
            </form>
            <div id="wrapper" className="flex flex-col items-center w-full h-full border rounded bg-orange-100">
                <Financials company={company}/>
            </div>
        
        </>
  );
};








