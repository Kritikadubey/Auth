async function getRadioValue(radioButton){
    let selectedValue = null;
    for(const value of radioButton){
        if(value.checked){
            selectedValue = value;
            console.log(selectedValue);
            break;
        }
    }
    return selectedValue;
}

//First Login Page
const loginEmail = document.getElementById("login-email");
const loginPassword = document.getElementById("login-password");
const firstLoginButton = document.getElementById("first-login");

//First register page
const regName = document.getElementById("reg-name");
const regEmail = document.getElementById("reg-email");
const regPassword = document.getElementById("reg-password");
const education = document.getElementById("edu");
const profession = getRadioValue(document.getElementsByName("profession"));
const dob = document.getElementById("birthday");
const firstRegisterButton = document.getElementById("register");

async function validateFirstLogin(event){
    if(!loginEmail.value || !loginPassword.value){
        alert("Enter the the fields");
        return false;
    }
    sessionStorage.setItem("currEmail", loginEmail.value);
    const formData = new FormData();
    formData.append("email", loginEmail.value);
    formData.append("password", loginPassword.value);

    try{
        const response = await fetch("/login_validation", {
            method: "POST",
            body: formData
        });

        if(response.redirected){
            window.location.replace(response.url);
        }
        else{
            const data = await response.json();
            alert(data.description);
        }
    }catch(error){
        console.log(error);
    }
} 

if(firstLoginButton){
    firstLoginButton.addEventListener("click",(event)=>{
        validateFirstLogin(event);
    } );
}


//second login page
const optForLogin = document.getElementById("login-otp");
const secondLoginBtn = document.getElementById("login-otp-btn");

async function login_otp_varification(){
    if(!optForLogin.value){
        alert("Enter The OTP");
        return false;
    }
    const response = await fetch("/otp_varification", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify(
            {"OTP" : optForLogin.value, "EMAIL" : sessionStorage.getItem("currEmail")}
        )
    })
    const result = await response.json();
    if(result.result === true){
        window.location.replace("/third");
    }
    else{
        alert("Incorrect OTP");
    }
}

if(secondLoginBtn){
    secondLoginBtn.addEventListener("click", (event)=>{
        console.log("click");
        login_otp_varification();
    })
}

async function validateRegister(){
    if(!regName.value || !regEmail.value || !regPassword.value || !education || !profession || dob == ""){
        alert("Enter the value at all feed");
        return false;
    }
    sessionStorage.setItem("currEmail", regEmail.value);
    sessionStorage.setItem(regEmail.value, JSON.stringify({
        "name" : regName.value,
        "password" : regPassword.value,
        "education" : education.value,
        "profession" : profession.value,
        "dob" : dob.value
    }));

    try{
        const response = await fetch("/second_register", {
            method:"POST",
            body: regEmail.value
        });
        if(response.ok){
            window.location.replace("/second_register");
        }
        else{
            alert("somthing Gone wrong");
            window.location.reload();
        }
    }
    catch(error){
        console.log(error);
    }
}

if(firstRegisterButton){
    firstRegisterButton.addEventListener("click", (event)=>{
        console.log("click");
        validateRegister();
    });
}

//Third register page
const optForRegistration = document.getElementById("regester-otp");
const lastRegistrationButton = document.getElementById("last-register");

async function last_register(){
    const dataToSend = JSON.parse(sessionStorage.getItem(sessionStorage.getItem("currEmail")));
    dataToSend.Email = sessionStorage.getItem("currEmail");
    console.log(dataToSend);
    const response = await fetch("/last_reg",{
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',        
        },
        body: JSON.stringify(dataToSend)
    }) 
    const result = await response.json();
    if(result.status === "success"){
        window.location.href = "/";
    }
    else{
        alert("something went wrong");
    }
} 

async function otp_verification(){
    if(!optForRegistration.value){
        alert("Enter The OTP");
        return false;
    }
    const response = await fetch("/otp_varification", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify(
            {"OTP" : optForRegistration.value, "EMAIL" : sessionStorage.getItem("currEmail")}
        )
    })
    const result = await response.json();
    if(result.result === true){
        last_register();
    }
    else{
        alert("Incorrect OTP");
    }
}

if(lastRegistrationButton){
    lastRegistrationButton.addEventListener("click", (event)=>{
        console.log("click");
        otp_verification();
    })
}
