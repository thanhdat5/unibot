// API Configuration
const API_BASE_URL = 'http://localhost:8000'; // Change to your API URL
const STREAM_ENDPOINT = `${API_BASE_URL}/chat/stream`;

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const chatForm = document.getElementById('chatForm');
const sendBtn = document.getElementById('sendBtn');

// State
let isLoading = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    chatForm.addEventListener('submit', handleSendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
            handleSendMessage(e);
        }
    });
});

/**
 * Handle sending message
 */
async function handleSendMessage(e) {
    e.preventDefault();
    
    const question = messageInput.value.trim();
    if (!question) return;
    
    // Add user message to chat
    addMessageToChat(question, 'user');
    messageInput.value = '';
    
    // Disable send button
    isLoading = true;
    sendBtn.disabled = true;
    
    // Create bot message container
    const botMessageElement = createBotMessageElement();
    chatMessages.appendChild(botMessageElement);
    
    try {
        await streamChatResponse(question, botMessageElement);
    } catch (error) {
        console.error('Error:', error);
        botMessageElement.querySelector('.message-content p').innerHTML = 
            `❌ Đã xảy ra lỗi: ${error.message}`;
    } finally {
        isLoading = false;
        sendBtn.disabled = false;
        messageInput.focus();
    }
}

/**
 * Stream chat response from API
 */
async function streamChatResponse(question, botMessageElement) {
    const contentElement = botMessageElement.querySelector('.message-content p');
    let fullResponse = '';
    let isFirstToken = true;
    
    try {
        const response = await fetch(STREAM_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        while (true) {
            const { done, value } = await reader.read();
            
            if (done) break;
            
            // Decode chunk
            const chunk = decoder.decode(value, { stream: true });
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.slice(6));
                        console.log('Received:', data);
                        
                        if (data.done) {
                            // Streaming complete
                            break;
                        } else if (data.error) {
                            contentElement.innerHTML = `❌ Error: ${data.error}`;
                            break;
                        } else if (data.documents && data.documents.length > 0) {
                            // Display retrieved documents
                            displayRetrievedDocuments(data.documents);
                        } else if (data.token) {
                            // Clear loading indicator on first token
                            if (isFirstToken) {
                                contentElement.innerHTML = '';
                                isFirstToken = false;
                            }
                            
                            fullResponse += data.token;
                            contentElement.textContent = fullResponse;
                            
                            // Auto-scroll to bottom
                            chatMessages.scrollTop = chatMessages.scrollHeight;
                        }
                    } catch (e) {
                        // Invalid JSON, skip
                        console.log('Invalid JSON:', line);
                    }
                }
            }
        }
        
        // Format and display final response
        if (fullResponse) {
            contentElement.innerHTML = formatResponse(fullResponse);
        }
        
    } catch (error) {
        contentElement.innerHTML = `❌ Lỗi kết nối: ${error.message}`;
        console.error('Stream error:', error);
    }
    
    // Update timestamp
    botMessageElement.querySelector('.message-time').textContent = getCurrentTime();
    
    // Auto-scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Add message to chat UI
 */
function addMessageToChat(text, sender = 'user') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const p = document.createElement('p');
    p.textContent = text;
    contentDiv.appendChild(p);
    
    messageDiv.appendChild(contentDiv);
    
    const timeSpan = document.createElement('span');
    timeSpan.className = 'message-time';
    timeSpan.textContent = getCurrentTime();
    messageDiv.appendChild(timeSpan);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageDiv;
}

/**
 * Create bot message element with loading state
 */
function createBotMessageElement() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const p = document.createElement('p');
    p.innerHTML = '<div class="loading"><div class="loading-dot"></div><div class="loading-dot"></div><div class="loading-dot"></div></div>';
    contentDiv.appendChild(p);
    
    messageDiv.appendChild(contentDiv);
    
    const timeSpan = document.createElement('span');
    timeSpan.className = 'message-time';
    timeSpan.textContent = 'Đang xử lý...';
    messageDiv.appendChild(timeSpan);
    
    return messageDiv;
}

/**
 * Format response text with basic markdown-like support
 */
function formatResponse(text) {
    // Escape HTML
    let formatted = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    
    // Convert line breaks
    formatted = formatted.replace(/\n/g, '<br>');
    
    // Convert URLs to links
    formatted = formatted.replace(
        /https?:\/\/[^\s]+/g,
        url => `<a href="${url}" target="_blank" style="color: #667eea; text-decoration: underline;">${url}</a>`
    );
    
    return formatted;
}

/**
 * Get current time formatted
 */
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('vi-VN', { 
        hour: '2-digit', 
        minute: '2-digit'
    });
}

/**
 * Ask a quick question
 */
function askQuestion(question) {
    messageInput.value = question;
    messageInput.focus();
    // Auto-submit after a short delay
    setTimeout(() => {
        chatForm.dispatchEvent(new Event('submit'));
    }, 100);
}

/**
 * Display retrieved documents
 */
function displayRetrievedDocuments(documents) {
    const docsContainer = document.getElementById('retrievedDocs');
    const docsList = document.getElementById('docsList');
    
    if (!documents || documents.length === 0) {
        if (docsContainer) docsContainer.style.display = 'none';
        return;
    }
    
    if (!docsContainer || !docsList) {
        console.warn('Documents container or list not found in DOM');
        return;
    }
    
    docsList.innerHTML = documents
        .map(doc => `
            <div class="doc-item">
                <span class="doc-name">${doc.filename}</span>
                <a href="${API_BASE_URL}/upload/documents/${encodeURIComponent(doc.filename)}" 
                   class="doc-download-link" 
                   download>
                    ⬇ Download
                </a>
            </div>
        `)
        .join('');
    
    docsContainer.style.display = 'block';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
