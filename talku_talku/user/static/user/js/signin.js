$(".toggle-password").click(function () {

    $(this).toggleClass("fa-eye fa-eye-slash");
    var input = $($(this).attr("toggle"));
    if (input.attr("type") == "password") {
        input.attr("type", "text");
    } else {
        input.attr("type", "password");
    }
});
$(".toggle-password2").click(function () {

    $(this).toggleClass("fa-eye fa-eye-slash");
    var input2 = $('#password-field2');
    if (input2.attr("type") == "password") {
        input2.attr("type", "text");
    } else {
        input2.attr("type", "password");
    }
});