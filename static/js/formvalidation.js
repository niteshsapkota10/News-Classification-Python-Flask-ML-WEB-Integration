function validate(){
    var psw1=document.signupform.password.value;
    var psw2=document.signupform.rpassword.value;
    if (psw1.length<8){
        alert("Password length must be greater than 8 ")
        return false;
    }else{
        if(psw1!=psw2){
            alert("Passwords doesnot match");
            return false;
        }
    }
}