yey_waypoint_ops = {
  offset : '100%'
};

function waypoint_handler(e, direction) {
  if (direction === 'down') {
    // loading animation
    $loading = 
      $('<div class="progress progress-striped active" style="width:10%; margin:auto;">\
        <div class="bar" style="width: 10%"></div></div>');
    $("#main").append($loading);
    loading_id = setInterval(function() {
      current_width = $loading.children().css('width');
      $loading.children().css('width', parseInt(parseInt(current_width)*3) + "px")
    }, 10);
    
    // fetch items
    id_split = $(this).get(0).id.split('_');
    if (id_split.length != 3) {
      console.log("error splitting id");
    }
    $(this).waypoint('remove');
    fetch_more_items(id_split[1], id_split[2], $(this), $loading, loading_id);
  }
}

function yey_set_waypoint() {
  if ($(document.body).height() > $(window).height()) {
  (function($footer) {
    console.log($footer.eq(0))
    $footer.waypoint(waypoint_handler, yey_waypoint_ops);
  })($('footer[id^="more"]').eq(0));
  }
}

// cl_id is cl for listing cls, a number for listing items
function fetch_more_items(cl_id, cursor, $footer, $loading, loading_id) {
    if (cl_id == "cl") {
      url = "/";
    } else {
      url = "/cl/" + cl_id;
    }
    $.get(url,
      {'cursor': cursor,
       'id': cl_id },
      function(data){
        obj = document.createElement("html")        
        obj.innerHTML = data;
        console.log(obj);
        setTimeout(function(){
          clearInterval(loading_id);
          $loading.remove();
          $("#main").append($("#main", obj).eq(0));
          $footer.replaceWith($("footer", obj).eq(0));
          $('footer[id^="more"]').waypoint(waypoint_handler, yey_waypoint_ops);
        }, 700);
      },
      "html"
    )
}

function deleteItem(item_id) {
  $.post("/delete/item", {'item_id': item_id}, function(data) {
    $("#"+item_id).remove();
    Notifier.success("Task is removed.");
  })

}

function deleteCL(cl_id) {
  $.post("/delete/checklist", {'cl_id': cl_id}, function(data) {
    $("#"+cl_id).remove();
    Notifier.success("Checklist is removed.");
  })
  
}


