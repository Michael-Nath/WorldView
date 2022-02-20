/*global chrome*/
chrome.runtime.onInstalled.addListener(() => {
  console.log('Chrome extension successfully installed!');
  return;
});

chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  if (changeInfo.status == 'complete') {

    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      console.log("PAGE LOADED: ")

      // chrome.storage.sync.set({
      //   currentArticleInfo: {
      //     "status": 200,
      //     "error": false,
      //     "headline": "German Chancellor rejects calls to sanction Russia now — argues the West should keep Putin guessing",
      //     "headline_sentiment": [
      //       "German Chancellor rejects calls to sanction Russia now — argues the West should keep Putin guessing"
      //     ],
      //     "content_sentiment": {
      //       "neg": 0.097,
      //       "neu": 0.807,
      //       "pos": 0.096,
      //       "compound": -0.3886
      //     },
      //     "top_words": {
      //       "“": 15,
      //       "”": 15,
      //       "Ukraine": 14,
      //       "’": 13,
      //       "Russia": 10,
      //       "said": 10
      //     }
      //   }
      // });
      fetch("http://54.219.124.53:5000/get-article-data?url=" + tabs[0].url)
        .then(res => res.json())
        .then(data => {
          const newData = {}
          newData[tabs[0].url] = data;
          chrome.storage.sync.set(newData)

          console.log("SAVED!")
          console.log(tabs[0].url)
        });


    });

  }
})