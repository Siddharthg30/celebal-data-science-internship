document.addEventListener("DOMContentLoaded", () => {

    // --------------------------------------------------
    // ELEMENTS
    // --------------------------------------------------

    const brandInput = document.getElementById("brand");
    const modelInput = document.getElementById("model");
    const queryInput = document.getElementById("query");

    const askButton = document.getElementById("askButton");

    const loading = document.getElementById("loading");
    const answerContainer = document.getElementById("answer");
    const sourcesContainer = document.getElementById("sources");


    // --------------------------------------------------
    // INITIAL STATE
    // --------------------------------------------------

    loading.style.display = "none";


    // --------------------------------------------------
    // ASK DRIVEWISE
    // --------------------------------------------------

    askButton.addEventListener("click", async () => {

        const query = queryInput.value.trim();
        const brand = brandInput.value;
        const model = modelInput.value;


        // --------------------------------------------------
        // VALIDATION
        // --------------------------------------------------

        if (!query) {

            answerContainer.innerHTML = `
                <p>Please enter a question.</p>
            `;

            return;
        }


        // --------------------------------------------------
        // LOADING STATE
        // --------------------------------------------------

        askButton.disabled = true;
        askButton.textContent = "Thinking...";

        loading.style.display = "block";

        answerContainer.innerHTML = "";

        sourcesContainer.innerHTML = "";


        try {

            // --------------------------------------------------
            // CALL FLASK API
            // --------------------------------------------------

            const response = await fetch("/api/chat", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    query: query,
                    brand: brand,
                    model: model
                })

            });


            // --------------------------------------------------
            // READ RESPONSE
            // --------------------------------------------------

            const data = await response.json();


            // --------------------------------------------------
            // HANDLE ERROR
            // --------------------------------------------------

            if (!response.ok || !data.success) {

                throw new Error(
                    data.error || "Unable to get an answer."
                );

            }


            // --------------------------------------------------
            // DISPLAY ANSWER
            // --------------------------------------------------

            displayAnswer(data.answer);


            // --------------------------------------------------
            // DISPLAY SOURCES
            // --------------------------------------------------

            displaySources(data.sources);


        } catch (error) {

            console.error("DriveWise error:", error);

            answerContainer.innerHTML = `
                <div class="error-message">
                    <strong>Something went wrong.</strong>
                    <p>${escapeHtml(error.message)}</p>
                </div>
            `;

        } finally {

            // --------------------------------------------------
            // RESET UI
            // --------------------------------------------------

            loading.style.display = "none";

            askButton.disabled = false;
            askButton.textContent = "Ask DriveWise";

        }

    });


    // --------------------------------------------------
    // DISPLAY ANSWER
    // --------------------------------------------------

    function displayAnswer(answer) {

        if (!answer) {

            answerContainer.innerHTML = `
                <p>No answer was generated.</p>
            `;

            return;
        }


        let formattedAnswer = escapeHtml(answer);


        // ----------------------------------------------
        // BOLD MARKDOWN
        // ----------------------------------------------

        formattedAnswer = formattedAnswer.replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        );


        // ----------------------------------------------
        // BULLET POINTS
        // ----------------------------------------------

        formattedAnswer = formattedAnswer.replace(
            /^- (.*)$/gm,
            "<li>$1</li>"
        );


        // ----------------------------------------------
        // WRAP LIST ITEMS
        // ----------------------------------------------

        formattedAnswer = formattedAnswer.replace(
            /(<li>.*?<\/li>)(\s*<li>.*?<\/li>)*/gs,
            "<ul>$&</ul>"
        );


        // ----------------------------------------------
        // NEW LINES
        // ----------------------------------------------

        formattedAnswer = formattedAnswer.replace(
            /\n/g,
            "<br>"
        );


        answerContainer.innerHTML = `
            <div class="answer-content">
                ${formattedAnswer}
            </div>
        `;

    }


    // --------------------------------------------------
    // DISPLAY SOURCES
    // --------------------------------------------------

    function displaySources(sources) {

        if (!sources || sources.length === 0) {

            sourcesContainer.innerHTML = "";

            return;
        }


        let html = `
            <div class="sources-title">
                Sources
            </div>

            <div class="sources-list">
        `;


        sources.forEach((source, index) => {

            const section =
                source.section || "Document";

            const page =
                source.page_number ?? "N/A";


            html += `
                <div class="source-card">

                    <div class="source-number">
                        ${index + 1}
                    </div>

                    <div class="source-info">

                        <strong>
                            ${escapeHtml(section)}
                        </strong>

                        <span>
                            Page ${escapeHtml(String(page))}
                        </span>

                    </div>

                </div>
            `;

        });


        html += `
            </div>
        `;


        sourcesContainer.innerHTML = html;

    }


    // --------------------------------------------------
    // ESCAPE HTML
    // --------------------------------------------------

    function escapeHtml(value) {

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");

    }

});