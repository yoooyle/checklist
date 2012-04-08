waypoint_ops = {
  offset : '100%'
};

function yey_setup_first_waypoint() {
  /*
   * Set up the first waypoint for the page displaying the first checklist,
   * Which is displayed by default.
   */
    (function(span) {
      $(span).waypoint(function(event, direction) {
        if (direction === 'down') {
          id_split = span.id.split('_');
          if (id_split.length != 3) {
            console.log("error splitting id");
          }
          fetch_more_items(id_split[1], id_split[2], $(this));
        }
      }, waypoint_ops);
    })($('footer[id^="MoreItems"]')[0]);
}

function yey_update_waypoint(cl_key) {
  // First destroy all waypoints. Otherwise they'll be triggered
  // once they become invisible.
  $.waypoints().each(function() {
    $(this).waypoint('destroy');
  });

  // Find the span element with id MoreItems_{{ cl.key() }}_{{
  // item_cursors[loop.index0] }}
    $('footer[id^="MoreItems_' + cl_key + '"]').waypoint(function(event, direction) {
      if (direction === 'down') {
        id_split = this.id.split('_');
        if (id_split.length != 3) {
          console.log("error splitting id");
        }
        fetch_more_items(id_split[1], id_split[2], $(this));
      }
    }, waypoint_ops);
}

function fetch_more_items(cl_key, cursor, span) {
  if ($(document.body).height() > $(window).height()) {
  $.get('ajax/moreitems', cl_key + "&" + cursor, function(r, s, xhr) {
    $("#cl_" + cl_key + "_items").append(r);
    console.log("fetch item for span " + span[0].id);
    span.waypoint('remove');
    span.waypoint(waypoint_ops);
  });
} else {
  $.waypoints().each(function() {
    $(this).waypoint('remove');
  });

}
}