// import React, { useEffect, useState } from "react";
// // import { Switch, Route } from "react-router-dom";

// function App() {
//   const [companies, setCompanies] = useState([]);
//   const [localCompanies, setLocalCompanies] = useState([])
//   const [difference, setDifference] = useState([])

//   const handleUpdateCompanies = () => {
//     fetch(`https://corsproxy.io/?https%3A%2F%2Fwww.sec.gov%2Ffiles%2Fcompany_tickers_exchange.json`)
//       .then(res => {
//         if (!res.ok) throw new Error('Failed to fetch companies from EDGAR');
//         return res.json()
//       })
//       .then(data => setCompanies(data.data)) 
//       .then(console.log(companies));
//   }

//   const compareCompanies = () => {
//     fetch('/companies')
//       .then(res=>{
//         if (!res.ok) throw new Error('Failed to fetch companies from local DB');
//         return res.json()
//       })
//         .then(data=>setLocalCompanies(data))
//       // .then(data => data.forEach(company => setLocalCompanies([...companies, company])))
//       // .then(setDifference(companies.filter(company => localCompanies.filter(locCompany => locCompany.cik != company[0]))))
//         // .then(companies.filter(company => {const companyCik = company[0]}))
    
    
//   //   const matchingCompanies = companies.filter(company => {
//   //     localCompanies.some(locCompany => {
//   //       locCompany.cik !== company[0];
//   //       console.log(company.cik)
//   //     })
//   //     console.log(company[0]); 
      
//   //   });

//   //   console.log(matchingCompanies)
//   // }

//   const postCompanies = () => {
//     fetch(`/companies`,{
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//         'Accept': 'application/json',
//       },
//       body: JSON.stringify({companies})
//     })
//       .then(res => {
//         if (!res.ok) throw new Error('Failed to post companies');
//         return res.json();
//       })
//       .catch(error => console.error('Failed to post companies:', error));
//   }

//   return(
//     <div>
//       <button onClick={handleUpdateCompanies}>Update Companies</button>
//       <button onClick={compareCompanies}>Compare Companies</button>
//       <button onClick={postCompanies}>Post Companies</button>
//     </div>
//   )
// }




 
// export default App;
