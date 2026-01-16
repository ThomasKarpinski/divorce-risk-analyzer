import os

questions = [
    "1. When one of our apologies apologizes when our discussions go in a bad direction, the issue does not extend.",
    "2. I know we can ignore our differences, even if things get hard sometimes.",
    "3. When we need it, we can take our discussions with my wife from the beginning and correct it.",
    "4. When I argue with my wife, it will eventually work for me to contact him.",
    "5. The time I spent with my wife is special for us.",
    "6. We don't have time at home as partners.",
    "7. We are like two strangers who share the same environment at home rather than family.",
    "8. I enjoy our holidays with my wife.",
    "9. I enjoy traveling with my wife.",
    "10. My wife and most of our goals are common.",
    "11. I think that one day in the future, when I look back, I see that my wife and I are in harmony with each other.",
    "12. My wife and I have similar values in terms of personal freedom.",
    "13. My husband and I have similar entertainment.",
    "14. Most of our goals for people (children, friends, etc.) are the same.",
    "15. Our dreams of living with my wife are similar and harmonious",
    "16. We're compatible with my wife about what love should be",
    "17. We share the same views with my wife about being happy in your life",
    "18. My wife and I have similar ideas about how marriage should be",
    "19. My wife and I have similar ideas about how roles should be in marriage",
    "20. My wife and I have similar values in trust",
    "21. I know exactly what my wife likes.",
    "22. I know how my wife wants to be taken care of when she's sick.",
    "23. I know my wife's favorite food.",
    "24. I can tell you what kind of stress my wife is facing in her life.",
    "25. I have knowledge of my wife's inner world.",
    "26. I know my wife's basic concerns.",
    "27. I know what my wife's current sources of stress are.",
    "28. I know my wife's hopes and wishes.",
    "29. I know my wife very well.",
    "30. I know my wife's friends and their social relationships.",
    "31. I feel aggressive when I argue with my wife.",
    "32. When discussing with my wife, I usually use expressions such as \"you always\" or \"you never\".",
    "33. I can use negative statements about my wife's personality during our discussions.",
    "34. I can use offensive expressions during our discussions.",
    "35. I can insult our discussions.",
    "36. I can be humiliating when we argue.",
    "37. My argument with my wife is not calm.",
    "38. I hate my wife's way of bringing it up.",
    "39. Fights often occur suddenly.",
    "40. We're just starting a fight before I know what's going on.",
    "41. When I talk to my wife about something, my calm suddenly breaks.",
    "42. When I argue with my wife, it only snaps in and I don't say a word.",
    "43. I'm mostly thirsty to calm the environment a little bit.",
    "44. Sometimes I think it's good for me to leave home for a while.",
    "45. I'd rather stay silent than argue with my wife.",
    "46. Even if I'm right in the argument, I'm thirsty not to upset the other side.",
    "47. When I argue with my wife, I remain silent because I am afraid of not being able to control my anger.",
    "48. I feel right in our discussions.",
    "49. I have nothing to do with what I've been accused of.",
    "50. I'm not actually the one who's guilty about what I'm accused of.",
    "51. I'm not the one who's wrong about problems at home.",
    "52. I wouldn't hesitate to tell her about my wife's inadequacy.",
    "53. When I discuss it, I remind her of my wife's inadequate issues.",
    "54. I'm not afraid to tell her about my wife's incompetence."
]

