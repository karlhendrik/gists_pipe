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

document.getElementById('gist-list').addEventListener('click', function(e){
    var gistID = e.target.dataset.id;
    var gistOwner = e.target.dataset.owner;

    fetch('http://localhost:8000/api/v1/deals', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: gistID + ' - ' + gistOwner,
            pipeline_id : 1,

        })
    }).then(function(response) {
        if (response.ok) {
            console.log('Deal created');
            return response.json();
        } else {
            throw new Error('Network response was not ok.');
        }
    }).then(function(data) {
        console.log(data);
    }).catch(function(error) {
        console.log('There has been a problem with your fetch operation: ' + error.message);
    });
});

function getGists(user) {
    // Create a request using fetch
    fetch('http://localhost:8000/api/v1/gists?username=' + user)
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
                data.forEach(function(gist) {
                    const gistID = gist.id;
                    const gistOwner = gist.owner.login;
                    const gistURL = gist.html_url;
                    const gistCreated = gist.created_at;
                    // const gistUpdated = gist.updated_at;
                    const gistFilename = gist.files[Object.keys(gist.files)[0]].filename;
                    const gistFileType = gist.files[Object.keys(gist.files)[0]].type;

                    
                    // TODO: from security perspective using innerHTML might not be the best idea..
                    document.getElementById('gist-list').innerHTML += '<tr> \
                    <td style="color: whitesmoke;" >' + gistFilename + '</td>' +
                    '<td style="color: whitesmoke;" >' + gistCreated  + '</td>' +
                    '<td style="color: whitesmoke;" >' + gistFileType  + '</td>' +
                    '<td>' + '<a class="btn btn-primary" href="' + gistURL + '" target=”_blank”>Open Gist</a>' +
                    '<td>' + '<a class="btn btn-success" href="#" data-id="'+gistID+'" data-owner="'+gistOwner+'">Create Deal</a>' +
                    '</tr>';
                });
            }
        }).catch(function(error) {
            console.log('There has been a problem with your fetch operation: ' + error.message);
        });

        
}
