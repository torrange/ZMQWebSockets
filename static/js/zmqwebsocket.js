var wsUri = "ws://127.0.0.1:8888/zmqwebsocket";

function init()
{
  feeder = document.getElementById("jsondiv")
  testWebSocket();
}

function testWebSocket()
{
  websocket = new WebSocket(wsUri);
  websocket.onopen = function(evt) { onOpen(evt) };
  websocket.onclose = function(evt) { onClose(evt) };
  websocket.onmessage = function(evt) { onMessage(evt) };
  websocket.onerror = function(evt) { onError(evt) };
}

function onOpen(evt)
{
  var log_entry = "Connected"
  console.log(log_entry)
}

function onClose(evt)
{
  var log_entry = "Disconnected"
  console.log(log_entry)
}

function onMessage(evt)
{
  writeToFeed(feedCreate(evt.data));
}

function onError(evt)
{
  var log_entry = "Error"
  console.log(log_entry)
}

function doSend(message)
{ 
  websocket.send(message);
}

function writeToFeed(message)
{
  feeder.innerHTML = message + feeder.innerHTML;
}

var feedCreate;

feedCreate = function(object) {
  var avatar, html_base, json, text, username;
  json = JSON.parse(object);
  username = json.username;
  avatar = json.avatar;
  text = json.text;
  return html_base = "<feed-card> <h2>" + username + "</h2> <img src=\"" + avatar + "\"> <p>" + text + "</p> </feed-card>";
};

window.addEventListener("load", init, false);