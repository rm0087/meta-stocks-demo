import React, {useEffect, useState} from "react";

export default function App(){
    const [ticker, setTicker] = useState('')
    const [co, setCo] = useState('')
    const [coKeywords, setCoKeywords] = useState([])
    const [newKeyword, setNewKeyword] = useState('')
    const [newDesc, setNewDesc] = useState('')
    const [dbKeywords, setDbKeywords] = useState([])
    const [selectedKeyword, setSelectedKeyword] = useState('') //uses keyword id

    const handleTicker = (e) => {
        const input = e.target.value
        setTicker(input)
    }

    const handleNewKeyword = (e) => {
        const input = e.target.value
        setNewKeyword(input)
    }

    const handleNewDesc = (e) => {
        const input = e.target.value
        setNewDesc(input)
    }

    
    const fetchTicker = async (e) => {
        e.preventDefault();
        try {
            const res = await fetch(`/companies/${ticker.toUpperCase()}`, {
                method:'GET',
                headers: {
                    'Content-Type':'application/json',
                    'Accept': 'application/json'
                },
            });

            if (!res.ok) {
                throw new Error('Failed to fetch company');
            }
            
            const data = await res.json()
            setCo(data)
            setCoKeywords(data.keyword_associations)
        } catch (error) {
            console.error('Error searching companies:', error);
        }
    }

    const fetchKeywordsDb = async () => {
        try {
            const res = await fetch(`/keywords`, {
                method:'GET',
                headers: {
                    'Content-Type':'application/json',
                    'Accept': 'application/json'
                },
            });

            if (!res.ok) {
                throw new Error('Failed to fetch keywords');
            }
            
            const data = await res.json()
            setDbKeywords(data)
        } catch (error) {
            console.error('Error searching keywords:', error);
        }
    }

    useEffect(()=>{
        fetchKeywordsDb()
    },[])


    
    const keywordsMap = co && coKeywords.length > 0 ? coKeywords.map((assoc, index) => (
                <span key={index} className="m-1 col-span-1">
                    <h2 className="font-bold ">
                        {assoc.keyword.word}
                    </h2>

                    {assoc.context.map((con,index)=> (
                        <li key={index}
                            className="text-sm list-disc list-inside"
                        >
                            {con}
                        </li>
                    ))}
                </span>
    )) : null

    const keywordOptions = dbKeywords && dbKeywords.length > 0 ? dbKeywords.map((keyword, index)=>(
        <option key={index} value ={keyword.id}>{keyword.word}</option>
    )) : null
        
    return(
        <>  
            <div className="mb-10">
                <form className="">
                    <input type="text" placeholder="new keyword" value={newKeyword} onChange={handleNewKeyword}/>
                    <input type="text" placeholder="description" value={newDesc} onChange={handleNewDesc}/>
                </form>
            </div>

            <div className="flex flex-row w-full ">
                <form className="" onSubmit={fetchTicker}>
                    <input type="text" placeholder="ticker" value={ticker} onChange={handleTicker}/>
                </form>
                <h1>{co.name} ({co.ticker}) - {co.id} / {co.cik_10}</h1>
            </div>

            <div className="flex flex-row w-full">
                <select
                    value={selectedKeyword}
                    onChange={(e) => setSelectedKeyword(e.target.value)}
                > 
                    <option value="" disabled>select a keyword</option>
                    {keywordOptions}
                </select>
                <p>keyword id: {selectedKeyword}</p>
            </div>
                
            <form className="w-16">
                <textarea type="text" 
                    placeholder="context" 
                    value={newDesc} 
                    onChange={handleNewDesc}
                    className="h-48 w-96 resize-none border border-black"
                    
                />
            </form>

            <div className="grid grid-cols-6 gap-4">
                {keywordsMap}
            </div>
        </>
    )
}