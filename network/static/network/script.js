document.addEventListener('DOMContentLoaded', function() {
    console.log("HELLO!");
    const editButtons = document.getElementsByClassName("edit");
    for (let i=0; i<editButtons.length; i++) {
        editButtons[i].addEventListener('click', function() {
            id = this.id;
            const textBox = document.getElementById("edit"+id);
            textBox.removeAttribute("hidden");
            const content = document.getElementById("content"+id);
            content.setAttribute("hidden", "true");
        });
    }
    
    const likeButtons = document.getElementsByClassName("like-button");
    for (let i=0; i<likeButtons.length; i++) {
        likeButtons[i].addEventListener('click', function() {

            const action = likeButtons[i].getAttribute("action-type");
            const postId = parseInt(likeButtons[i].getAttribute("post-id"));

            fetch(`/update-like/${action}/${postId}`)
                .then((response) => response.json())
                .then((data) => {
                    console.log(data)
                    const action = data.action;
                    const likes = data.likes;
                    var likeCounter = document.getElementById("likeCount"+postId);
                    likeCounter.innerHTML = likes + " Likes";
                    
                })
                .catch((error) => console.log(error));


        })
        /*
        likeButtons[i].addEventListener('click', function() {
            const postId = parseInt(likeButtons[i].getAttribute("post-id"));
            const action = likeButtons[i].getAttribute("action-type");
            fetch(`/update-like/${action}/${postId}/`)
                .then((response) => response.json())
                .then((data) => {
                    const status = data.action;
                    const likes = data.likes;
                    console.log(status);
                    if (status === "like")
                    {
                        var likeCounter = document.getElementById("likeCount"+postId);
                        likeCounter.innerHTML = likes.toString() + " Likes";
                    }
                    else if (status === "unlike")
                    {
                        var likeCounter = document.getElementById("likeCount"+postId);
                        likeCounter.innerHTML = likes.toString() + " Likes";
                    }
                })
                .catch((error) => console.log(error));
            
        })
        */
    }
    
});
    
