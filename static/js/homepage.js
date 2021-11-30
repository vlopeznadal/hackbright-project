// Once HTML document has been loaded
$(document).ready(function(){

    // When link with ID 'create-account' is clicked on homepage.html
    $(document).on('click', '#create-account', function() { 
        // Replace login form HTML with registration form HTML
        $('#login').replaceWith('<div name="register" id="register"><hr><h2 class="pt-2 justify-content-center text-center">Register</h2><form action="/register" method="POST"><div class="mb-3"><label for="register-email" class="form-label">Email address</label><input type="email" class="form-control" id="register-email" aria-describedby="emailHelp" name="register-email"></div><div class="mb-3"><label for="register-password" class="form-label">Password</label><input type="password" class="form-control" id="register-password" name="register-password"></div><button type="submit" class="btn btn-primary">Submit</button></form><a href="#" id="sign-in" class="p-2 d-flex justify-content-center text-center bold-link">Sign in</a></div>');
    });
    
    // When link with ID 'sign-in' is clicked on homepage.html
    $(document).on('click', '#sign-in', function() { 
        // Replace registration form HTML with login form HTML
        $('#register').replaceWith('<div name="login" id="login"><hr><h2 class="pt-2 justify-content-center text-center">Login</h2><form action="/login" method="POST"><div class="mb-3"><label for="login-email" class="form-label">Email address</label><input type="email" class="form-control" id="login-email" aria-describedby="emailHelp" name="login-email"></div><div class="mb-3"><label for="login-password" class="form-label">Password</label><input type="password" class="form-control" id="login-password" name="login-password"></div><button type="submit" class="btn btn-primary">Submit</button></form><a href="#" id="create-account" class="p-2 d-flex justify-content-center text-center bold-link">Create an account</a></div>');
    });
});