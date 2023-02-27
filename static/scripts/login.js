$(document).ready(function () {
    $(".btn_to_signup").click(function(){
        window.location.href="/register"
    })
    $(".form").on("submit",function(e){
        e.preventDefault()
        var formdata=new FormData(this)
        $.ajax({
            type: "post",
            url: "/login",
            data: formdata,
            contentType:false,
            processData:false,
            success: function (response) {
                if(response.message==1){
                    $(".flashmessage").text('Login Successful')
                    window.location.href="/home"
                }else{
                    $(".flashmessage").text(response.message)
                }
            }
        });
    })
});