// Once HTML document has been loaded
$(document).ready(function(){

    // When link with ID 'create-account' is clicked on homepage.html
    $(document).on('click', '#create-account', function() { 
        // Replace login form HTML with registration form HTML
        $('#login').replaceWith('<div name="register" id="register" class="d-flex flex-column min-vh-100 justify-content-center align-items-center form"><form action="/register" method="POST"><h1>Create an account</h1><div class="mb-3"><label for="register-email" class="form-label">Email address</label><input type="email" class="form-control" id="register-email" aria-describedby="emailHelp" name="register-email"></div><div class="mb-3"><label for="register-password" class="form-label">Password</label><input type="password" class="form-control" id="register-password" name="register-password"></div><button type="submit" class="btn btn-primary">Submit</button></form>Already have an account? <a href="#" id="sign-in">Sign in</a></div>');
    });
    
    // When link with ID 'sign-in' is clicked on homepage.html
    $(document).on('click', '#sign-in', function() { 
        // Replace registration form HTML with login form HTML
        $('#register').replaceWith('<div name="login" id="login" class="d-flex flex-column min-vh-100 justify-content-center align-items-center form"><h1>Login</h1><form action="/login" method="POST"><div class="mb-3"><label for="login-email" class="form-label">Email address</label><input type="email" class="form-control" id="login-email" aria-describedby="emailHelp" name="login-email"></div><div class="mb-3"><label for="login-password" class="form-label">Password</label><input type="password" class="form-control" id="login-password" name="login-password"></div><button type="submit" class="btn btn-primary">Submit</button></form><a href="#" id="create-account">Create an account</a></div>');
    });
});