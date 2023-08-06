/*global opener */
(function () {
  'use strict';
  var initData = JSON.parse(document.getElementById('django-admin-popup-response-constants').dataset.popupResponse);
  switch (initData.action) {
    case 'change':
      opener.dismissChangeOpeningHourPopup(window, initData.value, initData.obj, initData.new_value, initData.obj_display);
      break;
    case 'delete':
      opener.dismissDeleteOpeningHourPopup(window, initData.value);
      break;
    default:
      opener.dismissAddOpeningHourPopup(window, initData.value, initData.obj, initData.obj_display);
      break;
  }
})();
