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
            <div className="w-[95%]">
                <div className="w-[47%] mt-5 text-lime-400 font-mono tracking-tight">
                    <div className="px-5 py-2">
                        <h2 className="font-roboto text-lg font-bold">🖇️ MetaTags</h2>
                        <li className="flex flex-row">
                            {keywordElements.length > 0 ? (
                                keywordElements.map((keyword, index) => <ul className="text-sm font-roboto mr-2 underline italic overflow-x-visible"key={index}>{keyword}</ul>)
                            ) : (
                                <h2 className="text-sm font-roboto mr-2">No MetaTags for this company yet.</h2>
                            )}
                        </li>
                    </div>
                </div>
            </div>
        </>
    );
}