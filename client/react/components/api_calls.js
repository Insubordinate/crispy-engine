const handleGetUser = ({userEvent,email,dataFunc,pageFunc}) => {
    userEvent.preventDefault()

    if (email === null) {
        fetch('http://127.0.0.1:5000/user', {
            method: 'GET',
        })
            .then((res) => res.json())
            .then((data) => {
                console.log(data)
                dataFunc(data)
                pageFunc('displayAllUsers')
            })
            .catch((err) => console.error(err))
    }
    else {
        fetch('http://127.0.0.1:5000/user?'+`email=${email}`,{
            method:'GET',
        })
        .then((res)=>res.json())
        .then((data)=>{
                console.log(data)
                if(data.status =='failure'){
                    dataFunc(data)
                    pageFunc('errorPage')
                }
                else{
                    dataFunc(data)
                    pageFunc('displayUser')
                }

        })
        .catch((err)=>console.error(err))
    }


}
const handleAddUser = ({userEvent,email,name,dataFunc,pageFunc}) => {
    userEvent.preventDefault()
        fetch('http://127.0.0.1:5000/user?'+`email=${email}`+`&name=${name}`,{
            method:'POST',
        })
        .then((res)=>res.json())
        .then((data)=>{
                console.log(data)
                if(data.status =='failure'){
                    dataFunc(data)
                    pageFunc('errorPage')
                }
                else{
                    dataFunc(data)
                    pageFunc('displayUserSuccess')
                }

        })
        .catch((err)=>console.error(err))
}

const handleDeleteUser = ({userEvent,email,dataFunc,pageFunc}) => {
    userEvent.preventDefault()
    fetch('http://127.0.0.1:5000/user?'+`email=${email}`,{
        method:'DELETE',
        })
        .then((res)=>res.json())
        .then((data)=>{
                console.log(data)
                if(data.status =='failure'){
                    dataFunc(data)
                    pageFunc('errorPage')
                }
                else{
                    dataFunc(data)
                    pageFunc('displayUserDeleteSuccess')
                }
        })
        .catch((err)=>console.error(err))


}


const handleUpdateUser = ({userEvent,email,name,newName,newEmail,dataFunc,pageFunc}) => {
    userEvent.preventDefault()
    fetch('http://127.0.0.1:5000/user?'+`email=${email}`+`&name=${name}`+`&newName=${newName}`+`&newEmail=${newEmail}`,{
        method:'PUT',
        })
        .then((res)=>res.json())
        .then((data)=>{
                console.log(data)
                if(data.status =='failure'){
                    dataFunc(data)
                    pageFunc('errorPage')
                }
                else{
                    dataFunc(data)
                    pageFunc('displayUserEditSuccess')
                }

        })
        .catch((err)=>console.error(err))
}



module.exports = {handleAddUser,handleDeleteUser,handleGetUser,handleUpdateUser}