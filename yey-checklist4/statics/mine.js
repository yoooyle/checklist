yey_waypoint_ops = {
  offset : '100%'
};

var new_cl_template = '<div class="row-fluid"><div class="span1"><input type="checkbox" /></div><div class="span11">TITLE</div></div>';

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

function delete_cl(key) {
  $.post("/delete/checklistdashboard", {'key': key}, function(data) {
    $('[id^="' + key + '"]').remove();
    Notifier.success("Checklist is removed");
  });
}

function delete_item(key) {
  $.post("/delete/itemdashboard", {'key': key}, function(data) {
    $('[id^="' + key + '"]').remove();
    Notifier.success("Item is removed");
  });
}

function create_cl() {
  $inputbox = $("#create_cl_input")
  title = $inputbox.get(0).value;
  if (title != '') {
    $.post("/create/checklist", {'title':title}, function(data) {
      $inputbox.get(0).value="";
      
      $listentry = $(data).filter('[id$="listing"]').get(0)
      $detailentry = $(data).filter('[id$="details"]').get(0)
      
      $("#mylists").children().eq(0).after($listentry);
      $("#cl_details").prepend($detailentry);
      eval($(data).filter('.editable_script').eq(0).text())
      Notifier.success("Created: List " + title);
      $("#subscriptions").toggleClass("active", false);
      $("#mylists").toggleClass("active", true);
    });
  }
}

function create_task() {
  $inputbox = $("#create_task_input")
  title = $inputbox.get(0).value;
  if (title != '') {
    $.post("/create/item", {'cl_key':sessionStorage.getItem('cl_key'), 'title':title}, 
      function(data) {
      $inputbox.get(0).value="";
      $listentry = $(data).filter('[id$="listing"]').get(0)
      console.log($listentry)
      $detailentry = $(data).filter('[id$="details"]').get(0)
      console.log($detailentry)
      
      $("#mytasks").prepend($listentry);
      $("#item_details").prepend($detailentry);
      eval($(data).filter('.editable_script').eq(0).text())      
      Notifier.success("Created: Task " + title);
    });
  }
}

function showEntity(key) {
  var prev = sessionStorage.getItem("last_entity_key");
  sessionStorage.setItem('last_entity_key', key);
  if (prev != null) {
    $('[id^="' + prev + '_side' + '"]').toggleClass("hide", true);
  }
  $('[id^="' + key + '_side' + '"]').toggleClass("hide", false);
}

$(document).ready(function() {
  yey_set_waypoint();
  $('.edit_list').editable(window.location.origin + '/edit/checklistdashboard', {
    indicator : 'Saving',
    tooltip : 'Click to edit',
    submit: 'Save',
    cancel: 'Cancel',
  });
  $('.edit_list_select').editable(window.location.origin + '/edit/checklistdashboard', {
    data : '{"Yes" : "Yes", "No" : "No"}',
    type : 'select',
    submit: 'Save',
    cancel: 'Cancel',
  });  
  $('.edit_list_area').editable(window.location.origin + '/edit/checklistdashboard', {
    indicator : 'Saving',
    tooltip : 'Click to edit',
    type : 'textarea',
    cancel: 'Cancel',
    submit: 'Save',
    style: 'inherit',
  })
  
  $('.edit_item').editable(window.location.origin + '/edit/itemdashboard', {
    indicator : 'Saving',
    tooltip : 'Click to edit',
    submit: 'Save',
    cancel: 'Cancel',
  });
  $('.edit_item_area').editable(window.location.origin + '/edit/itemdashboard', {
    indicator : 'Saving',
    tooltip : 'Click to edit',
    type : 'textarea',
    cancel: 'Cancel',
    submit: 'Save',
    style: 'inherit',
  })  
  $('.edit_item_difficulty_select').editable(window.location.origin + '/edit/itemdashboard', {
    data : '{"3" : "Hard", "2" : "Medium", "1" : "Easy"}',
    type : 'select',
    submit: 'Save',
    cancel: 'Cancel',
  });    
})