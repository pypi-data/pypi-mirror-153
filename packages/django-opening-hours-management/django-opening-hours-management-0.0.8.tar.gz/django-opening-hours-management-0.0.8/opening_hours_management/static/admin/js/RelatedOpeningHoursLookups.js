(function () {
  "use strict";

  function dismissAddOpeningHourPopup(win, newId, newRepr, objDisplay) {
    var id = win.name;
    var id_selector = interpolate("%s", [id]);
    var id_display_selector = interpolate("%s_display", [id]);
    document.getElementById(id_display_selector).innerHTML = objDisplay;
    document.getElementById(id_selector).value = newId;
    updateRelatedObjectLinks("#" + id_selector);
    win.close();
  }

  function dismissChangeOpeningHourPopup(
    win,
    objId,
    newRepr,
    newId,
    objDisplay
  ) {
    var id = win.name.replace(/^edit_/, "");
    var id_selector = interpolate("%s", [id]);
    var id_display_selector = interpolate("%s_display", [id]);
    document.getElementById(id_display_selector).innerHTML = objDisplay;
    document.getElementById(id_selector).value = newId;
    updateRelatedObjectLinks("#" + id_selector);
    win.close();
  }

  function dismissDeleteOpeningHourPopup(win, objId) {
    var id = win.name.replace(/^delete_/, "");
    var id_selector = interpolate("%s", [id]);
    var id_display_selector = interpolate("%s_display", [id]);
    document.getElementById(id_display_selector).innerHTML = gettext(
      "No opening hours defined"
    );
    document.getElementById(id_selector).value = null;
    updateRelatedObjectLinks("#" + id_selector);
    win.close();
  }

  window.dismissAddOpeningHourPopup = dismissAddOpeningHourPopup;
  window.dismissChangeOpeningHourPopup = dismissChangeOpeningHourPopup;
  window.dismissDeleteOpeningHourPopup = dismissDeleteOpeningHourPopup;
})();
