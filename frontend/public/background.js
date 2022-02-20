/*global chrome*/
chrome.runtime.onInstalled.addListener(() => {
  console.log('Chrome extension successfully installed!');
  return;
});

chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  if (changeInfo.status == 'complete') {

    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      console.log("Attempting to get data for: " + tabs[0].url)

      fetch("http://54.219.124.53:5000/get-article-data?url=" + tabs[0].url)
        .then(res => res.json())
        .then(data => {
          const newData = {}
          newData[tabs[0].url] = data;

          console.log("Attempting to save to local storage ...")
          chrome.storage.sync.set(newData)

          console.log("Success! Data has been retrieved and saved to local storage.")
          console.log(tabs[0].url)
        });


    });

  }
})