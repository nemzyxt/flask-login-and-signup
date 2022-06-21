// check that the 2 passwords are indeed the same
function pass_match() {
    var pass = document.myform.passwd.value;
    var pass1 = document.myform.passwd1.value;
    if(pass === pass1) {
        return true;
    } else {
        document.getElementById('pass_err').innerHTML = 'Passwords do not match';
        return false;
    }
}