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
import ArticleNode from './helpers/articleNode'
import { BiHomeAlt } from "react-icons/bi"


const NavButtons = styled.div`
  position: absolute;
  bottom: 0;
  left: 0;
`

const HomeButton = styled.div`
  opacity: 0.5;
  color: white;
  padding: 30px;
  cursor: pointer;
`

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
  gap: 30px;
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

  .react-flow__node {
    cursor: pointer !important;
  }

  .react-flow__handle.connectable {
    cursor: pointer !important;
  }
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

const HoverInfo = styled.div`
  background: #393a3f;
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  padding: 20px;
`

const HoverInfoTitle = styled.div`
  font-size: 25px;
  font-family: Inter-Bold;
`

const HoverInfoSummary = styled.div`
  font-size: 15px;
  opacity: 0.5;
  font-family: Inter;
`
const clusters = [
  {
    id: '1', type: 'main', data: {
      label: 'Perspectives'
    },
    position: { x: (966 / 2) - 125, y: (766 / 2) - 60 }
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
    position: { x: (966 / 2) + 200, y: (766 / 2) - 60 }
  },
  {
    id: '4', type: 'cluster', data: {
      sentiment: {
        pos: 1.1,
        neg: 0.2,
        neu: 0.1
      },
      numNodes: 5,
      degree: 3,
      keywords: ["Test", "hey", "lol"]
    },
    position: { x: (966 / 2) - 400, y: (766 / 2) - 60 }
  },
  { id: 'e1-2', source: '1', target: '2', animated: false },
  { id: 'e1-3', source: '1', target: '3', animated: false },
  { id: 'e1-4', source: '1', target: '4', animated: false }
];

const articles = [
  {
    id: '1', type: 'article', data: {
      url: "http://google.com",
      headline: "Headline 1",
      summary: ["hello there", "this is great"],
      keywords: ["Top", "Low"],
      cluster_id: "2",
      sentiment: {
        pos: 1.1,
        neg: 0.2,
        neu: 0.1
      },
    },
    position: { x: 200, y: 200 }
  },
  {
    id: '2', type: 'article', data: {
      url: "http://bing.com",
      headline: "Headline 2",
      summary: ["hello there", "this is great"],
      keywords: ["Top", "Low", "Amazon", "Jeff Bezos"],
      cluster_id: "2",
      sentiment: {
        pos: 1.1,
        neg: 0.2,
        neu: 0.1
      },
    },
    position: { x: 250, y: 250 }
  },
  {
    id: '3', type: 'article', data: {
      url: "http://aol.com",
      headline: "Headline 3",
      summary: ["hello there", "this is great"],
      keywords: ["Top", "Low"],
      cluster_id: "2",
      sentiment: {
        pos: 1.1,
        neg: 0.2,
        neu: 0.1
      },
    },
    position: { x: 350, y: 350 }
  },
  {
    id: '4', type: 'article', data: {
      url: "http://yahoo.com",
      headline: "Headline 4",
      summary: ["hello there", "this is great"],
      keywords: ["Top", "Low"],
      cluster_id: "2",
      sentiment: {
        pos: 1.1,
        neg: 0.2,
        neu: 0.1
      },
    },
    position: { x: 100, y: 100 }
  },
  {
    id: 'e1-2', source: '1', target: '2', data: {
      similarity: 0.5
    }
  },
  {
    id: 'e1-3', source: '1', target: '3', data: {
      similarity: 0.7
    }
  }
];

const App = () => {

  const [loadState, setLoadState] = useState("loading");
  const [selectedTab, setSelectedTab] = useState("first");
  const [currentArticleInfo, setCurrentArticleInfo] = useState(null)

  const [hoverInfo, setHoverInfo] = useState(null)
  const [dashboardView, setDashboardView] = useState({
    view: "cluster",
    data: null
  })
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
              {currentArticleInfo.top_words.map((word) => {
                return (
                  <Keyword>{word.word}</Keyword>
                )
              })}
            </Keywords>

          </Article>
          {hoverInfo ?
            <HoverInfo>
              <HoverInfoTitle>
                {hoverInfo.title}
              </HoverInfoTitle>
              <HoverInfoSummary>
                <ul>
                  {hoverInfo.summary.map((sentence => {
                    return (
                      <li>{sentence}</li>
                    )
                  }))}
                </ul>
              </HoverInfoSummary>
            </HoverInfo>
            : null}

          <NavButtons>
            {dashboardView.view == "article" ?
              <HomeButton
                onClick={() => {
                  setDashboardView({ view: 'cluster', data: null })
                }}
              >
                <BiHomeAlt size="36px" />
              </HomeButton>
              : null}
          </NavButtons>
        </LeftSidebar>


        <MainContent>
          <ReactFlow
            elements={dashboardView.view == "cluster" ? clusters :
              [...articles.filter(article => article.data && article.data.cluster_id == dashboardView.data.cluster_id), ...articles.filter(article => article.source)]
            }
            nodeTypes={{ cluster: ClusterNode, main: MainNode, article: ArticleNode }}
            elementsSelectable={false}
            nodesConnectable={false}
            onNodeDoubleClick={(e, node) => {

              if (node.type == 'cluster') {
                setDashboardView({
                  view: "article", data: {
                    cluster_id: node.id
                  }
                })
              }

              if (node.type == 'article') {
                window.location.href = node.data.url;
              }

            }}
            onNodeMouseEnter={(e, node) => {
              if (node.type == 'article') {
                setHoverInfo({
                  title: node.data.headline,
                  summary: node.data.summary
                })
              }
            }}
            onNodeMouseLeave={(e, node) => {
              setHoverInfo(null)
            }}

            onEdgeMouseEnter={(e, edge) => {
              setHoverInfo({
                title: "Edge Similarity",
                summary: [edge.data.similarity]
              })
            }}
          />
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
