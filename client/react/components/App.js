import React, { useState, useEffect } from 'react';
import {handleAddUser,handleDeleteUser} from './api_calls'
export const  App = () => {

    const [page,setPage] = useState('default')
    const [name,setName] = useState('')
    const [email,setEmail] = useState('')



    if (page==='default') {

      return (
          <div>
            <h1>Welcome to the DB Management Screen</h1>

            <button onClick={(e) => setPage('addUser')}>Add User</button>
            <button onClick={(e) => setPage('deleteUser')}>Delete User</button>
            <button onClick={(e) => setPage('findUser')}>Find User</button>
            <button onClick={(e) => setPage('listUsers')}>List All Users</button>

          </div>
      )
    }
    else if (page==='addUser'){
        return (
            <div>
                <form onSubmit={(e) => handleAddUser(e,name,email)}>
                    <input type="text" onChange={(e) => setName(e.target.value)} placeholder='name'/>
                    <input type="text" onChange={(e) => setEmail(e.target.value)} placeholder='email'/>
                    <input type='submit' value='Submit User'></input>
                </form>

                <button onClick={(e)=>setPage('default')}>Go Back</button>
            </div>
        )
    }

    else if (page==='deleteUser'){
        return (
            <div>
                <form onSubmit={(e) => handleDeleteUser(e,email)}>
                    <input type="text" onChange={(e) => setEmail(e.target.value)} placeholder='email'/>
                    <input type='submit' value='Delete User'></input>
                </form>
                <button onClick={(e)=>setPage('default')}>Go Back</button>
            </div>
        )
    }

    else if (page==='findUser'){

    }
    else if (page==='listUsers'){

    }
}



// Set the default appearance