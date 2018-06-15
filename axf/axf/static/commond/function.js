
function addcart(goods_id) {
            var token = $('input[type=hidden]').val();
            $.ajax({
                url:'/axf/addcart/',
                type:'POST',
                data:{
                    'goods_id':goods_id
                },
                dataType:'json',
                headers:{'X-CSRFToken': token},
                success:function (msg) {
                    if (msg.code == 200){
                        $('#num_'+ goods_id).text(msg.c_num)
                    }else{
                        alert(msg.msg)
                    }
                },
                error:function (msg) {
                    alert(msg.msg)
                }
            })
        }

function subcart(goods_id) {
    var token = $('input[type=hidden]').val();
    $.ajax({
        url:'/axf/subcart/',
        type:'POST',
        data:{'goods_id':goods_id},
        dataType:'json',
        headers:{'X-CSRFToken':token},
        success:function (msg) {
            if (msg.code == 200){
                $('#num_' + goods_id).text(msg.c_num)
            }else{
                alert(msg.msg)
            }
        },
        error:function (msg) {
            alert(msg.msg)
        }
    });
}

 function addcart(goods_id) {
        var token = $('input[type=hidden]').val();
        $.ajax({
            url:'/axf/addcart/',
            type:'POST',
            data:{
                'goods_id':goods_id
            },
            dataType:'json',
            headers:{'X-CSRFToken': token},
            success:function (msg) {
                if (msg.code == 200){
                    $('#num_'+ goods_id).text(msg.c_num)
                }else{
                    alert(msg.msg).remove()
                }
                total_price()
            },
            error:function (msg) {
                alert(msg.msg)
            }
        })
    }
function subcarts(goods_id) {
    var token = $('input[type=hidden]').val();
    $.ajax({
        url:'/axf/subcart/',
        type:'POST',
        data:{'goods_id':goods_id},
        dataType:'json',
        headers:{'X-CSRFToken':token},
        success:function (msg) {
            if (msg.code == 200){
                $('#num_' + goods_id).text(msg.c_num)
                if (msg.c_num == 0){
                    $('#num_'+ goods_id).parent().parent().remove()
                }
            }else{
                alert(msg.msg)
            }
            total_price()
        },
        error:function (msg) {
            alert(msg.msg)
        }
    });
}
function change(id) {

        var token = $('input[type=hidden]').val();
        $.ajax({
            url:'/axf/change_cart_select/',
            type:'POST',
            data:{'cart_id':id},
            headers:{'X-CSRFToken':token},
            dataType:'json',
            success:function (data) {
                if (data.is_select){
                    $('#num_'+ id).text('√')
                }else{
                    $('#num_'+ id).text('x')
                }
                total_price()
            },
            error:function () {

            }
        })
    }
$(function () {
    total_price()
})

function total_price() {
    $.get('/axf/total/', function(data){
            $('#total').html(data.total)
        })
    }


function all_selects() {
    var token = $('input[type=hidden]').val();
    var i = $('#selects').attr('name')
    $.ajax({
        url: '/axf/all_select/',
        type: 'POST',
        dataType: 'json',
        headers: {'X-CSRFToken': token},
        data: {
            'is_selected': i
        },
        success: function (data) {
            total_price()
            if (data.code == '200') {
                if (data.flag) {
                    for (var a = 0; a < data.cart_id.length; a++) {
                        $('#num_' + data.cart_id[a]).text('x');
                        $('#all').text('x');
                    $('#selects').attr({'name': '1'});
                    }

                } else {
                    for (var b = 0; b < data.cart_id.length; b++) {
                        $('#num_' + data.cart_id[b]).text('√');
                        $('#all').text('√');
                    $('#selects').attr({'name': '0'});
                    }
                }
            }
        }
    })
}


// function receipt() {
//     alet('hjkl;')
    // var token = $('input[type=hidden]').val();
    // $.ajax({
    //     url:'/axf/receipt/',
    //     type:'POST',
    //     headers:{'X-CSRFToken':token},
    //     data:{
    //         'o_num':o_num
    //     },
    //     dataType:'json',
    //     success:function (data) {
    //         if (data == 200){
    //              $(this).parent().remove()
    //         }
    //     }
    // })
// }



