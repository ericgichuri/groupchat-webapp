$(document).ready(function () {
    $(".btnviewgrp").click(function(){
        groupid=$(this).attr("data")
        grpname=$(this).attr("data-grpN")
        grpinfo=$(this).attr("data-grpIn")
        grpimg=$(this).attr("data-grpImg")
        $.ajax({
            type: "post",
            url: "/checkgroup",
            data: {groupid:groupid},
            success: function (response) {
                $(".mdgrpname").text("Group Name: "+grpname)
                $(".mdgrpinfo").text("Group Info: "+grpinfo)
                $(".mdgrpimg").attr("src",'static/images/groupicons/'+grpimg)
                if(response.msg==1){
                    $(".btnstatus").text("You are admin")
                    $(".btnstatus").attr("data","")
                    $(".btnstatus").attr("databtngroupid",groupid)
                }else if(response.msg==2){
                    $(".btnstatus").text("You are member")
                    $(".btnstatus").attr("data","")
                    $(".btnstatus").attr("databtngroupid",groupid)
                }else if(response.msg==3){
                    $(".btnstatus").text("Join Group")
                    $(".btnstatus").attr("data","btnjoin")
                    $(".btnstatus").attr("databtngroupid",groupid)
                }else{
                    $(".btnstatus").text("Error")
                    $(".btnstatus").attr("data","")
                    $(".btnstatus").attr("databtngroupid",groupid)
                }
                $("#modelviewgroup").show()
            }
        });
    })
    $(".btnstatus").click(function(){
        if($(this).attr("data")=="btnjoin"){
            var groupid=$(this).attr("databtngroupid")
            $.ajax({
                type: "post",
                url: "/joingroup",
                data: {groupid:groupid},
                success: function (response) {
                    if(response.message==1){
                        alert("You joined successfully")
                        $(".mygroupsdiv").empty()
                        $(".mygroupsdiv").load('/viewallgroups')
                        
                        $("#modelviewgroup").hide()
                    }else{
                        alert("Unable to join group \n"+response.message)
                        
                    }
                }
            });

        }else{
            $("#modelviewgroup").hide()
        }
    })
    $(".closemodal").click(function(){
        $("#modelviewgroup").hide()
    })
});