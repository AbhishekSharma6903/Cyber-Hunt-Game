function openhint(){
    const maindiv = document.getElementById("hnt");
    let userdiv = document.createElement("div");
    userdiv.id = "hintbox";
    userdiv.innerHTML = ` <div class="hntbx">
    <p> this is a hint which <br> gives you an <br> idea of how to <br> approach the problem <br>hdjskn lleudbfs sfss gd <br> xodndo dgds agac fswcb</p>
 </div> `;
 maindiv.appendChild(userdiv);
}