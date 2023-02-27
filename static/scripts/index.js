$(document).ready(function () {
    //$(".btndropdown img").toggleClass('toggle')
    //$(".sidemenu").toggleClass('hide')
    $(".btndropdown img").click(function(){
        $(".btndropdown img").toggleClass('toggle')
        $(".sidemenu").toggleClass('hide')
    })
    $(".btnlist").click(function(){
        $(".btndropdown img").toggleClass('toggle')
        $(".sidemenu").toggleClass('hide')
    })
    $(".btnlogout").click(function(){
        msg=confirm("Do you want to logout")
        if(msg==true){
            window.location.href="/logout"
        }
        
    })
    $(".btnaddgroup").click(function(){
        $(".others").empty()
        $(".others").load("/addgroup")
    })
    $(".mygroupsdiv").empty()
    $(".mygroupsdiv").load('/viewallgroups')
    $(".divchatform").on("submit",function(e){
        e.preventDefault()
        formdta=new FormData(this)
        $.ajax({
            type: "post",
            url: "/sendmessage",
            data: formdta,
            processData:false,
            contentType:false,
            success: function (response) {
                if(response.message==1){
                    alert("messsage sent")
                    $(".divchatform")[0].reset()
                    $(".divchatarea").load("/displaychats")
                }else{
                    alert(response.message)
                }
            }
        });
    })
    $(".btnbio").click(function(){
        $.ajax({
            type: "post",
            url: "/displaymybio",
            data: "data",
            success: function (response) {
                if(response.msg==1){
                    $(".mybioname").text("Name: "+response.ret[0][1])
                    $(".mybiophoneno").text("Phone No: "+response.ret[0][2])
                    $(".mybioemail").text("Email: "+response.ret[0][3])
                    $(".mybiocountry").text("Country: "+response.ret[0][4])
                    $(".mybioedu").text("Education: "+response.ret[0][5])
                    $(".mybioprof").text("Profession: "+response.ret[0][6])
                    $(".mybioimg").attr("src","static/images/profiles/"+response.ret[0][9])
                }else{
                    alert("error")
                }
            }
        });
    })
});