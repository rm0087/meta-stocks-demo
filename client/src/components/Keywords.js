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
            <div className="w-[95%] ">
                <div className="w-[50%] border bg-white rounded mt-5 bg-gray-50">
                    <div className="px-5 py-2">
                    
                    <h2 className="font-roboto text-lg font-bold">Metatags</h2>
                    <ul className="flex flex-row">
                        {keywordElements.length > 0 ? (
                            keywordElements.map((keyword, index) => <li className="text-sm font-roboto mr-2 underline italic overflow-x-visible"key={index}>{keyword}</li>)
                        ) : (
                            <h2 className="text-sm font-roboto mr-2">No keywords for this company yet.</h2>
                        )}
                    </ul>
                    </div>
                </div>
            </div>
        </>
    );
}