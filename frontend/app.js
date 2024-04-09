let token = localStorage.getItem("accessToken");
if (token) {
    verifyTokenAndRedirect(token);
}

async function verifyTokenAndRedirect(token) {
    try {
        const validateResponse = await fetch(
            "http://127.0.0.1:8000/auth/verifytoken",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ token: token }),
            }
        );

        if (validateResponse.ok) {
            const jsonResponse = await validateResponse.json();
            if (jsonResponse.valid) {
                window.location.href = "home.html";
            }
        } else {
            console.error("Token validation failed, redirecting to login.");
            localStorage.clear();
            window.location.href = "app.html";
        }
    } catch (error) {
        console.error("Error during token validation:", error);
    }
}

document
    .getElementById("signupButton")
    .addEventListener("click", async function () {
        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;

        if (username.trim() === "" || password.trim() === "") {
            alert("Username and password cannot be empty.");
            return;
        }

        try {
            console.log(
                `Signing up as user: ${username} with password: ${password}`
            );
            const signUpResponse = await fetch("http://127.0.0.1:8000/auth/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
            });

            if (!signUpResponse.ok) {
                console.log(`Username '${username}' already exists`);
                alert(`Username '${username}' already exists`);
                return;
            }

            alert("Sign up successful!");
        } catch (error) {
            console.error("Error during signup:", error);
            return;
        }
    });

document
    .getElementById("signinButton")
    .addEventListener("click", async function () {
        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;

        if (username.trim() === "" || password.trim() === "") {
            alert("Username and password cannot be empty.");
            return;
        }

        try {
            let body = new URLSearchParams({
                username: username,
                password: password,
            }).toString();

            const tokenResponse = await fetch(
                "http://127.0.0.1:8000/auth/token",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        Accept: "application/json",
                    },
                    body: body,
                }
            );

            if (!tokenResponse.ok) {
                alert("Invalid Username or Password");
                return;
            }

            const tokenData = await tokenResponse.json();
            alert("Sign in successful!");
            localStorage.setItem("accessToken", tokenData.access_token);
            window.location.href = "home.html";
        } catch (error) {
            console.error("Error during token retrieval:", error);
        }
    });
