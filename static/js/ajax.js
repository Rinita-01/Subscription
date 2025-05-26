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

    $(document).on('click', '.subscribe-btn', function (event) {
      event.preventDefault();

      const cardBody = $(this).closest('.card-body');
      const planID = cardBody.find('.plan-id').val();
      const amountText = cardBody.find('.plan-price').text().trim();
      const amount = parseFloat(amountText);

      if (isNaN(amount) || amount <= 0) {
        alert('Invalid subscription amount.');
        return;
      }

      const amountInPaise = Math.round(amount * 100);
      const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

      const requestData = {
        amount: amountInPaise.toString(),
        plan_id: planID,
        csrfmiddlewaretoken: csrfToken
      };

      $.ajax({
        url: '/payments/create_order/',
        type: 'POST',
        data: requestData,
        success: function (data) {
          const options = {
            key: data.key,
            amount: data.amount,
            order_id: data.order_id,
            currency: 'INR',
            name: 'BuyBook Subscription',
            description: 'Payment for subscription plan',
            handler: function (response) {
              alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);

              const verifyData = {
                razorpay_order_id: response.razorpay_order_id,
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_signature: response.razorpay_signature,
                plan_id: planID,
                csrfmiddlewaretoken: csrfToken
              };

              $.ajax({
                url: '/payments/verify_payment/',
                type: 'POST',
                data: verifyData,
                success: function (verificationResponse) {
                  if (verificationResponse.success) {
                    alert("Subscription payment verified successfully!");
                    window.location.href = `/payments/success/${verificationResponse.subscription_id}/`;
                  } else {
                    alert("Payment verification failed: " + verificationResponse.error);
                  }
                },
                error: function (error) {
                  console.error("Verification error:", error);
                  alert("Error verifying subscription payment.");
                }
              });
            }
          };

          const rzp = new Razorpay(options);
          rzp.open();
        },
        error: function (error) {
          console.error('Order creation error:', error);
          alert('Error creating subscription order.');
        }
      });
    });
});
