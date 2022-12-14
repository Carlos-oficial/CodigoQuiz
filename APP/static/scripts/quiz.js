var strikes = 0;
var correct_n = 0;
var answered_n = 0;
var first_go = true;
var questions = [];
var wrong_answers = [];
var right_answers = [];

function bcrypt(e) {
    var t = String(e).replace(/=+$/, "");
    var n = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    for (
        var r = 0, i, s, o = 0, u = "";
        (s = t.charAt(o++)); ~s && ((i = r % 4 ? i * 64 + s : s), r++ % 4) ?
        (u += String.fromCharCode(255 & (i >> ((-2 * r) & 6)))) :
        0
    ) {
        s = n.indexOf(s);
    }
    return u;
}

function bc(e, t) {
    (n = bcrypt(e)), (r = n - t);
    return r;
}

function lazyLoadImage(id, enc_string) {
    e = bc(enc_string, id);
    return String.fromCharCode(e);
}

function validate(obj, answer, id, enc_string) {
    let correct = lazyLoadImage(id, enc_string);
    if (!answered) {
        answered = true;
        if (answer == correct) {
            obj.classList.add("bg-green-600");
            return true;
        } else {
            obj.classList.add("bg-red-600");
            document.getElementById(correct).classList.add("bg-green-600");
            return false;
        }
    }
}

async function postRecord(record, wrong_answers, right_answers) {
    console.log("posting" + record);
    fetch("/api/record", {
            method: "POST",
            body: JSON.stringify({
                score: record,
                wrong_answers: wrong_answers,
                right_answers: right_answers,
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8",
            },
        })
        .then((response) => response.json())
        .then((json) => console.log(json));
}

function deleteChildren(e) {
    let child = e.lastElementChild;
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }
}
async function fetchQuestion() {
    answered = false;
    let clicks = 1;

    if (injected && answered_n < injected.length) {
        id = injected[answered_n];
    } else {
        do var id = Math.floor(Math.random() * (5012 - 1103) + 1103);
        while (id in questions);
    }
    console.log(id)
    questions.push(id);

    let response = await fetch("api/questao/" + id);
    let text = await response.json();
    console.log(text);
    document.getElementById("question_text").innerHTML = text.question;
    document
        .getElementById("question_image")
        .setAttribute(
            "src",
            "https://www.bomcondutor.pt/assets/images/questions/" + id + ".jpg"
        );
    let answers = text.answers;
    ul = document.createElement("ul");
    ul.setAttribute("class", "space-y-2 mt-2");
    deleteChildren(document.getElementById("answers"));
    document.getElementById("answers").appendChild(ul);

    answers.forEach((item) => {
        let li = document.createElement("li");
        let span = document.createElement("span");
        let button = document.createElement("button");
        ul.appendChild(li);
        li.appendChild(span);
        li.id = item[0];
        span.setAttribute("class", "h-16 w-16 flex items-center justify-center");
        span.appendChild(button);
        button.innerHTML = item[0];
        button.setAttribute(
            "class",
            "w-[50px] h-[50px] rounded-[25px] bg-gray-600"
        );

        li.addEventListener("click", async function() {
            if (clicks) {
                if (!validate(li, item[0], id, text.enc_string)) {
                    clicks = 0;
                    strikes += 1;
                    wrong_answers.push(id);
                    document.getElementById("strikes").innerHTML = strikes;
                } else {
                    clicks = 0;
                    correct_n += 1;
                    right_answers.push(id);
                    document.getElementById("correct_n").innerHTML = correct_n;
                }
            }
            if (strikes > 3 && first_go) {
                // location.href = "/";
                first_go = false;
                if (confirm("Restart?")) {
                    console.log("u got", correct_n, "correct");
                    rec = await postRecord(correct_n, wrong_answers, right_answers);
                    console.log(rec);
                    // window.location.href = "/";
                }
            } else if (correct_n + strikes == 30) {
                if (confirm("You Passed \n Restart?")) {
                    location.reload();
                }
            }
        });
        li.setAttribute(
            "class",
            "h-16 w-full bg-blue-200 flex items-center rounded-[30px]"
        );
        li.innerHTML += item[1];
    });
    answered_n++;

    return text;
}

console.log(injected);

fetchQuestion();