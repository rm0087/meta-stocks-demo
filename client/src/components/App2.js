import React, {useEffect, useState} from "react";

export default function App(){
    const [ticker, setTicker] = useState('')
    const [co, setCo] = useState('')
    const [coKeywords, setCoKeywords] = useState([])
    const [newKeyword, setNewKeyword] = useState('')
    const [newDesc, setNewDesc] = useState('')
    const [dbKeywords, setDbKeywords] = useState([])
    const [selectedKeyword, setSelectedKeyword] = useState('') //uses keyword id
    const [context, setContext] = useState('')

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

    const handleContext = (e) => {
        const input = e.target.value;
        setContext(input)
    }

    
    const fetchTicker = async (e, ticker) => {
        if (e){
            e.preventDefault();
        }
        
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
        setTicker("")
    }

    const fetchKeywordsDb = async (e) => {
        
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

    const setAssoc = async (e) => {
        e.preventDefault()
        const payload = [co.id, selectedKeyword, context]
        try {
            const res = await fetch(`/association`, {
                method:'POST',
                headers: {
                    'Content-Type':'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                throw new Error('Failed to fetch keywords');
            }
            const data = await res.json()
            console.log(data)
            setContext("")
            fetchTicker(null, co.ticker)
        } catch (error) {
            console.error('Error searching keywords:', error);
        }
    }

    useEffect(()=>{
        fetchKeywordsDb()
    },[])


    
    const keywordsMap = co && coKeywords.length > 0 ? coKeywords.map((assoc, index) => (
                <span 
                    key={index} 
                    className="m-1 col-span-1"
                >
                    <h2 className="font-bold ">
                        {assoc.keyword.word}
                    </h2>

                    {assoc.context.map((con,index)=> (
                        <li 
                            key={index}
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
        <div className="p-5">  
            <div className="mb-10 w-full flex flex-row justify-end">
                <form className="">
                    <input 
                        type="text" 
                        placeholder="enter new keyword" 
                        value={newKeyword} 
                        onChange={handleNewKeyword}
                        className="border m-1"
                    />
                    <input 
                        type="text" 
                        placeholder="keyword description" 
                        value={newDesc} 
                        onChange={handleNewDesc}
                        className="w-96 border m-1"
                    />
                </form>
            </div>

            <div className="flex flex-col w-full">
                <form className="" onSubmit={(e)=>fetchTicker(e, ticker)}>
                    <input type="text" placeholder="enter ticker" value={ticker} onChange={handleTicker}/>
                </form>
                <h1 className="font-bold">{co.name} ({co.ticker}) - {co.id} / {co.cik_10}</h1>
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
                
            <form className="w-16" onSubmit={(e)=>setAssoc(e)}>
                <textarea type="text" 
                    placeholder="context" 
                    value={context} 
                    onChange={handleContext}
                    className="h-48 w-96 resize-none border border-black"
                    
                />
                <button type="submit">
                    Submit
                </button>
            </form>

            <div className="grid grid-cols-6 gap-4">
                {keywordsMap}
            </div>
        </div>
    )
}