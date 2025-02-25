import React, { useEffect, useState } from "react";

export default function CompanyInfo({company, filings}) {
    const [latestFilings, setLatestFilings] = useState([])
    const [finFilings, setFinFilings] = useState([])
    const [insiderFilings, setInsiderFilings] = useState([]);
    const [institutionalFilings, setInstitutionalFilings] = useState([]);
    

    useEffect(()=>{
        
            const latest = filings?.latest?.map((filing,index)=> {
                return (
                    <tr key={index}><td>{filing.date} - <a target="_blank" href={filing.url}>{filing.form}</a></td></tr>
                )
            })
            setLatestFilings(latest)

            const fins = filings?.fin?.map((filing,index)=> {
                return (
                    <tr key={index}><td>{filing.date} - <a target="_blank" href={filing.url}>{filing.form}</a></td></tr>
                )
            })
            setFinFilings(fins)

            const insiders = filings?.insiders?.map((filing,index)=> {
                return (
                    <tr key={index}><td>{filing.date} - <a target="_blank" href={filing.url}>{filing.form}</a></td></tr>
                )
            })
            setInsiderFilings(insiders)

            const institutionals = filings?.institutions?.map((filing,index)=> {
                return (
                    <tr key={index}><td>{filing.date} - <a target="_blank" href={filing.url}>{filing.form}</a></td></tr>
                )
            })
            setInstitutionalFilings(institutionals)
        
    },[filings])
    
    
    
    return (
        <div className="w-full justify-center mt-5">
            <div className="w-[95%] flex flex-row justify-center">
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
            <div className="w-[75%] font-mono tracking-tight font-mono tracking-tight text-xs border rounded text-white">
            <div className="px-5 py-2">
                
                <h2 className="text-lg font-bold">🏢 Filings</h2>
                <div className="md:grid grid-cols-6 gap-4 place-items-center w-full h-full text-gray-50 font-mono text-xs">
                    <table className="">
                        <tbody>
                            <h2 className="font-bold text-sm">Latest</h2>
                            {latestFilings}
                        </tbody>
                    </table>
                    <table>
                        <tbody>
                            <h2 className="font-bold text-sm">Financial Reports</h2>
                            {finFilings}
                        </tbody>
                    </table>
                    <table>
                        <tbody>
                            <h2 className="font-bold text-sm">Insiders</h2>
                            {insiderFilings}
                        </tbody>
                    </table>
                    <table>
                        <tbody>
                            <h2 className="font-bold text-sm">Institutions</h2>
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