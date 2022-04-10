/*function tip() {
  msg.className= "tip";
  msg.textContent= "username@gmail.com";
}
var elm= document.getElementById("username");
var msg= document.getElementById("tip");
elm.addEventListener("focus",tip,false);
elm.addEventListener("blur",function(){
  msg.textContent= ""
},false);*/

var btn = document.getElementById("closebtn");
var alert = document.getElementById("alert");
btn.addEventListener("click",function() {
  alert.style.display = "none";
},false);
