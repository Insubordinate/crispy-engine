const handleAddUser = (e,name,email) => {
    e.preventDefault()

    fetch('http://127.0.0.1:5000/user',{
        method:'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
        body:JSON.stringify({name:name,email:email})
    })

    .then((res)=>res.json())
    .then((data)=>{console.log(data)})
    .catch((err)=>console.error(err))
}

const handleDeleteUser = (e,email) => {
    e.preventDefault()

    fetch('http://127.0.0.1:5000/user',{
        method:'DELETE',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
        body:JSON.stringify({email:email})
    })

    .then((res)=>res.json())
    .then((data)=>{console.log(data)})
    .catch((err)=>console.error(err))
}


module.exports = {handleAddUser,handleDeleteUser}