// Her Drive's door for finished reels (Google Apps Script, deployed as a web app).
// tools/driveup.py asks it for an upload link; the video then goes straight to
// Drive, any size. Files land in the folder named in the request ("Reels" by
// default), created in her My Drive if it isn't there yet.
function doPost(e) {
  var req = JSON.parse(e.postData.contents);
  var name = req.folder || "Reels";
  var found = DriveApp.getFoldersByName(name);
  var folder = found.hasNext() ? found.next() : DriveApp.createFolder(name);
  var res = UrlFetchApp.fetch(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable&fields=id,name,webViewLink", {
      method: "post",
      contentType: "application/json; charset=UTF-8",
      headers: {
        Authorization: "Bearer " + ScriptApp.getOAuthToken(),
        "X-Upload-Content-Type": req.type || "video/mp4",
        "X-Upload-Content-Length": String(req.size)
      },
      payload: JSON.stringify({name: req.name, parents: [folder.getId()]})
    });
  var h = res.getHeaders();
  return ContentService.createTextOutput(JSON.stringify({upload: h.Location || h.location}))
    .setMimeType(ContentService.MimeType.JSON);
}
