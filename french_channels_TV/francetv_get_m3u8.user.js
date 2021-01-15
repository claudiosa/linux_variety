// ==UserScript==
// @name        get_m3u8
// @namespace   francetvinfo
// @include     http://www.francetvinfo.fr/*
// @version     1
// @grant       none
// ==/UserScript==

/* Using Content Script Injection (window.functionName) to make function available outside GreaseMonkey scope
Page reload is needed if using existing function _jsonp_loader_callback_request_0. */

window._jsonp_loader_callback_request_1 = function(json)
{
  alert(json.videos[1].url);
}

window._jsonp_loader_callback_request_2 = function(json)
{
  alert(json.videos[5].url);
}

function get_m3u8()
{
  // replay
  var el = document.getElementById("catchup");
  if (el) {
    var id = el.href.match(/video\/(.*)@/)[1];
    var script = document.createElement("script");
    script.src = "http://sivideo.webservices.francetelevisions.fr/tools/getInfosOeuvre/v2/?idDiffusion=" + id + "&catalogue=Info-web&callback=_jsonp_loader_callback_request_1";
    document.getElementsByTagName("head")[0].appendChild(script);
  } else {
    // live
    var el = document.getElementById("en_direct_video");
    if (el) {
      var id = el.href.match(/video\/(.*)/)[1];
      var script = document.createElement("script");
      script.src = "http://sivideo.webservices.francetelevisions.fr/tools/getInfosOeuvre/v2/?idDiffusion=" + id + "&catalogue=Pluzz&callback=_jsonp_loader_callback_request_2";
      document.getElementsByTagName("head")[0].appendChild(script);
    }
  }
}

get_m3u8();
