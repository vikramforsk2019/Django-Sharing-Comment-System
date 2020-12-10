$('#create_bookfrm').submit(function (e) {
        e.preventDefault();
//alert('parents');
    var content = $('input[name=commentbox]').val()
    var postid = $('input[name=postid]').val()
        $.ajax({
            type: 'POST',       // define the type of HTTP verb we want to use (POST for our form)
            url: '/comment_post/',
            dataType: 'json',
            data: JSON.stringify({
            'content': content,
            'postid': postid
                   }), 
            success: function (data) {
                //alert('ok');
                  window.location.reload();
               $('input[name=commentbox]').val(''); // remove the value from the input
            },
            error: function (exception) {
                alert('Exeption:' + exception);
            },
        });
    });


function child_comment(parentid) {
  var postid=document.getElementById(parentid+"postid").value
  var content=document.getElementById(parentid+"cc").value
  //alert(parentid)
          $.ajax({
            type: 'POST',       // define the type of HTTP verb we want to use (POST for our form)
            url: '/comment_post/',
            dataType: 'json',
            data: JSON.stringify({
            'content': content,
            'postid': postid,
            'parentid':parentid
                   }), 
            success: function (data) {
                //alert('ok');
                  window.location.reload();
             //  $('input[name=commentbox]').val(''); // remove the value from the input
            },
            error: function (exception) {
                alert('Exeption:' + exception);
            },
        });
  
  }

function edit(parentid) {
  var content=document.getElementById(parentid+"ee").value
        $.ajax({
            type: 'POST',       // define the type of HTTP verb we want to use (POST for our form)
            url: '/edit/',
            dataType: 'json',
            data: JSON.stringify({
            'content': content,
            'parentid':parentid
                   }), 
            success: function (data) {
                //alert('ok');
                  window.location.reload();
             //  $('input[name=commentbox]').val(''); // remove the value from the input
            },
            error: function (exception) {
                alert('Exeption:' + exception);
            },
        });
  
  }
function myLike(commentid,button) {
  //alert(button);
         $.ajax({
        type: 'POST',
        url: '/thumbs/',
        data: {
          postid: commentid,
          csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
          action: 'thumbs',
          button: button,
        },
        success: function (json) {
          if (json.length < 1 || json == undefined) {
            //empty
          }
          document.getElementById(commentid+"up").innerHTML = json['up']
          document.getElementById(commentid+"down").innerHTML = json['down']

        },
        error: function (xhr, errmsg, err) {}
      });

}




function getProducts(response) {
    var Json = JSON.parse(response)
    textlist = ""
    for (var i = 0; i < Json.length; i++) {
        textlist += "<input type='radio'  name='product' id=" + Json[i].pk + ">" + Json[i].fields['name'] + ", €" + Json[i].fields['price'] + "<br>"
    }
    $('#name').val('Name')
    $('#description').val("Description")
    $('#price').html("Price")
    if (textlist == "")
        $("#productlist").html("No products available, add one below please")
    else
        $("#productlist").html(textlist)

}
