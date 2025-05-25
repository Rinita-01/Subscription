$(document).ready(function () {
  $("#register-btn").click(function (event) {
        event.preventDefault(); 
        
        let formData = new FormData();
        formData.append("email", $("#email").val().trim());
        formData.append("password", $("#password").val().trim());
        formData.append("first_name", $("#first_name").val().trim());
        formData.append("last_name", $("#last_name").val().trim());
        formData.append("username", $("#username").val().trim());

        console.log(formData)
        
        let profilePicture = $("#profile_picture")[0].files[0]; 
        if (profilePicture) {
            formData.append("profile_picture", profilePicture);
        }

        formData.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());

        $("#register-btn").prop("disabled", true); 

        $.ajax({
            type: "POST",
            url: "/users/register/",
            data: formData,
            processData: false,
            contentType: false,
            dataType: "json",
            success: function (response) {
                if (response.success) {
                    alert("Registration successful! Redirecting to login...");
                    window.location.assign("/users/customer_login/");
                } else {
                    alert("Error: " + response.error);
                }
            },
            error: function () {
                alert("Something went wrong. Please try again.");
            },
            complete: function () {
                $("#register-btn").prop("disabled", false);
            }
        });
    });


    $("#admin-Register-btn").click(function(event){
        event.preventDefault();

        var formData = new FormData();
        formData.append("username", $("#username").val());
        formData.append("email", $("#email").val());
        formData.append("password", $("#password").val());
        formData.append("first_name", $("#first_name").val());
        formData.append("last_name", $("#last_name").val());
        let profilePicture = $("#profile_picture")[0].files[0]; 
        if (profilePicture) {
            formData.append("profile_picture", profilePicture);
        }

        
        formData.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());

        $.ajax({
            url: "/users/admin_registration/", 
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            dataType: "json",
            success: function(response) {
                if (response.success) {
                    $("#message").text(response.message).css("color", "green");
                    setTimeout(function() {
                        window.location.href = response.redirect_url; 
                    }, 2000);
                } else {
                    $("#message").text(response.error).css("color", "red");
                }
            },
            error: function(response) {
                var errorMsg = response.responseJSON?.error || "An error occurred";
                $("#message").text(errorMsg).css("color", "red");
            }
        });
    });

    
    $("#login-btn").click(function (event) {
        event.preventDefault(); 
    
        let email = $("#email").val().trim();
        let password = $("#password").val().trim();
    
        if (!email || !password) {
            alert("Please enter both email and password.");
            return;
        }
    
        $("#login-btn").prop("disabled", true); 
    
        $.ajax({
            type: "POST",
            url: "/users/customer_login/",
            data: {
                email: email,
                password: password,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            dataType: "json",
            success: function (response) {
                if (response.success) {
                    alert("Login successful! Redirecting...");
                    window.location.assign(response.redirect_url);
                } else {
                    alert("Error: " + response.error);
                }
            },
            error: function (xhr, status, error) {
                alert("Something went wrong. Please try again.");
                console.log("AJAX error:", xhr.responseText);
            },
            complete: function () {
                $("#login-btn").prop("disabled", false);
            }
        });
    });
});
