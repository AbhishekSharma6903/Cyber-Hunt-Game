//var send = document.getElementById("ht");
//send.addEventListener("click",openhint);

function openhint(){
    const maindiv = document.getElementById("hnt");
    let userdiv = document.createElement("div");
    userdiv.id = "hintbox";
    userdiv.innerHTML = ` <div class="hntbx">
    <p> See whats happening in the gif <br> collect information<br> and use it to proceed further <br> </p>
 </div>`;
 maindiv.appendChild(userdiv);
}