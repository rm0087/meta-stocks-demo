import React from "react";

export default function Keywords({ company }) {
    // Ensure company and company.comments are defined
    if (!company || !company.keywords) {
        return null;
    }

    // Create list items for each comment
    const keywordElements = company.keywords.map((keyword, index) => (
        <li key={index}>{keyword.word}</li>
    ));

    return (
        <>
            
            <h1>{company && company.name} - {company && company.ticker}</h1>
            <h2>Keywords:</h2>
            <ul className="keywords">
                {keywordElements.length > 0 ? (
                    keywordElements.map((keyword, index) => <li className="keyword"key={index}>{keyword}</li>)
                ) : (
                    <h2>No keywords for this company yet</h2>
                )}
            </ul>
        </>
    );
}