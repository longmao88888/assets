function infoclose(obj){
    $(obj).parent().parent().css("background-color","red");
    $(obj).parent().parent().find("p").css("background-color","green");
     $(obj).parent().parent().find("td").attr('contentEditable','true');
    //   $(obj).parent().parent().find("#tdd").css("background-color","yellow");
    //  $(obj).parent().parent().find("#tdd").attr('contentEditable','true');
    // $(obj).parent().parent().find("table").setAttribute('contentEditable','true');
    // document.getElementById("tdd").setAttribute('contentEditable','true');
    alert("success");
}