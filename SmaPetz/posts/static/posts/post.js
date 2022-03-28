// Comments show/hide button
$(document).ready(function(){
    let display = false
    $(".cmtbutton").click(function(){
        if(display===false){
            $(this).next(".comment-box").show("slow");
            display=true
        }else{
            $(this).next(".comment-box").hide("slow");
            display=false
        }
    })
})