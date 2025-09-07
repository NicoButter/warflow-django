
function handleCredentialResponse(response) {
    console.log("JWT recibido:", response.credential);
    $.post("{% url 'accounts:google_login' %}", { credential: response.credential })
     .done(function(data) {
         console.log("Redirigiendo a:", data.redirect_url);
         window.location.href = data.redirect_url;
     })
     .fail(function(err) {
         console.error("Error login Google:", err);
         alert("Error al iniciar sesión con Google.");
     });
}

window.onload = function () {
    google.accounts.id.initialize({
        client_id: '412755564966-676n6n8qeehofgo4ihmineteauom13e2.apps.googleusercontent.com',
        callback: handleCredentialResponse,
        auto_select: false,
    });

    google.accounts.id.renderButton(
        document.getElementById("googleSignInBtn"),
        { theme: "outline", size: "large", text: "signin_with" }
    );

    google.accounts.id.prompt(); 
};