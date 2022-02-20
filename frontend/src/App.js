/*global chrome*/
import React, { useEffect, useState } from 'react'
import './App.css';
import styled from 'styled-components'
import { AiFillAppstore, AiFillSetting } from "react-icons/ai";
import { BsFillPeopleFill } from "react-icons/bs";
import { Loader, Dimmer } from 'semantic-ui-react'
import ReactFlow from 'react-flow-renderer';
import ClusterNode from './helpers/clusterNode'
import MainNode from './helpers/mainNode'

const elements = [
  {
    id: '1', type: 'main', data: {
      label: 'Perspective'
    },
    position: { x: 250, y: 5 }
  },
  {
    id: '2', type: 'cluster', data: {
      sentiment: {
        pos: 0.7,
        neg: 0.2,
        neu: 0.1
      },
      numNodes: 5,
      degree: 3,
      keywords: ["Test", "hey", "lol"]
    },
    position: { x: 250, y: 200 }

  },
  {
    id: '3', type: 'cluster', data: {
      sentiment: {
        pos: 0.7,
        neg: 0.2,
        neu: 0.1
      },
      numNodes: 5,
      degree: 3,
      keywords: ["Test", "hey", "lol"]
    },
    position: { x: 250, y: 100 }
  },
  {
    id: '4', type: 'cluster', data: {
      sentiment: {
        pos: 0.7,
        neg: 0.2,
        neu: 0.1
      },
      numNodes: 5,
      degree: 3,
      keywords: ["Test", "hey", "lol"]
    },
    position: { x: 250, y: 200 }
  },
  { id: 'e1-2', source: '1', target: '2', animated: false },
  { id: 'e1-3', source: '1', target: '3', animated: false },
  { id: 'e1-4', source: '1', target: '4', animated: false }
];

const PopupContainer = styled.div`
  background: #202124;
  color: white;
  height: 400px;
  font-family: Inter;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
`

const DashboardContainer = styled.div`
  background: #202124;
  color: white;
  font-family: Inter;
  height: 100vh;
  display: flex;
`

const LoadingContainer = styled.div`
  background: #202124;
  color: white;
  font-family: Inter;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
`

const CurrentArticleHeader = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;  
  padding: 25px;
  background: #202124;
  border-bottom: 1px solid #292A2E; 
  gap: 20px;
`

const Tabs = styled.div`
  background: #292A2E;
  display: flex;
  align-items: center;
  justify-content: center;
`

const TabItem = styled.div`
  margin: 0 15px;
  padding: 20px;
  cursor: pointer;
  border-top: ${props => props.selected ? "3px solid white" : "none"};
`

const LeftSidebar = styled.div`
  background: #292A2E;
  height: 100vh;
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 50px;
`

const ArticleInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 7px;
`

const Source = styled.div`
  opacity: 0.5;
  font-size: 15px;
  font-family: Inter;
`

const Headline = styled.div`
  font-size: 20px;
  font-family: Inter-Bold;
  line-height: 25px;
`

const SentimentBar = styled.div`
  width: 100%;
  display: flex;
  height: 35px;
  border-radius: 6px;
`

const PositiveSentiment = styled.div`
  flex: ${props => props.value};
  background: #7ADD7E;
  border-top-left-radius: 6px;
  border-bottom-left-radius: 6px;
`

const NegativeSentiment = styled.div`
  flex: ${props => props.value};
  background: #FF8F51;
`

const NeutralSentiment = styled.div`
  flex: ${props => props.value};
  background: #4E4E4E;
  border-bottom-right-radius: 6px;
  border-top-right-radius: 6px;
`

const Article = styled.div`
  display: flex;
  flex-direction: column;
  gap: 30px;
`

const SentimentDescriptions = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`

const Descriptor = styled.div`
  color: ${props => props.color};
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: Inter-Bold;
  gap: 3px;
  font-size: 12px;

  div {
    background:${props => props.color}; 
  }
`

const DescriptorBox = styled.div`
  height: 8px;
  width: 8px;
  border-radius: 2px;
`

const Sentiment = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
`

const MainContent = styled.div`
  flex: 3;

`

