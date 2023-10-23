function employeeLogin() {
    // Assume you have a function `validateEmployeeLogin` that returns true on successful login
    const loginSuccessful = true;//validateEmployeeLogin();

    if (loginSuccessful) {
        // Redirect to the employee dashboard
        window.location.href = "employee_dashboard.html";
    }
}

function customerLogin() {
    // Assume you have a function `validateEmployeeLogin` that returns true on successful login
    const loginSuccessful = true;//validateEmployeeLogin();

    if (loginSuccessful) {
        // Redirect to the employee dashboard
        window.location.href = "customer_dashboard.html";
    }
}
