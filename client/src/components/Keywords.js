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
            <div className="w-[100%] flex justify-center">
                <div className="w-[95%]">
                <div className="w-[47%] my-5 tracking-tight border border rounded font-mono tracking-tight text-xs text-white">
                    <div className="px-5 py-2">
                        <h2 className="text-lg font-bold">🖇️ MetaTags</h2>
                        <li className="flex flex-row">
                            {keywordElements.length > 0 ? (
                                keywordElements.map((keyword, index) => <ul className="mr-2 overflow-x-visible tracking-tighter flex"key={index}>{keyword}{index < keywordElements.length - 1 && ','}</ul>)
                            ) : (
                                <h2 className="text-sm font-mono text-xs mr-2">No MetaTags for this company yet.</h2>
                            )}
                        </li>
                    </div>
                </div>
                </div>
            </div>
        </>
    );
}