const Keywords = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
`

const Keyword = styled.div`
  border-radius: 6px;
  background: #37383d;
  padding: 10px;
  font-size: 14px;
  color: white;
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
`

const App = () => {

  const [loadState, setLoadState] = useState("loading");
  const [selectedTab, setSelectedTab] = useState("first");
  const [currentArticleInfo, setCurrentArticleInfo] = useState(null)


  useEffect(() => {
    let views = chrome.extension.getViews({ type: "popup" });

    // If dashboard
    if (views.length == 0) {
      setLoadState("dashboard")

      // Get previous accessed tab (need to fix this...)
      chrome.tabs.query({
        active: false
      }, (tabs) => {
        let tab = tabs.reduce((previous, current) => {
          return previous.lastAccessed > current.lastAccessed ? previous : current;
        });

        chrome.storage.sync.get(tab.url, data => {
          setCurrentArticleInfo(data[tab.url])
        })

      });
    } else {

      // If popup
      setLoadState("popup")

      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.storage.sync.get(tabs[0].url, data => {
          setCurrentArticleInfo(data[tabs[0].url])
        })
      })

    }

  }, [])


  if (!currentArticleInfo) {
    return (
      <LoadingContainer>
        <Dimmer active>
          <Loader />
        </Dimmer>
      </LoadingContainer>
    )
  }

  if (loadState == "popup") {
    return (
      <PopupContainer>
        <CurrentArticleHeader>
          <Headline>
            {currentArticleInfo.headline}
          </Headline>
          <Sentiment>
            <SentimentBar>
              <PositiveSentiment value={currentArticleInfo.content_sentiment.pos} />
              <NegativeSentiment value={currentArticleInfo.content_sentiment.neg} />
              <NeutralSentiment value={currentArticleInfo.content_sentiment.neu} />
            </SentimentBar>
            <SentimentDescriptions>
              <Descriptor color="#7ADD7E">
                <DescriptorBox />
                {Math.round(currentArticleInfo.content_sentiment.pos * 100)}% Positive
                </Descriptor>
              <Descriptor color="#FF8F51">
                <DescriptorBox />
                {Math.round(currentArticleInfo.content_sentiment.neg * 100)}% Negative
                </Descriptor>
            </SentimentDescriptions>
          </Sentiment>
        </CurrentArticleHeader>

        <Tabs>
          <TabItem selected={selectedTab == "first" ? true : false} onClick={() => {
            setSelectedTab("first")
          }}>
            <AiFillAppstore color={selectedTab == "first" ? "white" : "#535760"} size="30px" />
          </TabItem>
          <TabItem selected={selectedTab == "second" ? true : false} onClick={() => {
            setSelectedTab("second")
          }}>
            <BsFillPeopleFill color={selectedTab == "second" ? "white" : "#535760"} size="30px" />
          </TabItem>
          <TabItem selected={selectedTab == "third" ? true : false} onClick={() => {
            // setSelectedTab("third")
            chrome.tabs.create({ active: true, url: '/popup.html' });
          }}>
            <AiFillSetting color={selectedTab == "third" ? "white" : "#535760"} size="30px" />
          </TabItem>
        </Tabs>

      </PopupContainer>
    )
  } else if (loadState == "dashboard") {
    return (
      <DashboardContainer>
        <LeftSidebar>
          <Article>
            <ArticleInfo>
              <Source>
                New York Times
              </Source>
              <Headline>
                {currentArticleInfo.headline}
              </Headline>
            </ArticleInfo>

            <Sentiment>
              <SentimentBar>
                <PositiveSentiment value={currentArticleInfo.content_sentiment.pos} />
                <NegativeSentiment value={currentArticleInfo.content_sentiment.neg} />
                <NeutralSentiment value={currentArticleInfo.content_sentiment.neu} />
              </SentimentBar>
              <SentimentDescriptions>
                <Descriptor color="#7ADD7E">
                  <DescriptorBox />
                  {Math.round(currentArticleInfo.content_sentiment.pos * 100)}% Positive
                </Descriptor>
                <Descriptor color="#FF8F51">
                  <DescriptorBox />
                  {Math.round(currentArticleInfo.content_sentiment.neg * 100)}% Negative
                </Descriptor>
              </SentimentDescriptions>
            </Sentiment>

            <Keywords>
              {Object.keys(currentArticleInfo.top_words).map((word) => {
                return (
                  <Keyword>{word}</Keyword>
                )
              })}
            </Keywords>

          </Article>
        </LeftSidebar>

        <MainContent>
          <ReactFlow elements={elements} nodeTypes={{ cluster: ClusterNode, main: MainNode }} />
        </MainContent>
      </DashboardContainer>
    )
  } else {
    return (
      <LoadingContainer>
        Loading
      </LoadingContainer>
    )
  }

}

export default App;
