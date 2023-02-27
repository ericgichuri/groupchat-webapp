$(document).ready(function () {
    $(".btntojoin").click(function(){
        var groupid=$(this).attr('data')
        var groupname=$(this).attr('data-name')
        msg=confirm("Do you want to join group "+groupname+" ?")
        if(msg==true){
            $.ajax({
                type: "post",
                url: "/joingroup",
                data: {groupid:groupid},
                success: function (response) {
                    if(response.message==1){
                        alert("You joined successfully")
                        $(".mygroupsdiv").empty()
                        $(".mygroupsdiv").load('/viewallgroups')
                        
                    }else{
                        alert("Unable to join group \n"+response.message)
                    }
                }
            });
        }
    })
    $(".btnchat").click(function(){
        var groupid=$(this).attr('data')
        $.ajax({
            type: "post",
            url: "/viewgroupmembers",
            data: {groupid:groupid},
            success: function (response) {
                //alert(response.groupadmin)
                $(".others").empty()
                
                $(".others").load("/viewgroupmembers")
                $(".grouprow").removeClass('activegroup')
                $(".grp"+groupid).addClass('activegroup')
                $(".divchatarea").load("/chatarea")
                
            }
        });
        grpdivid=$(this).parents(".grp"+groupid).attr("id")
        groupname=$("#"+grpdivid).children(".grpinfo"+groupid).attr("data-grpname")
        groupdescrp=$("#"+grpdivid).children(".grpinfo"+groupid).attr("data-grpdescrp")
        groupimage=$("#"+grpdivid).children(".groupimg"+groupid).attr("data-grpimg")
        $(".chatgrpname").text(groupname)
        $(".chatgrpdescrp").text(groupdescrp)
        $(".chatgrpimage").attr('src','static/images/groupicons/'+groupimage)
        $(".chatgroupid").val(groupid)
    })
    
    $(".btnsearch").click(function(){
        var searchname=$(".searchtext").val()
        $.ajax({
            type: "post",
            url: "/searchgroup",
            data: {searchname:searchname},
            success: function (response) {
                $(".displayallgroups").load("/displaysearchedgroups")
            }
        });
    })
    $("#checkall").click(function(){
        if(this.checked==true){
            $.ajax({
                type: "post",
                url: "/displayallgroups",
                data: {"viewall":"viewall"},
                success: function (response) {
                    $(".displayallgroups").load("/displaysearchedgroups")
                }
            });
        }else{
            $(".displayallgroups").empty()
        }
    })
});