$(document).ready(function(){
    $("#answer button").click(function () {
      var vote = parseInt($(this).attr("vote"));
      if(vote){
        var id = parseInt($(this).attr("answer"));
        var pergunta_id = parseInt($(this).attr("question"));
        var total = parseInt($("#answer-votes_"+id).text());
        $("#answer-votes_"+id).html('<img src="/static/img/loading.gif" />');
        $.ajax({
          type : "POST",
          dataType : "text",
          url : "/resposta-votar",
          contentType: "application/json; charset=utf-8",
          data : JSON.stringify({"idquestion":""+pergunta_id+"","idanswer":""+id+"", "vote":""+vote+""}),
          success: function(data, textStatus, jQxhr){
            if(vote == 1)
              $("#answer-upvote_"+id).css("background","green");
            else
              $("#answer-downvote_"+id).css("background","red");
            $("#answer-votes_"+id).val(vote+total);
            $("#answer-votes_"+id).html($("#answer-votes_"+id).val());
            $("#answer-msg_"+id).html("Tudo certo! O voto foi computado com sucesso.");
          },
          error: function(jqXhr, textStatus, errorThrown){
            $("#answer-votes_"+id).html(total);
            $("#answer-msg_"+id).html("Algo deu errado! Você já votou nessa resposta.");
          }
        });
      }
    }); 
});