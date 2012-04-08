function delete_cl(key, redirect) {
  $.post("/delete/checklistdashboard", {
    'key' : key
  }, function(data) {
    Notifier.success("Checklist is removed. Redirecting to homepage in 2s");
    setTimeout("window.location = '/' ", 1500);
  });
}

function delete_item(key) {
  $.post("/delete/itemdashboard", {
    'key' : key
  }, function(data) {
    $('[id^="' + key + '"]').remove();
    Notifier.success("Item is removed");
  });
}

function create_cl() {
  title = 'New Checklist'
  $.post("/create/checklist", {
    'title' : title
  }, function(data) {
    window.location = data; 
  });
}

function create_task() {
  $inputbox = $("#create_task_input")
  title = $inputbox.get(0).value;
  if (title != '') {
    $.post("/create/item", {
        'cl_key' : sessionStorage.getItem('cl_key'),
        'title' : title
    }, function(data) {
      $inputbox.get(0).value = "";
      $listentry = $(data).filter('[id$="listing"]').get(0)

      $("#items").children().eq(0).after($listentry);
      eval($(data).filter('.editable_script').eq(0).text())
      Notifier.success("Created: Task " + title);
    });
  }
}

// sub: want to subscribe?
function subscribe(id, sub, redirect) {
  $.post("/subscribe", {
      'subscribe' : sub,
      'cl_id' : id
  }, function(data) {
    if (data == 'subscribed') {
      $("#unsubscribe_button").toggleClass("hide", false);
      $("#subscribe_button").toggleClass("hide", true);
      msg = "Subscribed";
    } else if (data == 'unsubscribed') {
      $("#unsubscribe_button").toggleClass("hide", true);
      $("#subscribe_button").toggleClass("hide", false);
      msg = "Unsubscribed";
    }
    
    if (redirect) {
      Notifier.success(msg + ". Redirect to " + redirect + " in 2s ");
      setTimeout("window.location = '" + redirect + "'", 1500);
    } else {
      Notifier.success(msg);
    }
  })
}

function toggleComplete(subItem_key, checkbox, title_text) {
  title = $('[id="' + subItem_key + '_title"]').eq(0)
  console.log("1")
  if (checkbox.checked) {
    newnode= "<span><s><h4 class='inline'>" + title_text + "</h4></s></span>"
    finished = "finished"
  } else {
    newnode = "<span><h4 class='inline'>" + title_text + "</h4></span>"
    finished = "not finished"
  }
  $.post("/edit/subitemdashboard", {'key': subItem_key, 'finished': finished},
    function (data) {
      title.empty();
      title.append(newnode);
      if (checkbox.checked) {
        Notifier.success("Marked as complete");
      } else {
        Notifier.success("Marked as incomplete");
      }
  });
}

$(document).ready(function() {
  $('.edit_list').editable(window.location.origin + '/edit/checklistdashboard', {
      indicator : 'Saving',
      tooltip : 'Click to edit',
      submit : 'Save',
      cancel : 'Cancel',
  });
  $('.edit_list_area').editable(window.location.origin + '/edit/checklistdashboard', {
      indicator : 'Saving',
      tooltip : 'Click to edit',
      type : 'textarea',
      cancel : 'Cancel',
      submit : 'Save',
      style : 'inherit',
  })

  $('.edit_item').editable(window.location.origin + '/edit/itemdashboard', {
      indicator : 'Saving',
      tooltip : 'Click to edit',
      submit : 'Save',
      cancel : 'Cancel',
  });
  $('.edit_item_area').editable(window.location.origin + '/edit/itemdashboard', {
      indicator : 'Saving',
      tooltip : 'Click to edit',
      type : 'textarea',
      cancel : 'Cancel',
      submit : 'Save',
      style : 'inherit',
      rows : 3,
  })
})