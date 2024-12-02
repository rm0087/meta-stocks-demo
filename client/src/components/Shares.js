import React, { useEffect, useState } from "react";
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
// import { Switch, Route } from "react-router-dom";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

// facts["us-gaap"].WeightedAverageNumberOfDilutedSharesOutstanding
// facts["us-gaap"].WeightedAverageNumberOfSharesOutstandingBasic

export default function Shares({company, apiInfo}) {
    const [splits, setSplits] = useState ([])
    
    let sharesPath, splitsPath;
    let sharesStr = String(sharesPath)
    let sharesData;
    let sharesLabels;

    useEffect(()=>{
        fetch(`https://financialmodelingprep.com/api/v3/historical-price-full/stock_split/${company.ticker}?apikey=EOfl8KTkpcv0ciq9jzeIjaCidrrQZTTa`)
        .then(res => res.json())
        .then(data => setSplits(data))
    },[company])

    if (apiInfo){
        if (apiInfo.facts.dei.EntityCommonStockSharesOutstanding){
            sharesPath = apiInfo.facts.dei.EntityCommonStockSharesOutstanding.units.shares
        }
        if (!apiInfo.facts.dei.EntityCommonStockSharesOutstanding){
            sharesPath = apiInfo.facts["us-gaap"].WeightedAverageNumberOfDilutedSharesOutstanding.units.shares
        }
        sharesData = sharesPath.map(shares => shares.val)
        sharesLabels = sharesPath.map(shares => shares.end)
    }
    
    if (splits){
        splitsPath = splits.historical
    }
    // let splitData = splits.historical.map(split => {split.numerator})

    // Define chart data
    const data = {
        labels: sharesLabels, // X-axis labels
        datasets: [
          {
            label: 'Shares Outsanding', // Label for the dataset
            data: sharesData, // Y-axis data
            backgroundColor: 'rgba(75, 192, 192, 0.2)', // Bar color
            borderColor: 'rgba(75, 192, 192, 1)', // Bar border color
            borderWidth: 1, // Bar border width
          },
        ],
      };
    
      // Define options for the chart
      const options = {
        responsive: true,
        plugins: {
          legend: {
            position: 'top', // Position of the legend
          },
          title: {
            display: true,
            text: 'Shares Outstanding History', // Title of the chart
          },
        },
      };

    return(
        <div id ="shares-div">
            <div id = "share-info-div">
                {/* <ul>
                    {sharesPath && sharesPath.map(shares => <li key={sharesPath.indexOf(shares)}>{shares.end} - {shares.fp} - {shares.val.toLocaleString('en-US')}</li> )}
                </ul> */}
                <h3>Stock Split History</h3>
                <ul>
                    {company && splitsPath.map(split => <li key={splitsPath.indexOf(split)}>{split.date} - {split.numerator} for {split.denominator}</li> )}
                </ul>
                <p>{apiInfo && sharesPath[sharesPath.length - 1].val.toLocaleString('en-US')} Shares Outstanding as of: {apiInfo && sharesPath[sharesPath.length - 1].end}</p>
            </div>
            <div id ="shares-graph-div">
                <p></p>
                <Bar data={data} options={options} />
                {/* <ChartJS data={data} options={options}/> */}
            </div>    
        </div>
    )
}