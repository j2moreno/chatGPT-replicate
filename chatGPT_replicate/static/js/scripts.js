document.addEventListener('DOMContentLoaded', (event) => {
    var input = document.getElementById('userInput');
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault(); // Prevent the default action to avoid submitting a form if there is one
            sendMessage();
        }
    });
});
document.addEventListener('DOMContentLoaded', function() {
    // Attach click event listeners to all conversation items
    document.querySelectorAll('.sidebar ul li').forEach(item => {
        item.addEventListener('click', function(event) {
            // Prevent the default action if necessary
            // event.preventDefault();

            // Clear the active class from all conversation items
            document.querySelectorAll('.sidebar ul li').forEach(innerItem => {
                innerItem.classList.remove('active-conversation');
            });

            // Set the clicked item as the active conversation
            this.classList.add('active-conversation');

            const conversationId = this.getAttribute('id').split('_')[1];
            console.log('Selected Conversation ID:', conversationId);
        });
    });
});

function sendMessage() {
    var input = document.getElementById('userInput');
    var conversationId = document.getElementById('conversationId').value; // Get the conversation ID
    var message = input.value.trim();
    if (!message) return;

    displayMessage(message, 'user-message');

    fetch('/chatGPT/chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({message: message, conversation_id: conversationId})
    })
    .then(response => response.json())
    .then(data => displayMessage(data.reply, 'bot-message'))
    .catch(error => console.error('Error:', error));

    input.value = ''; // Clear input after sending
}

function displayMessage(content, className) {
    var chatbox = document.getElementById('messages');
    
    var messageDiv = document.createElement('div');
    messageDiv.className = className;
    
    var senderLabel = document.createElement('div'); // Use 'div' to ensure it's on a new line
    senderLabel.className = 'sender-info'; // Add a class for styling
    if (className.includes('user-message')) {
        senderLabel.textContent = 'User: ';
        senderLabel.classList.add('user-sender'); // Add specific class for user
    } else {
        senderLabel.textContent = 'GPT4: ';
        senderLabel.classList.add('gpt4-sender'); // Add specific class for bot
    }
    messageDiv.appendChild(senderLabel);

    var messageContent = document.createElement('div'); // Also 'div' to be block-level by default
    messageContent.className = 'message-content'; // Add a class for additional styling

    const parts = content.split(/```(.*?)```/s);
    parts.forEach((part, index) => {
        if (index % 2 === 0) {
            // Text part
            var textDiv = document.createElement('div');
            textDiv.textContent = part.trim();
            messageContent.appendChild(textDiv);
        } else {
            // Code block part
            var pre = document.createElement('pre');
            var code = document.createElement('code');
            pre.className = 'code-block';
            code.textContent = part.trim();
            pre.appendChild(code);
            messageContent.appendChild(pre);
        }
    });
    
    messageDiv.appendChild(messageContent);

    // Append the message container to the chatbox
    chatbox.appendChild(messageDiv);

    // Scroll to the newest message
    chatbox.scrollTop = chatbox.scrollHeight;
}

function createConversation() {
    fetch('/chatGPT/create_conversation/', {
        method: 'POST',
        headers: {
            // Add any necessary headers
            'X-CSRFToken': getCookie('csrftoken'), // Handling CSRF token
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            // Any necessary body data
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === 'success') {
            // Update the conversation list
            addConversationToList(data.conversation_id, data.created_at);
        } else {
            // Handle any errors
            console.error('Error creating conversation');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Helper function to add the new conversation to the list
function addConversationToList(conversationId, created_at) {
    const date = new Date(created_at);

    // Format the date - "MM/DD/YYYY, HH:MM AM/PM"
    const formattedDate = formatDate(date);

    const conversationsList = document.querySelector('.sidebar ul');
    const newListItem = document.createElement('li');
    newListItem.innerHTML = `<a href="?conversation_id=${conversationId}">Conversation at ${formattedDate}</a>`;
    // conversationsList.appendChild(newListItem);
    conversationsList.insertBefore(newListItem, conversationsList.firstChild); // To add at the top
}
// Helper function to format date in MM/DD/YYYY, HH:MM AM/PM format
function formatDate(date) {
    const pad = (num) => (num < 10 ? '0' + num : num);
    const hours = date.getHours();
    const minutes = date.getMinutes();
    const ampm = hours >= 12 ? 'p.m.' : 'a.m.';
    const hoursFormatted = hours % 12 || 12; // Convert to 12-hour format and handle 0 as 12
    return (pad(date.getMonth() + 1)) + '/' + 
        pad(date.getDate()) + '/' + 
        date.getFullYear() + ' ' + 
        pad(hoursFormatted) + ':' + 
        pad(minutes) + ' ' + 
        ampm;
}

function deleteConversation(conversationId) {
    if (!confirm("Are you sure you want to delete this conversation?")) {
        return; // Stop if the user cancels the action
    }
    fetch(`/chatGPT/delete_conversation/${conversationId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.redirect_url);
        if (data.success) {
            // Remove the conversation element from the DOM
            // document.querySelector(`#conversation_${conversationId}`).remove();
            window.location.href = data.redirect_url;

        } else {
            alert('Error deleting conversation');
        }
    })
    .catch(error => console.error('Error:', error));
}
