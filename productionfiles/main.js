document.addEventListener('DOMContentLoaded', () => {
    const chatItemBox = document.querySelector('.chat-item-box');
    const newChatBtn = document.getElementById('new-chat');
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    const messageList = document.querySelector('.message-list'); // ul chứa message của user và chatbot
    const messageForm = document.querySelector('.message-form'); // form để gửi message 
    const messageInput = document.querySelector('.message-input'); // input dùng để nhập message

    let chatId = messageInput.dataset.id;

    loadChats();

    messageForm.addEventListener('submit', (e) => {
        e.preventDefault(); // ngăn ngừa sự kiện mặc định: sự kiện load lại trang

        const message = messageInput.value.trim(); // lấy input của user và loại bỏ khoảng trắng đầu và cuối
    
        if (message.length === 0) {
            return;  // nếu người dùng không nhập vào
        }

        const messageItem = document.createElement('li');
        messageItem.classList.add('message', 'message-sent');
        messageItem.innerHTML = `
            <div class="message-text">
                <div class="message-sender">
                    <b>You</b>    
                </div>
                <div class="message-content">
                    ${message}    
                </div>
            </div>
        `; 
        messageList.appendChild(messageItem);

        messageInput.value = ''; 

        chatId = messageInput.dataset.id;

        // url để xác định tạo chat mới hay add message vào chat cũ
        const url = chatId ? `/api/chat/${chatId}/add-messag/` : '/api/chat/create/'; // sự kiện 2 tạo chat

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(message)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);

            // set attibute cho input bằng chat_id
            messageInput.setAttribute('data-id', data.chat_id);
            const response = data.answer_question;

            const messageItem = document.createElement('li');
            messageItem.classList.add('message', 'message-received');
            messageItem.innerHTML = `
                <div class="message-text">
                    <div class="message-sender">
                        <b>AI Chatbot</b>    
                    </div>
                    <div class="message-content">
                        ${response}    
                    </div>
                </div>
            `;
            messageList.appendChild(messageItem);
            chatItemBox.innerHTML = '';
            loadChats();        
        })
        .catch(error => console.error(error));
    });

    newChatBtn.addEventListener('click', () => {
        fetch('/chat/create/')   // 1 sự kiện gọi tạo chat
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            chatItemBox.innerHTML = '';
            loadChats();
            messageInput.value = '';

            // add data-id vào messageInput
            messageInput.setAttribute('data-id', data.chat_id);

            // xóa bỏ các message tại message list
            messageList.innerHTML = '';
            messageInput.focus();
        })
        .catch(error => console.error(error));
    });

    function loadChats() {
        fetch('/chat/load/')
        .then(response => response.json())
        .then(data => {
            //console.log(data.chats);
            const chats = data.chats;

            const ulItem = document.createElement('ul');
            chats.forEach(chat => {
                const liItem = document.createElement('li');
                const chatTitle = document.createElement('div');
                chatTitle.classList.add('chat-item-title');
                chatTitle.textContent = chat.name;

                // retrive chat
                chatTitle.addEventListener('click', () => {
                    const idChatRetrive = chat.id;
                    retriveChatFunction(idChatRetrive);
                });

                const deleteChatBtn = document.createElement('div');
                deleteChatBtn.classList.add('delete-chat-btn');
                deleteChatBtn.innerHTML = `<i class="fa-solid fa-trash-can"></i>`;

                deleteChatBtn.addEventListener('click', () => {
                    const idChatDelete = chat.id;
                    deleteChatFunction(idChatDelete, liItem);
                });

                liItem.appendChild(chatTitle);
                liItem.appendChild(deleteChatBtn);

                ulItem.appendChild(liItem);
            });

            chatItemBox.appendChild(ulItem);
        })
        .catch(error => console.error(error));
    }


    function retriveChatFunction(chatId) {
        fetch(`/chat/retrive/${chatId}/`, {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            // console.log(data.messages);
            messages_ = data.messages;
            messageInput.value = '';

            // add data-id vào messageInput
            messageInput.setAttribute('data-id', chatId);
            
            // xóa bỏ các message tại message list
            messageList.innerHTML = '';

            messages_.forEach(message => {
                const messageItemSent = document.createElement('li');
                messageItemSent.classList.add('message', 'message-sent');
                messageItemSent.innerHTML = `
                    <div class="message-text">
                        <div class="message-sender">
                            <b>You</b>    
                        </div>
                        <div class="message-content">
                            ${message.question}    
                        </div>
                    </div>
                `; 
                messageList.appendChild(messageItemSent);

                const messageItemReceived = document.createElement('li');
                messageItemReceived.classList.add('message', 'message-received');
                messageItemReceived.innerHTML = `
                    <div class="message-text">
                        <div class="message-sender">
                            <b>AI Chatbot</b>    
                        </div>
                        <div class="message-content">
                            ${message.answer}    
                        </div>
                    </div>
                `;
                messageList.appendChild(messageItemReceived);
            });

        })
        .catch(error => console.error(error));
    }

    
    function deleteChatFunction(chatId, Item) {
        fetch(`/chat/delete/${chatId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            Item.remove();
        })
        .catch(error => console.error(error));
    }

});