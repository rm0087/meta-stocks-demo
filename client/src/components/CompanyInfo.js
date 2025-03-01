import React, { useEffect, useState } from "react";

export default function CompanyInfo({company, filings}) {
    const [latestFilings, setLatestFilings] = useState([])
    const [finFilings, setFinFilings] = useState([])
    const [insiderFilings, setInsiderFilings] = useState([]);
    const [institutionalFilings, setInstitutionalFilings] = useState([]);
    


    const fetchAiAnalysis = async (txtUrl) => {
        console.log(txtUrl)
        try {
            const response = await fetch(`ai/analyze?url=${encodeURIComponent(txtUrl)}`, {
              method: 'GET',
              headers: {
                'Accept': 'application/json'
              },
            });
            
            if (!response.ok) {
              throw new Error(`Failed to retrieve AI: ${response.status}`);
            }
            
            const data = await response.json();
            console.log(data); // This will now log {message: "your-txt-url-value"}
            return data;
          } catch (error) {
            console.error('Error retrieving AI', error);
          }
        
}

    useEffect(()=>{
        
            const latest = filings?.latest?.map((filing,index)=> {
                const primaryUrl = filing.urlPrefix + filing.doc
                const txtUrl = filing.urlPrefix + filing.txt
                return (
                    <span className="flex flex-row items-center">
                        <img className="border rounded m-1" src="ai-icon.png" onClick={(e) => fetchAiAnalysis(txtUrl)}></img>
                        <a className="whitespace-nowrap" key={index} target="_blank" rel="noreferrer" href={primaryUrl}>{filing.filingDate} - {filing.form}</a>
                    </span>
                )

            })
            setLatestFilings(latest)

            const fins = filings?.fin?.map((filing,index)=> {
                const primaryUrl = filing.urlPrefix + filing.doc
                const txtUrl = filing.urlPrefix + filing.txt
                return (

                    <span className="flex flex-row items-center">
                        <img className="border rounded m-1" src="ai-icon.png" onClick={(e) => fetchAiAnalysis(txtUrl)}></img>
                        <a className="whitespace-nowrap" key={index} target="_blank" rel="noreferrer" href={primaryUrl}>{filing.reportDate} - {filing.form}</a>
                    </span>
                )
            })
            setFinFilings(fins)

            const insiders = filings?.insiders?.map((filing,index)=> {
                const primaryUrl = filing.urlPrefix + filing.doc
                const txtUrl = filing.urlPrefix + filing.txt
                return (

                    <span className="flex flex-row items-center">
                        <img className="border rounded m-1" src="ai-icon.png" onClick={(e) => fetchAiAnalysis(txtUrl)}></img>
                        <a className="whitespace-nowrap" key={index} target="_blank" rel="noreferrer" href={primaryUrl}>{filing.filingDate} - {filing.form}</a>
                    </span>

                )
            })
            setInsiderFilings(insiders)

            const institutionals = filings?.institutions?.map((filing,index)=> {
                const primaryUrl = filing.urlPrefix + filing.doc
                const txtUrl = filing.urlPrefix + filing.txt
                return (
                    <span className="flex flex-row items-center">
                        <img className="border rounded m-1" src="ai-icon.png" onClick={(e) => fetchAiAnalysis(txtUrl)}></img>
                        <a className="whitespace-nowrap" key={index} target="_blank" rel="noreferrer" href={primaryUrl}>{filing.filingDate} - {filing.form}</a>
                    </span>
                )
            })
            setInstitutionalFilings(institutionals)
        
    },[filings])
    
    
    // https://www.sec.gov/edgar/search/#/dateRange=custom&ciks={CIK10}
    
    return (
        <div className="w-[100%] flex justify-center mt-5">
            <div className="w-[95%] flex flex-row ">
            <div className="w-[25%] font-mono tracking-tight font-mono tracking-tight text-xs border rounded text-white">
            <div className="px-5 py-2">
                <h2 className="text-lg font-bold">🏢 Company Info.</h2>
                <table>
                    <tbody>
                        <tr className=""><th className='font-bold text-left'>Name:&nbsp;</th><th className="text-left font-medium">{company && company.name && company.name}</th></tr>
                        <tr className=""><th className='font-bold text-left'>Ticker:&nbsp;</th><th className="text-left font-medium">{company && company.ticker && company.ticker}</th></tr>
                        {/* <tr className=""><th className='font-bold text-left'>CIK ID#:&nbsp;</th><th className="text-left font-medium">{company && company.cik && company.cik}</th></tr>
                        <tr className=""><th className='font-bold text-left'>Exchange:&nbsp;</th><th className="text-left font-medium">{company && company.exchange && company.exchange}</th></tr> */}
                        <tr className=""><th className='font-bold text-left'>Sector:&nbsp;</th><th className="text-left font-medium">{company && company.owner_org && company.owner_org.slice(3)}</th></tr>
                        <tr className=""><th className='font-bold text-left'>Industry:&nbsp;</th><th className="text-left font-medium">{company && company.sic_description && company.sic_description}</th></tr>
                    </tbody>
                </table>

            </div>
            </div>
            <div className="w-[50%] font-mono tracking-tight font-mono tracking-tight text-xs border rounded text-white ml-5">
            <div className="px-5 py-2">
                <span className="flex flex-row">
                <h2 className="text-lg font-bold">🏢 Filings</h2><a rel="norefferer" target= "_blank" href = {"https://www.sec.gov/edgar/search/#/dateRange=10y&ciks="+company.cik_10}>View all</a>
                </span> 
                <div className="md:grid grid-cols-2 gap-4 place-items-left w-full h-full text-gray-50 font-mono text-xs">
                    <table className="">
                        <tbody>
                            <h2 className="font-bold text-base">Latest (all)</h2>
                            {latestFilings}
                        </tbody>
                    </table>
                    <table>
                        <tbody>
                            <h2 className="font-bold text-base">Financial Reports</h2>
                            {finFilings}
                        </tbody>
                    </table>
                    <table>
                        <tbody>
                            <h2 className="font-bold text-base">Insiders</h2>
                            {insiderFilings}
                        </tbody>
                    </table>
                    <table>
                        <tbody>
                            <h2 className="font-bold text-base">Institutions</h2>
                            {institutionalFilings}
                        </tbody>
                    </table>
                </div>               


            </div>

            </div>
            </div>
            <div className="w-[50%] font-mono tracking-tight text-xs border rounded text-white ml-5">
                <div className="px-5 py-2">
                    <div className="flex flex-row justify-between items-center mb-4">
                    <h2 className="text-lg font-bold">🏢 Filings</h2>
                    <a rel="noreferrer" target="_blank" href={"https://www.sec.gov/edgar/search/#/dateRange=10y&ciks="+company.cik_10}>  (View all) </a>
                    </div>
                    
                    <div className="flex flex-row justify-center">
                        <div className="px-5 w-[25%]">
                            <h2 className="font-bold text-base">Latest</h2>
                            <div>{latestFilings}</div>
                        </div>
                        
                        <div className="px-5 w-[25%]">
                            <h2 className="font-bold text-base">Financial Reports</h2>
                            <div>{finFilings}</div>
                        </div>
                        
                        <div className="px-5 w-[25%]">
                            <h2 className="font-bold text-base">Insiders</h2>
                            <div>{insiderFilings}</div>
                        </div>
                        
                        <div className="px-5 w-[25%]">
                            <h2 className="font-bold text-base">Institutions</h2>
                            <div>{institutionalFilings}</div>
                        </div>
                    </div>
                </div>
                </div>
        </div>
        </div>
    )
}