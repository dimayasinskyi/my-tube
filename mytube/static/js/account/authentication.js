// Opens or hides the login and registration window when you click on the buttons.
const signInBtn = document.getElementById('signInBtn');
const signUpBtn = document.getElementById('signUpBtn');
const signInModal = document.getElementById('signInModal');
const signUpModal = document.getElementById('signUpModal');
const closeSignIn = document.getElementById('closeSignIn');
const closeSignUp = document.getElementById('closeSignUp');

signInBtn.addEventListener('click', () => signInModal.classList.remove('hidden'));
signUpBtn.addEventListener('click', () => signUpModal.classList.remove('hidden'));
closeSignIn.addEventListener('click', () => signInModal.classList.add('hidden'));
closeSignUp.addEventListener('click', () => signUpModal.classList.add('hidden'));