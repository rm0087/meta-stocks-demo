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
    const [query, setQuery] = useState('');  // The current value of the search input
    const [suggestions, setSuggestions] = useState([]);  // The list of company suggestions
    const [loading, setLoading] = useState(false);  // Loading state for making requests

    // Function to handle input changes
    const handleInputChange = (event) => {
        const searchQuery = event.target.value;
        setQuery(searchQuery);

        // If the query is empty, clear suggestions
        if (searchQuery.trim().length === 0) {
        setSuggestions([]);
        return;
        }

        // Fetch matching companies if the query is non-empty
        fetchSuggestions(searchQuery);
    };

    // Function to fetch suggestions from the backend
    const fetchSuggestions = async (searchQuery) => {
        setLoading(true);
        try {
        const response = await fetch(`/api/companies/search?query=${searchQuery}`);
        
        // Check if the response is ok (status code 200)
        if (response.ok) {
            const data = await response.json();
            setSuggestions(data);  // Update the suggestions with the response data
        } else {
            setSuggestions([]);  // If response is not OK, clear suggestions
        }
        } catch (error) {
        console.error("Error fetching companies", error);
        setSuggestions([]);  // Clear suggestions in case of error
        } finally {
        setLoading(false);
        }
    };
    
    /// async fetch request ////
    const fetchCompany = async (e) => {
        e.preventDefault();
        setQuery('');
    
        try {
            const response = await fetch('/companies', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(query)
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
            setQuery('');
            setSuggestions([])
        
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
                <input id='company-input' type='text' value={query} onChange={handleInputChange} placeholder="(AAPL, BRK-B, NVDA etc...)" autoComplete="off"/>
                {loading && <p>Loading...</p>}
                {suggestions.length > 0 && (
                    <ul className="list-none mt-2">
                    {suggestions.map((company) => (
                        <li key={company.id} className="p-2 border-b" onClick={(e) => fetchCompany(e)}>{company.name} </li>
                    ))}
                    </ul>
                )}
                {suggestions.length === 0 && query && !loading && (
                    <p>No companies found.</p>
                )}
                <input id='company-submit-button' type='submit' value="Search Company Symbol"/>
                <h1 id = "co-header">{company && company.name} - ({company && company.ticker} - {company && company.cik})</h1>
            </form>
            <div id="wrapper" className="flex flex-col items-center w-full h-full border rounded bg-orange-100">
                <p>{query}</p>
                <Financials company={company}/>
                <p>{query}</p>
            </div>
        
        </>
  );
};








