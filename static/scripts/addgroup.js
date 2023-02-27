$(document).ready(function () {
    $(".btndefaultupload").change(function(event){
        var file=URL.createObjectURL(event.target.files[0])
        $(".groupiconpreview").attr('src',file)
    })
    $(".btnclose").click(function(){
        $(".others").empty()
    })
    $(".formaddgroup").on("submit",function(e){
        e.preventDefault()
        var formdata=new FormData(this)
        msg=confirm("Do you want to create group?")
        if(msg==true){
            $.ajax({
                type: "post",
                url: "/addgroup",
                data: formdata,
                contentType:false,
                processData:false,
                success: function (response) {
                    if(response.message==1){
                        alert("Group created successfully")
                        $(".mygroupsdiv").empty()
                        $(".mygroupsdiv").load('/viewallgroups')
                    }else{
                        alert(response.message)
                    }
                }
            });
        }
    })
});