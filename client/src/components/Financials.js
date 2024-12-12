import React, { useEffect, useState } from "react";
import { Bar, Line } from 'react-chartjs-2';
// import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, PointElement } from 'chart.js';
import 'chart.js/auto'

// facts["us-gaap"].CashAndCashEquivalentsAtCarryingValue.units
export default function Financials({company}){
    
    let assetsData, liabilitiesData, stockholdersData, revenueData,revenueLabels, cashData, opCfData, opCfLabels, invCfData, invCfLabels, finCfData, finCfLabels, netCfData, netCfLabels, goodwillData, goodwillLabels, netIncomeData, netIncomeLabels; // declare chart/bar data
    let assetsLabels, primaryLabels; // declare chart/bar labels

    const[api, setApi] = useState([])
    const[incApi, setIncApi] = useState([])
    const[cfApi, setCfApi] = useState([])

    useEffect(() =>{
        const fetchBs = async () => {
            try {
                const response = await fetch(`/balance_sheets/${company.cik}`);
                if (response.ok) {
                    const data = await response.json();
                    setApi(data)
                } else {
                    setApi([])
                    console.error('Failed to fetch balance sheets:', response.status);
                }
            } catch (error) {
                console.error('Error fetching balance sheets:', error);
            }
        };

        const fetchInc = async () => {
            try {
                const response = await fetch(`/income_statements/${company.cik}`);
                if (response.ok) {
                    const data = await response.json();
                    setIncApi(data)
                } else {
                    setIncApi([])
                    console.error('Failed to fetch income statements:', response.status);
                }
            } catch (error) {
                console.error('Error fetching income statements:', error);
            }
        };

        const fetchCf = async () => {
            try {
                const response = await fetch(`/cf_statements/${company.cik}`);
                if (response.ok) {
                    const data = await response.json();
                    setCfApi(data)
                } else {
                    setCfApi([])
                    console.error('Failed to fetch cashflow statements:', response.status);
                }
            } catch (error) {
                console.error('Error fetching cashflow statements:', error);
            }
        };

        fetchBs()
        fetchInc()
        fetchCf()
    },[company])

//// 1.) Create data and labels for bar and other charts ////////////////////////////////////////////////////////////////////////////////////////////////
    assetsData = api.map(bs => bs.total_assets)
    assetsLabels = api.map(bs => bs.end)
    liabilitiesData = api.map(bs => bs.total_liabilities)
    stockholdersData = api.map(bs => bs.total_stockholders_equity)
    primaryLabels = assetsLabels

    revenueData = incApi.map(inc => inc.total_revenue)
    revenueLabels = incApi.map(inc => inc.end)

    opCfData = cfApi.map(cf => cf.opr_cf)
    opCfLabels = cfApi.map(cf => cf.end)

    invCfData = cfApi.map(cf => cf.inv_cf)
    invCfLabels = cfApi.map(cf => cf.end)

    finCfData = cfApi.map(cf => cf.fin_cf)
    finCfLabels = cfApi.map(cf => cf.end)

    netCfData = cfApi.map(cf => cf.net_cf)
    netCfLabels = cfApi.map(cf => cf.end)

    cashData = api.map(bs => bs.cash_and_equiv)

    goodwillData = api.map(bs => bs.goodwill)
    goodwillLabels = api.map(bs => bs.end)

    netIncomeData = incApi.map(inc => inc.net_income)
    netIncomeLabels = incApi.map(inc => inc.end)

    function formatNumber(num, digits=3) {
        if (typeof num !== 'number' || isNaN(num)) {
            return 0;
        }
        if (Math.abs(num) >= 1000000000000) {
            return (num / 1000000000000).toFixed(digits) + ' T';
        } else if (Math.abs(num) >= 1000000000) {
            return (num / 1000000000).toFixed(digits) + ' B';
        } else if (Math.abs(num) >= 1000000) {
            return (num / 1000000).toFixed(digits) + ' M';
        } else if (Math.abs(num) >= 1000) {
            return (num / 1000).toFixed(digits) + ' K';
        } else {
            return num.toFixed(0);
        }
    }

    
    // define data for LINE graphs
    function lineData(labels, data, data2, data3, data4, data5){
        const dataObj = {
            labels: labels,
            datasets: [{
                label: 'Assets',
                data: data,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                pointBackgroundColor: 'rgb(75, 192, 192)',
                tension: 0.4
            },
            {
                label: 'Liabilities',
                data: data2,
                fill: false,
                borderColor: 'rgb(255, 0, 0)',
                pointBackgroundColor: 'rgb(255, 0, 0)',
                tension: 0.4
            },
            {
                label: `Stockholders' Equity`,
                data: data3,
                fill: false,
                borderColor: 'rgb(0, 0, 0)',
                pointBackgroundColor: 'rgb(0, 0, 0)',
                tension: 0.4
            },
            {
                label: `Cash and Equivalents`,
                data: data5,
                fill: false,
                borderColor: 'rgb(0, 128, 0)',
                pointBackgroundColor: 'rgb(0, 128, 0)',
                tension: 0.4
            },
            {
                label: `Goodwill`,
                data: data4,
                fill: false,
                borderColor: 'rgb(255, 255, 0)',
                pointBackgroundColor: 'rgb(255, 255, 0)',
                tension: 0.4
            },
            
            ]
        };
        return dataObj
    }

    function revData(labels,data, data2){
        const dataObj = {
            labels: labels,
            datasets: [
            {
                label: 'Net Income',
                data: data2,
                fill: false,
                borderColor: 'rgb(255, 0, 0)',
                pointBackgroundColor: 'rgb(255, 0, 0)',
                tension: 0.4
            }, 
            {
                label: 'Revenue',
                data: data,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                pointBackgroundColor: 'rgb(75, 192, 192)',
                tension: 0.4
            },
            
            ]
        };
        return dataObj
    }

    function cfData(labels, data, data2, data3){
        const dataObj = {
            labels: labels,
            datasets: [{
                label: 'Operating Cashflows',
                data: data,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                pointBackgroundColor: 'rgb(75, 192, 162)',
                tension: 0.3
            },
            {
                label: 'Investing Cashflows',
                data: data2,
                fill: false,
                borderColor: 'rgb(0, 0, 0)',
                pointBackgroundColor: 'rgb(0, 0, 0)',
                tension: 0.3
            },
            {
                label: `Financing Cashflows`,
                data: data3,
                fill: false,
                borderColor: 'rgb(255, 0, 0)',
                pointBackgroundColor: 'rgb(255, 0, 0)',
                tension: 0.3
            },
            // {
            //     label: `Net Cashflows`,
            //     data: data4,
            //     fill: false,
            //     borderColor: 'rgb(255, 100, 100)',
            //     tension: 0.1
            // }
            ]
            
        }
        return dataObj
    }

    // define options for LINE graphs
    const options = {
        responsive: true,
        elements: {
            line: {
                borderWidth: 4,
                capBezierPoints: false,
                lineJoin: 'round',

            },
            point:{
                pointStyle: true,
                radius: 2,
                hoverRadius: 4
            },
        },

        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    color: '#000000',
                    usePointStyle: true,
                    pointStyle: 'rect',
                    font: {
                        family: 'Arial',
                    },
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const label1 = context.dataset.label + ': ' + incApi[0].currency + ' ' + formatNumber(context.parsed.y, 3);
                       
                        return label1;
              }
            }
          },
          
        },
        scales: {
            x: {
                ticks: {
                    stepSize: 4,
                    
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.0)' // Adjust alpha (opacity) here
                }
            },
            y: {
                ticks: {
                    callback: function(label, index, values) {
                    
                        
                        return "$" + "" + formatNumber(label,0);
                    },
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.03)' // Adjust alpha (opacity) here
                }
            }
        },
    }
    
    // Define data for BAR graphs
    function barData(labels, data, dataSetLabel, backgroundColor = 'rgba(75, 192, 192, 0.2)', borderColor = 'rgba(75, 192, 192, 1)', borderWidth = 1){
        const dataObj = {
            labels: labels, // X-axis labels
            datasets: [
                {
                    label: dataSetLabel, // Label for the dataset
                    data: data, // Y-axis data
                    backgroundColor: backgroundColor, // Bar color
                    borderColor: borderColor, // Bar border color
                    borderWidth: borderWidth, // Bar border width
                },
            ],
        };
        return dataObj
    }

    // Define options for BAR graphs
    function barOptions(header){
        const optionsObj = {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top', // Position of the legend
                },
                title: {
                    display: true,
                    text: header, // Title of the chart
                },
            },
        };
        return optionsObj
    }

    // {/* <Bar data={barData(cashLabels, cashData, "Cash")} options={barOptions("Cash History")} /> */}
    // {/* <p>${company && cashPath[cashPath.length - 1].val.toLocaleString('en-US')} Cash & Equivialents as of: {company && cashPath[cashPath.length - 1].end}</p> */}

