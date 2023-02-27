$(document).ready(function () {
    $(".btn_to_signin").click(function(){
        window.location.href="/login"
    })
    $(".btnnext").click(function(){
        var dn=$(this).attr('data')
        if(dn==1){
            $(".mldiv").removeClass('divactive')
            $(".othersinfo").addClass('divactive')
        }else if(dn==2){
            $(".mldiv").removeClass('divactive')
            $(".systeminfo").addClass('divactive')
        }else if(dn==3){
            $(".mldiv").removeClass('divactive')
            $(".profileinfo").addClass('divactive')
        }
    })
    $(".btnprev").click(function(){
        var dp=$(this).attr('data')
        if(dp==1){
            $(".mldiv").removeClass('divactive')
            $(".personalinfo").addClass('divactive')
        }else if(dp==2){
            $(".mldiv").removeClass('divactive')
            $(".othersinfo").addClass('divactive')
        }else if(dp==3){
            $(".mldiv").removeClass('divactive')
            $(".systeminfo").addClass('divactive')
        }
    })
    $(".normalupload").change(function(event){
        var file=URL.createObjectURL(event.target.files[0])
        $(".profileimage").attr('src',file)
    })
    $(".form").on("submit",function(e){
        e.preventDefault()
        var formdata=new FormData(this)
        $.ajax({
            type: "post",
            url: "/register",
            data: formdata,
            contentType:false,
            processData:false,
            success: function (response) {
                if(response.message==1){
                    $(".flashmessage").text("Registered Successfully")
                    $(".form")[0].reset()
                    $(".profileimage").attr('src',"")
                }else{
                    $(".flashmessage").text(response.message)
                }
            }
        });
    })
});