html_head = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Divorce Risk Survey</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }

        header {
            background-color: #ff6b81;
            color: white;
            padding: 1.5rem;
            text-align: center;
        }

        main {
            max-width: 900px;
            margin: 2rem auto;
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        h1 {
            margin-top: 0;
        }

        .question {
            margin-bottom: 2rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid #eee;
        }

        .question label.q-text {
            display: block;
            margin-bottom: 1rem;
            font-weight: bold;
            line-height: 1.4;
            font-size: 1.1rem;
        }

        .radio-group {
            display: flex;
            justify-content: space-between;
            max-width: 500px;
            margin-bottom: 1rem;
        }

        .radio-option {
            display: flex;
            flex-direction: column;
            align-items: center;
            cursor: pointer;
            font-size: 0.9rem;
            color: #666;
        }

        .radio-option input {
            margin-bottom: 0.5rem;
            width: 1.2rem;
            height: 1.2rem;
            accent-color: #ff6b81;
            cursor: pointer;
        }

        .radio-labels {
            display: flex;
            justify-content: space-between;
            max-width: 500px;
            font-size: 0.8rem;
            color: #888;
            margin-top: -0.5rem;
            margin-bottom: 1rem;
        }

        /* Pagination Styles */
        .page {
            display: none;
        }
        .page.active {
            display: block;
            animation: fadeIn 0.5s;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .nav-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 2rem;
        }

        button {
            background-color: #ff6b81;
            color: white;
            border: none;
            padding: 1rem 2.5rem;
            border-radius: 50px;
            cursor: pointer;
            font-size: 1.1rem;
            font-weight: bold;
            transition: 0.3s;
        }

        button:hover {
            background-color: rgb(238, 10, 67);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(238, 10, 67, 0.3);
        }

        button:disabled {
            background-color: #ccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        .stat-feedback {
            display: block;
            margin-top: 0.5rem;
            font-size: 0.9rem;
            color: #ff6b81;
            font-weight: bold;
            opacity: 0;
            transition: opacity 0.5s ease;
        }
        .stat-feedback.visible {
            opacity: 1;
        }
    </style>
</head>
<body>

    <header>
        <h1>Divorce Risk Survey</h1>
        <p>Scale: 0 (Strongly Disagree) to 4 (Strongly Agree)</p>
    </header>

    <main>
        <form action="{% url 'result' %}" method="POST" id="surveyForm">
            {% csrf_token %}
            
            <div id="questions-container">
"""

html_tail = """            </div>

            <!-- Navigation Buttons -->
            <div class="nav-buttons">
                <button type="button" id="prevBtn" onclick="changePage(-1)">Previous</button>
                <span id="pageIndicator" style="align-self: center; font-weight: bold; color: #555;">Page 1 of 18</span>
                <button type="button" id="nextBtn" onclick="changePage(1)">Next</button>
                <button type="submit" id="submitBtn" style="display: none;">Submit Survey</button>
            </div>

        </form>
    </main>

    <script>
        let currentPage = 0;
        const questionsPerPage = 3;
        let pages = [];

        document.addEventListener('DOMContentLoaded', function() {
            const form = document.getElementById('surveyForm');
            const questions = Array.from(document.querySelectorAll('.question'));
            const totalQuestions = questions.length;
            const totalPages = Math.ceil(totalQuestions / questionsPerPage);
            
            for (let i = 0; i < totalPages; i++) {
                const pageDiv = document.createElement('div');
                pageDiv.className = 'page';
                if (i === 0) pageDiv.classList.add('active');
                
                for (let j = 0; j < questionsPerPage; j++) {
                    const qIndex = i * questionsPerPage + j;
                    if (qIndex < totalQuestions) {
                        pageDiv.appendChild(questions[qIndex]);
                    }
                }
                
                form.insertBefore(pageDiv, document.querySelector('.nav-buttons'));
                pages.push(pageDiv);
            }
            
            updateButtons();

            const isAuthenticated = "{{ user.is_authenticated|yesno:'true,false' }}" === "true";
            
            if (isAuthenticated) {
                document.querySelectorAll('input[type="radio"]').forEach(radio => {
                    radio.addEventListener('change', function() {
                        const questionId = this.name;
                        const answerValue = this.value;
                        const span = document.getElementById('stat-' + questionId);

                        fetch(`/api/stats/?question_id=${questionId}&answer_value=${answerValue}`)
                            .then(response => response.json())
                            .then(data => {
                                if (data.message) {
                                    span.textContent = data.message;
                                    span.classList.add('visible');
                                }
                            })
                            .catch(error => console.error('Error:', error));
                    });
                });
            }
        });

        function changePage(step) {
            if (step === 1 && !validatePage(currentPage)) {
                alert("Please answer all questions on this page.");
                return;
            }

            pages[currentPage].classList.remove('active');
            currentPage += step;
            pages[currentPage].classList.add('active');
            
            updateButtons();
            window.scrollTo(0, 0);
        }

        function updateButtons() {
            const prevBtn = document.getElementById('prevBtn');
            const nextBtn = document.getElementById('nextBtn');
            const submitBtn = document.getElementById('submitBtn');
            const pageIndicator = document.getElementById('pageIndicator');
            
            pageIndicator.textContent = `Page ${currentPage + 1} of ${pages.length}`;
            prevBtn.style.visibility = (currentPage === 0) ? 'hidden' : 'visible';

            if (currentPage === pages.length - 1) {
                nextBtn.style.display = 'none';
                submitBtn.style.display = 'block';
            } else {
                nextBtn.style.display = 'block';
                submitBtn.style.display = 'none';
            }
        }

        function validatePage(pageIndex) {
            const page = pages[pageIndex];
            const groups = new Set();
            page.querySelectorAll('input[type="radio"]').forEach(input => groups.add(input.name));
            
            for (let name of groups) {
                if (!page.querySelector(`input[name="${name}"]:checked`)) {
                    return false;
                }
            }
            return true;
        }
    </script>
</body>
</html>
"""

def generate_questions_html():
    q_html = ""
    for i, q_text in enumerate(questions):
        q_num = i + 1
        q_block = f"""
    <div class="question">
        <label class="q-text">{q_text}</label>
        <div class="radio-group">
            <label class="radio-option"><input type="radio" name="q{q_num}" value="0" required> 0</label>
            <label class="radio-option"><input type="radio" name="q{q_num}" value="1"> 1</label>
            <label class="radio-option"><input type="radio" name="q{q_num}" value="2"> 2</label>
            <label class="radio-option"><input type="radio" name="q{q_num}" value="3"> 3</label>
            <label class="radio-option"><input type="radio" name="q{q_num}" value="4"> 4</label>
        </div>
        <div class="radio-labels">
            <span>Strongly Disagree</span>
            <span>Strongly Agree</span>
        </div>
        <span class="stat-feedback" id="stat-q{q_num}"></span>
    </div>"""
        q_html += q_block
    return q_html

full_html = html_head + generate_questions_html() + html_tail

with open('backend/templates/survey.html', 'w') as f:
    f.write(full_html)

print("Successfully generated survey.html with Radio Buttons!")