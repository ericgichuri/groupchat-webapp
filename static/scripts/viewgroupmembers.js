$(document).ready(function () {
    $(".btnviewmember").click(function(){
        var userid=$(this).attr('data')
        var position=$(this).attr('data-position')
        $.ajax({
            type: "post",
            url: "/viewmember",
            data: {userid:userid},
            success: function (response) {
                $(".textMpos").text("Position: "+position)
                $(".textMname").text("Name: "+response.memberdetails[0])
                $(".textMtel").text("Tel: "+response.memberdetails[1])
                $(".textMemail").text("Email: "+response.memberdetails[2])
                $(".imgMprofile").attr('src','static/images/profiles/'+response.memberdetails[3])
            }
        });
        
    })
});