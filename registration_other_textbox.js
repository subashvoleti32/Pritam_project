function showOtherTextInput() {
    var idProofType = document.getElementById("idProofType");
    var otherIdProofType = document.getElementById("otherIdProofType");

    if (idProofType.value == "other") {
        otherIdProofType.style.display = "block";
    } else {
        otherIdProofType.style.display = "none";
    }
}
