// Load button when page loads
window.onload = getUserGists;

function getUserGists(){
    document.getElementById('gist-submit').addEventListener('click', function(e) {
        e.preventDefault();
        let user = document.getElementById('gist-input').value;
        if (user) {
            getGists(user);
        } else {
            document.getElementById('alert-username').style.display = 'block';
        }

    });
}

function getGists(user) {
    // Create a request using fetch
    fetch('http://localhost:8000/gists?username=' + user)
       // If Array is empty show error message
        .then(function(response) {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Network response was not ok.');
            }
        }).then(function(data) {
            if (data.length === 0) {
                document.getElementById('alert-no-gists').style.display = 'block';
            } else {
                document.getElementById('alert-username').style.display = 'none';
                document.getElementById('gist-list').innerHTML = '';
                console.log(data);
                data.forEach(function(gist) {
                    // const gistID = gist.id;
                    // const gistOwner = gist.owner.login;
                    const gistURL = gist.html_url;
                    const gistCreated = gist.created_at;
                    // const gistUpdated = gist.updated_at;
                    const gistFilename = gist.files[Object.keys(gist.files)[0]].filename;
                    const gistFileType = gist.files[Object.keys(gist.files)[0]].type;
                    
                    // Add gist to DOM list
                    document.getElementById('gist-list').innerHTML += '<tr> \
                        <td style="color: whitesmoke;" >' + gistFilename + '</td>' + 
                        '<td style="color: whitesmoke;" >' + gistCreated  + '</td>' + 
                        '<td style="color: whitesmoke;" >' + gistFileType  + '</td>' + 
                        '<td>' + '<a class="btn btn-primary" href="' + gistURL + '" target=”_blank”>Open Gist</a>' +
                        '<td>' + '<a class="btn btn-success" href="' + gistURL + '">Add to Pipe</a>' + 
                    '</tr>';
                });
            }
        }).catch(function(error) {
            console.log('There has been a problem with your fetch operation: ' + error.message);
        });
}
