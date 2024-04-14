const token = localStorage.getItem("accessToken");
const valid_user = localStorage.getItem("valid_user");

if (!localStorage.getItem("valid_user")) {
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

        if (!validateResponse.ok) {
            console.error("Token validation failed, redirecting to login.");
            localStorage.clear();
            window.location.href = "app.html";
            return;
        }

        const jsonResponse = await validateResponse.json();

        if (!jsonResponse.valid) {
            return;
        }

        window.location.href = "home.html";
        localStorage.setItem("valid_user", true);
    } catch (error) {
        console.error("Error during token validation:", error);
    }
}
