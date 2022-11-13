$(document).ready(function(){
    for (let i = 0; i < 11; i++) {
        $('<div class="scorenumbox"></div>').appendTo('.scorebox');
    }
})


$(".dcmclassname").click(function(){
    $(this).parent().siblings().css({'font-weight':'normal','color':'black','background-color':'white'});
    $(this).parent().css({'font-weight':'bold','color':'blue','background-color':'aqua'});
})


$(".filebutton").change(function(){
    // console.log($(this)[0].files);
    // $("#img1").attr("src",URL.createObjectURL($(this)[0].files[0]));
    var allnum = $(this)[0].files.length;
    $(".allpagenum").val(allnum);
    $(".curpagenum").val(1);
    $(".predict").trigger('click');
});

$(".up").click(function(){
    // console.log(parseInt($(".curpagenum").val())+1);
    var curnum = parseInt($(".curpagenum").val())
    $("#img1").attr("src",'');
    $("#img2").attr("src",'');
    $("#img3").attr("src",'');
    $("#img4").attr("src",'');
    var allnum = parseInt($(".allpagenum").val())
    if(curnum<allnum){
        $(".curpagenum").val(curnum+1);
    }
    $(".predict").trigger('click');
})

$(".down").click(function(){
    // console.log(parseInt($(".curpagenum").val())+1);
    var curnum = parseInt($(".curpagenum").val());
    $("#img1").attr("src",'');
    $("#img2").attr("src",'');
    $("#img3").attr("src",'');
    $("#img4").attr("src",'');
    if(curnum>1){
        $(".curpagenum").val(curnum-1);
    }
    $(".predict").trigger('click');
})

$(".predict").click(function(){
    var targetUrl = $("#form-predict").attr("action");
    var data = new FormData($("#form-predict")[0])
    $(".scorenumbox").css('background-color','white');
    $.ajax({
        type: "post",
        url: targetUrl,
        cache: false,
        processData: false,
        contentType: false,
        data: data,
        dataType: "json",
        success: function (res) {
            var id = 0;
            $(".scorenumbox:eq("+res.index+")").css('background-color','aqua');
            $(".dcmclassname:eq("+res.index+")").trigger('click');
            // $(".dcmclassname:eq("+res.index+")").attr("checked","checked");
            // $(".dcmclassname:eq("+res.index+")").parent().css({'font-weight':'bold','color':'blue','background-color':'aqua'});
            // $(".scorenumbox").each(function(){
            //     $(this).css('background-color','white');
            //     if(id===res.index){
            //         $(this).css('background-color','aqua');
            //     }
            //     id+=1;
            // });        
            $("#img1").attr('src','static/imgs/0.jpg'+'?'+Math.random());
            $("#img2").attr('src','static/imgs/1.jpg'+'?'+Math.random());
            $("#img3").attr('src','static/imgs/2.jpg'+'?'+Math.random());
            $("#img4").attr('src','static/imgs/3.jpg'+'?'+Math.random());
        },
        error:function(err){
            console.log(err);
        }
    })
})

$(".upload").click(function(){
    var targetUrl = $("#form-submit").attr("action");
    var data = new FormData($("#form-submit")[0])
    // alert(data.get("dcmclass"))
    $.ajax({
        type: "post",
        url: targetUrl,
        cache: false,
        processData: false,
        contentType: false,
        data: data,
        dataType: "json",
        success: function (res) {
            console.log(res.Log);
            alert(res.Log);
        },
        error:function(err){
            console.log(err);
            alert("上传失败！");
        }
})})
