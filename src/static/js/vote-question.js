$(document).ready(function(){
    $("#question button").click(function(){
      var vote = parseInt($(this).attr("vote"));
      if(vote){
        var id = parseInt($(this).attr("question"));
        var total = parseInt($("#question-votes_"+id).text());
        $("#question-votes_"+id).html('<img src="/static/img/loading.gif" />');
        $.ajax({
          type : "POST",
          dataType : "text",
          url : "/pergunta-votar",
          contentType: "application/json; charset=utf-8",
          data : JSON.stringify({"id":""+id+"", "vote":""+vote+""}),
          success: function(data, textStatus, jQxhr){
            if(vote == 1)
              $("#question-upvote_"+id).css("background","green");
            else
              $("#question-downvote_"+id).css("background","green");
            $("#question-votes_"+id).val(vote+total);
            $("#question-votes_"+id).html($("#question-votes_"+id).val());
            $("#question-msg_"+id).html("<div class='alert alert-success' role='alert'>Tudo certo! O voto foi computado com sucesso.<div>");
          },
          error: function(jqXhr, textStatus, errorThrown){
            if(vote == 1)
              $("#question-upvote_"+id).css("background","red");
            else
              $("#question-downvote_"+id).css("background","red");
            $("#question-votes_"+id).html(total);
            $("#question-msg_"+id).html("<div class='alert alert-danger' role='alert'>Algo deu errado! Você já votou nessa pergunta.<div>");
          }
        });
      }
    });
});