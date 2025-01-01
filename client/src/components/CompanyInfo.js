import React from "react";

export default function CompanyInfo({company}) {



    return (
        <div className="w-[95%]">
            <div className="w-[47%] mt-5 text-lime-400 font-mono tracking-tight">
            <div className="px-5 py-2">
                <h2 className="font-roboto text-lg font-bold">🏢 Company Info.</h2>
                <table>
                <tbody>
                                <tr className=""><th className='text-sm font-roboto font-bold text-left'>Name:&nbsp;</th><th className="text-sm font-roboto text-left font-medium">{company && company.name && company.name}</th></tr>
                                <tr className=""><th className='text-sm font-roboto font-bold text-left'>Ticker:&nbsp;</th><th className="text-sm font-roboto text-left font-medium">{company && company.ticker && company.ticker}</th></tr>
                                {/* <tr className=""><th className='text-sm font-roboto font-bold text-left'>CIK ID#:&nbsp;</th><th className="text-sm font-roboto text-left font-medium">{company && company.cik && company.cik}</th></tr>
                                <tr className=""><th className='text-sm font-roboto font-bold text-left'>Exchange:&nbsp;</th><th className="text-sm font-roboto text-left font-medium">{company && company.exchange && company.exchange}</th></tr> */}
                                <tr className=""><th className='text-sm font-roboto font-bold text-left'>Sector:&nbsp;</th><th className="text-sm font-roboto text-left font-medium">{company && company.owner_org && company.owner_org.slice(3)}</th></tr>
                                <tr className=""><th className='text-sm font-roboto font-bold text-left'>Industry:&nbsp;</th><th className="text-sm font-roboto text-left font-medium">{company && company.sic_description && company.sic_description}</th></tr>
                                </tbody>
                            </table>
            </div>
            </div>
        </div>
    )
}