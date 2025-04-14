async function askQuestion() {
    const questionInput = document.getElementById("question");
    const chatMessages = document.getElementById("chat-messages");
    const question = questionInput.value.trim();
    


    if (!question) {
        return alert("Please enter a question.");
    }

    const userMessage = document.createElement("div");
    userMessage.className = "chat-message user";
    userMessage.textContent = question;
    chatMessages.appendChild(userMessage);

    questionInput.value = "";

    const typingIndicator = document.createElement("div");
    typingIndicator.className = "chat-message bot typing";
    typingIndicator.textContent = "Typing...";
    chatMessages.appendChild(typingIndicator);

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question }),
        });
    
        const data = await response.json();
        
        console.log("API Response:", data); // <-- ADD THIS LINE TO DEBUG
        
        chatMessages.removeChild(typingIndicator);
    

        let answerText = formatResponse(data.answer);

        const botMessage = document.createElement("div");
        botMessage.className = "chat-message bot";
        botMessage.innerHTML = answerText;
        chatMessages.appendChild(botMessage);

    } catch (error) {
        console.error("Error fetching response:", error);
        chatMessages.removeChild(typingIndicator);

        const errorMessage = document.createElement("div");
        errorMessage.className = "chat-message bot";
        errorMessage.textContent = "Sorry, something went wrong. Please try again.";
        chatMessages.appendChild(errorMessage);
    }

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatResponse(response) {
    if (!response) {
        return "I couldn't find an answer to that.";
    }

    if (typeof response === "object") {
        let formattedText = "<strong>Details:</strong><br>";

        Object.entries(response).forEach(([key, value]) => {
            if (typeof value === "object" && !Array.isArray(value)) {
                formattedText += `<strong>${capitalize(key)}:</strong><br>`;
                Object.entries(value).forEach(([subKey, subValue]) => {
                    if (Array.isArray(subValue)) {
                        formattedText += `&nbsp;&nbsp;- <strong>${capitalize(subKey)}:</strong> ${subValue.join(", ")}<br>`;
                    } else {
                        formattedText += `&nbsp;&nbsp;- <strong>${capitalize(subKey)}:</strong> ${subValue}<br>`;
                    }
                });
            } else {
                formattedText += `<strong>${capitalize(key)}:</strong> ${value}<br>`;
            }
        });

        return formattedText;
    }

    return response;
}

function capitalize(str) {
    return str.replace(/_/g, " ").replace(/\b\w/g, char => char.toUpperCase());
}
