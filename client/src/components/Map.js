import React, { useEffect, useState } from "react";
// import { Switch, Route } from "react-router-dom";

export default function Map({company}) {
   const [mapApi, setMapApi] = useState('')

// 2. If queried company exists: display data from foreign API
    useEffect(() => {
        const getInfo = () => {
            if (company.cik_10 !== undefined){
                fetch(`https://corsproxy.io/?https%3A%2F%2Fdata.sec.gov%2Fsubmissions%2FCIK${company.cik_10}.json`)
                .then(res => res.json())
                .then(data => setMapApi(data))
            }
        }
        getInfo()
    },[company])
    
    let mapUrl;

    if (mapApi){
        mapUrl = `https://www.google.com/maps/embed/v1/place?key=AIzaSyBKMTn4XBizhn-Ga8R7ziCXNty1J2lHsNc&q=${mapApi.addresses.business.street1}+${mapApi.addresses.business.city}`
    }
    
    return(
        <div id = 'location-div'>
            
            <iframe
                width="450"
                height="250"
                frameborder="0"
                referrerpolicy="no-referrer-when-downgrade"
                src={mapUrl}
                allowfullscreen>
            </iframe>
            <h1>{company.name} Business Address</h1>
            <p>{mapApi && mapApi.addresses.business.street1}</p>
            <p>{mapApi && mapApi.addresses.business.street2}</p>
            <p>{mapApi && mapApi.addresses.business.city}</p>
            <p>{mapApi && mapApi.addresses.business.stateOrCountry}</p>
            <p>{mapApi && mapApi.addresses.business.zipCode}</p>
            <br/>
            <h1>{company.name} Mailing Address</h1>
            <p>{mapApi && mapApi.addresses.mailing.street1}</p>
            <p>{mapApi && mapApi.addresses.mailing.street2}</p>
            <p>{mapApi && mapApi.addresses.mailing.city}</p>
            <p>{mapApi && mapApi.addresses.mailing.stateOrCountry}</p>
            <p>{mapApi && mapApi.addresses.mailing.zipCode}</p>
        </div>
        
    )
}