// import React, {useState, useEffect} from "react";

// export default function Note({ company }) {
//     // Ensure company and company.comments are defined
//     const [notes, setNotes] = useState([]);
//   const [newNote, setNewNote] = useState('');
//   const [editingNote, setEditingNote] = useState(null);
//   const [editContent, setEditContent] = useState('');

//   useEffect(() => {
//     setNotes(company.notes)
//     // fetchNotes();
//   }, [company]);

//   const fetchNotes = async () => {
//     try {
//         const response = await fetch('/notes', {
//           method: 'POST',
//           headers: {
//             'Content-Type': 'application/json',
//           },
//           body: JSON.stringify({
//             company_id: company.id
//            }),
//         });
//       setNotes(response);
//     } catch (error) {
//       console.error('Error fetching notes:', error);
//     }
//   };

//   const handleAddNote = async () => {
//     if (newNote) {
//       try {
//         const response = await fetch('/notes', {
//           method: 'POST',
//           headers: {
//             'Content-Type': 'application/json',
//           },
//           body: JSON.stringify({ content: newNote,
//             company_id: company.id
//            }),
//         });
//         const data = await response.json();
//         setNewNote('');
//         fetchNotes();
//       } catch (error) {
//         console.error('Error adding note:', error);
//       }
//     }
//   };

//   const handleUpdateNote = async (id) => {
//     if (editContent) {
//       try {
//         const response = await fetch(`notes/${id}`, {
//           method: 'PUT',
//           headers: {
//             'Content-Type': 'application/json',
//           },
//           body: JSON.stringify({ content: editContent }),
//         });
//         const data = await response.json();
//         setEditingNote(null);
//         setEditContent('');
//         fetchNotes();
//       } catch (error) {
//         console.error('Error updating note:', error);
//       }
//     }
//   };

//   const handleDeleteNote = async (id) => {
//     try {
//       await fetch(`notes/${id}`, {
//         method: 'DELETE',
//       });
//       fetchNotes();
//     } catch (error) {
//       console.error('Error deleting note:', error);
//     }
//   };

//   return (
//     <div>
//       <h1>Notes</h1>
//       <input
//         type="text"
//         value={newNote}
//         onChange={(e) => setNewNote(e.target.value)}
//         placeholder="Add a new note"
//       />
//       <button onClick={handleAddNote}>Add Note</button>
//       <ul>
//         {notes.map((note) => (
//           <li key={note.id}>
//             {editingNote === note.id ? (
//               <>
//                 <input
//                   type="text"
//                   value={editContent}
//                   onChange={(e) => setEditContent(e.target.value)}
//                 />
//                 <button onClick={() => handleUpdateNote(note.id)}>Save</button>
//                 <button onClick={() => setEditingNote(null)}>Cancel</button>
//               </>
//             ) : (
//               <>
//                 {note.content}
//                 <button onClick={() => {
//                   setEditingNote(note.id);
//                   setEditContent(note.content);
//                 }}>Edit</button>
//                 <button onClick={() => handleDeleteNote(note.id)}>Delete</button>
//               </>
//             )}
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// };
