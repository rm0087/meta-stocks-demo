import React, { useEffect, useState } from "react";

export default function CompanyInfo({company, filings}) {
    const [latestFilings, setLatestFilings] = useState([])
    const [finFilings, setFinFilings] = useState([])
    const [insiderFilings, setInsiderFilings] = useState([]);
    const [institutionalFilings, setInstitutionalFilings] = useState([]);
    const [isOpen, setIsOpen] = useState(false);
    const [aiSummary, setAiSummary] = useState(null)

    function AiPopup(){

        return (
            <div>
              {/* The Modal/Popup */}
              {isOpen && (
                <div className="modal-overlay" onClick={() => setIsOpen(false)}>
                  <div className="modal-content book-page" onClick={e => e.stopPropagation()}>
                    <button 
                      className="close-button" 
                      onClick={() => {setIsOpen(false); setAiSummary(null)}}
                    >
                      ×
                    </button>
                    <div className="page-content">
                      {aiSummary ? (
                        <div>
                            <div className="flex flex-row">
                                <div className="w-[25%] flex justify-start">
                                    {aiSummary.filing && 
                                        <div className="flex flex-col">
                                            <span className="flex flex-col">
                                                <h3 className="text-xs font-bold">Filing Date: </h3>
                                                <h4 className="text-xs">{aiSummary?.filing?.filingDate}</h4>
                                            </span>
                                            <span className="flex flex-col">
                                                <h3 className="text-xs font-bold">Reporting for: </h3>
                                                <h4 className="text-xs">{aiSummary?.filing?.reportDate}</h4>
                                            </span>
                                        </div> 
                                    }
                                </div>
                                <div className="w-[50%] flex flex-col justify-center">
                                    <h1 className="flex font-bold text-xl text-center justify-center">{aiSummary.filing && company.name}</h1>
                                    <h2 className="flex text-sm text-center justify-center">{aiSummary.filing && "Ticker: " + company.ticker}</h2>
                                    <h2 className="flex font-bold text-center justify-center">{aiSummary.filing && aiSummary.title}</h2>
                                </div>
                                <div className="w-[25%] flex justify-end">
                                    {aiSummary.filing && <a className="text-xs" href={aiSummary?.filing?.urlPrefix + aiSummary?.filing?.doc} rel="noreferrer" target="_blank">Read Full Filing</a>}
                                </div>
                            </div>
                            <div dangerouslySetInnerHTML={{__html: aiSummary.summary}}/>
                        </div>
                      ) : (
                        <div>Loading AI Summary... This could take a minute... or two...</div>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
        );
    }

    const fetchAiAnalysis = async (filing) => {
        // console.log(txtUrl)
        // console.log(filing)
        setAiSummary(null)
        setIsOpen(true)

        const fullUrl = filing.urlPrefix + filing.txt
        // console.log(fullUrl)
        try {
            const response = await fetch(`ai/analyze?url=${encodeURIComponent(fullUrl)}`, {
              method: 'GET',
              headers: {
                'Accept': 'application/json'
              },
            });
            
            if (!response.ok) {
              throw new Error(`Failed to retrieve AI summary: ${response.status}`);
            }
            
            const aiResponse = await response.json();
            
            setAiSummary({
                title: filing.form,
                summary: aiResponse.summary,
                filing: filing
            })
            
          } catch (error) {
            console.error('Error retrieving AI', error);
            setAiSummary({summary:"<p>Summary cannot be displayed at this time. Please try a different filing.</p>", filing: null})
          }
        
}

    useEffect(()=>{
            setIsOpen(false)
            setAiSummary(null)

            const latest = filings?.latest?.map((filing,index)=> {
                const primaryUrl = filing.urlPrefix + filing.doc
                const txtUrl = filing.urlPrefix + filing.txt
                return (
                    <span  key={index} className="flex flex-row items-center">
                        <img className="border rounded m-1" src="ai-icon.png" onClick={(e) => fetchAiAnalysis(filing)}></img>
                        <a className="whitespace-nowrap"  target="_blank" rel="noreferrer" href={primaryUrl}>{filing.filingDate} - {filing.form}</a>
                    </span>
                )

            })
            setLatestFilings(latest)

            const fins = filings?.fin?.map((filing,index)=> {
                const primaryUrl = filing.urlPrefix + filing.doc
                const txtUrl = filing.urlPrefix + filing.txt
                return (
                    <span key={index} className="flex flex-row items-center">
                        <img className="border rounded m-1" src="ai-icon.png" onClick={(e) => fetchAiAnalysis(filing)}></img>
                        <a className="whitespace-nowrap" target="_blank" rel="noreferrer" href={primaryUrl}>{filing.reportDate} - {filing.form}</a>
                    </span>
                )
            })
            setFinFilings(fins)

            const insiders = filings?.insiders?.map((filing,index)=> {
                const primaryUrl = filing.urlPrefix + filing.doc
                const txtUrl = filing.urlPrefix + filing.txt
                return (
                    <span key={index} className="flex flex-row items-center">
                        <img className="border rounded m-1" src="ai-icon.png" onClick={(e) => fetchAiAnalysis(filing)}></img>
                        <a className="whitespace-nowrap" target="_blank" rel="noreferrer" href={primaryUrl}>{filing.filingDate} - {filing.form}</a>
                    </span>
                )
            })
            setInsiderFilings(insiders)

            const institutionals = filings?.institutions?.map((filing,index)=> {
                const primaryUrl = filing.urlPrefix + filing.doc
                const txtUrl = filing.urlPrefix + filing.txt
                return (
                    <span key={index} className="flex flex-row items-center">
                        <img className="border rounded m-1" src="ai-icon.png" onClick={(e) => fetchAiAnalysis(filing)}></img>
                        <a className="whitespace-nowrap" target="_blank" rel="noreferrer" href={primaryUrl}>{filing.filingDate} - {filing.form}</a>
                    </span>
                )
            })
            setInstitutionalFilings(institutionals)
        
    },[filings])
    
    
    // https://www.sec.gov/edgar/search/#/dateRange=custom&ciks={CIK10}
    
    return (
        <div className="w-[100%] flex justify-center mt-5">
            {isOpen? <AiPopup/>: null}
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
            <div className="w-[100%] font-mono tracking-tight font-mono tracking-tight text-xs border rounded text-white ml-5">
            <div className="px-5 py-2">
                <span className="flex flex-row">
                <h2 className="text-lg font-bold">🏢 Filings</h2><a rel="norefferer" target= "_blank" href = {"https://www.sec.gov/edgar/search/#/dateRange=10y&ciks="+company.cik_10}>View all</a>
                </span> 
                <div className="flex flex-row place-items-left w-full h-full text-gray-50 font-mono text-xs">
                    <table className="w-[25%]">
                        <tbody>
                            <h2 className="font-bold text-base">Latest (all)</h2>
                            {latestFilings}
                        </tbody>
                    </table>
                    <table className="w-[25%]">
                        <tbody>
                            <h2 className="font-bold text-base">Financial Reports</h2>
                            {finFilings}
                        </tbody>
                    </table>
                    <table className="w-[25%]">
                        <tbody>
                            <h2 className="font-bold text-base">Insiders</h2>
                            {insiderFilings}
                        </tbody>
                    </table>
                    <table className="w-[25%]">
                        <tbody>
                            <h2 className="font-bold text-base">Institutions</h2>
                            {institutionalFilings}
                        </tbody>
                    </table>
                </div>               


            </div>

            </div>
            </div>
        </div>
    )
}