//// 2.) Render component in JSX ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // ## BAR DATA TEMPLATE ##: function barData(labels, data, dataSetLabel, backgroundColor = 'rgba(75, 192, 192, 0.2)', borderColor = 'rgba(75, 192, 192, 1)', borderWidth = 1)
    return(
        <>  
            <div id ="stats" className="w-[95%] flex flex-row mt-5 ">
                <div className="w-[50%] rounded border bg-gray-50 px-5 py-2 ">
                        <p className='text-lg font-roboto font-bold'>🔑 Financials</p>
                        
                        <div className="flex flex-row justify-left">
                            <table>
                                <tr className=""><th className='text-sm font-roboto font-bold text-right'>Assets:&nbsp;</th> <th className="text-sm font-roboto text-right text-green-700 font-medium">{incApi.length > 0 && incApi[0].currency ? incApi[0].currency : ''} {company && assetsData.length > 0 ? formatNumber(assetsData[assetsData.length - 1], 3) : ''}</th></tr>
                                <tr className=""><th className='text-sm font-roboto font-bold text-right'>Liabilities:&nbsp;</th> <th className="text-sm font-roboto text-right text-red-500 font-medium">{incApi.length > 0 && incApi[0].currency ? incApi[0].currency : ''} {company && liabilitiesData.length > 0 ? formatNumber(liabilitiesData[liabilitiesData.length - 1], 3) : ''}</th></tr>
                                <tr className=""><th className='text-sm font-roboto font-bold text-right'>Stockholders Equity:&nbsp;</th> <th className="text-sm font-roboto text-right font-medium">{incApi.length > 0 && incApi[0].currency ? incApi[0].currency : ''} {company && stockholdersData.length > 0 ? formatNumber(stockholdersData[stockholdersData.length - 1], 3) : ''}</th></tr>
                                <tr className=""><th className='text-sm font-roboto font-bold text-right'>Cash:&nbsp;</th><th className="text-sm font-roboto text-right text-green-700 font-medium">{incApi.length > 0 && incApi[0].currency ? incApi[0].currency : ''} {company && cashData.length > 0 ? formatNumber(cashData[cashData.length - 1], 3) : ''}</th></tr>
                            </table>
                            <table className="ml-5">
                                <tr className=""><th className='text-sm font-roboto font-bold text-right'>Revenue (Q):&nbsp;</th> <th className="text-sm font-roboto text-right font-medium">{incApi.length > 0 && incApi[0].currency ? incApi[0].currency : ''} {company && revenueData.length > 0 ? formatNumber(revenueData[revenueData.length - 1], 3) : ''}</th></tr>
                                <tr className=""><th className='text-sm font-roboto font-bold text-right'>Net Income (Q):&nbsp;</th> <th className="text-sm font-roboto text-right font-medium">{incApi.length > 0 && incApi[0].currency ? incApi[0].currency : ''} {company && netIncomeData.length > 0 ? formatNumber(netIncomeData[netIncomeData.length - 1], 3) : ''}</th></tr>
                                <tr className=""><th className='text-sm font-roboto font-bold text-right'>Revenue (TTM):&nbsp;</th> - <th className="text-sm font-roboto text-right font-medium"></th></tr>
                                <tr className=""><th className='text-sm font-roboto font-bold text-right'>Net Income (TTM):&nbsp;</th> - <th className="text-sm font-roboto text-right font-medium"></th></tr>
                            </table>
                        
                        </div>
                            <p className='text-base text-xs font-roboto italic p-1 text-left'>Latest financial statements as of:&nbsp;{company && assetsLabels[assetsLabels.length - 1]} </p>
                        
                </div>

                <div className="w-[33%] rounded border bg-gray-50 px-5 py-2 ml-12">
                        <p className='text-lg font-roboto font-bold'>📊 Valuation</p>
                        <table className="w-[50%]">
                            <tr className=""><th className='text-sm font-roboto font-bold text-right'>Market Capitalization:&nbsp;</th> <th className="text-sm font-roboto text-right font-medium">{incApi.length > 0 && incApi[0].currency ? incApi[0].currency : ''}</th></tr>
                            <tr className=""><th className='text-sm font-roboto font-bold text-right'>Earnings per Share (EPS):&nbsp;</th> <th className="text-sm font-roboto text-right font-medium">{incApi.length > 0 && incApi[0].currency ? incApi[0].currency : ''}</th></tr>
                            <tr className=" "><th className='text-sm font-roboto font-bold text-right'>Price-to-Earnings (P/E):&nbsp;</th> <th className="text-sm font-roboto text-right font-medium">{incApi.length > 0 && incApi[0].currency ? incApi[0].currency : ''}</th></tr>
                            <tr className=""><th className='text-sm font-roboto font-bold text-right'>Price-to-Sales (P/S):&nbsp;</th> <th className="text-sm font-roboto text-right font-medium">{incApi.length > 0 && incApi[0].currency ? incApi[0].currency : ''}</th></tr>
                            <tr className=""><th className='text-sm font-roboto font-bold text-right'>Enterprise Value (EV):&nbsp;</th><th className="text-sm font-roboto text-right font-medium">{incApi.length > 0 && incApi[0].currency ? incApi[0].currency : ''}</th></tr>
                        </table>
                </div>

                <div className="w-[33%] rounded border bg-gray-50 px-5 py-2 ml-12">
                        <p className='text-lg font-roboto font-bold'>🩳 Short Info.</p>
                        <table>
                            <tr className=""><th className='text-sm font-roboto font-bold text-right'>Shares Available:&nbsp;</th> <th className="text-sm font-roboto content-center"></th></tr>
                            <tr className=""><th className='text-sm font-roboto font-bold text-right'>Borrow Rate %:&nbsp;</th> <th className="text-sm font-roboto content-center"></th></tr>
                            <tr className=""><th className='text-sm font-roboto font-bold text-right'>Short Float %:&nbsp;</th> <th className="text-sm font-roboto content-center"></th></tr>
                        </table>
                </div>

            </div>
            <div id ="cash-graph-div" className="md:grid grid-cols-2 gap-4 place-items-center mt-5 w-full h-full">
                <div className = "border border-black rounded w-[90%] h-full">
                    <h2 className="text-center font-bold">Balance Sheet History</h2>
                    <Line data={lineData(primaryLabels, assetsData, liabilitiesData, stockholdersData, goodwillData, cashData)} options={options}/>
                </div>
                <div className = "border border-black rounded w-[90%] h-full">
                    <h2 className="text-center font-bold">Income Statement History</h2>
                    <Line data={revData(netIncomeLabels, revenueData, netIncomeData)} options={options}/>
                </div>
                <div className = "border border-black rounded w-[90%] h-full">
                    <h2 className="text-center font-bold">Cashflows History</h2>
                    <Line data={cfData(opCfLabels, opCfData, invCfData, finCfData,)} options={options}/>
                </div>
            </div>  
        </>
    )
}