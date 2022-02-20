/*global chrome*/
import React, { useEffect, useState } from 'react'
import './App.css';
import styled from 'styled-components'
import { AiFillAppstore } from "react-icons/ai";
import { BsFillPeopleFill } from "react-icons/bs";
import { Loader, Dimmer } from 'semantic-ui-react'
import ReactFlow from 'react-flow-renderer';
import ClusterNode from './helpers/clusterNode'
import MainNode from './helpers/mainNode'
import CustomEdge from './helpers/customEdge'
import ArticleNode from './helpers/articleNode'
import { BiHomeAlt, BiArrowBack, BiNetworkChart } from "react-icons/bi"


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
  border-radius: 6px;
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
  justify-content: center;
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
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
  padding: 7px;
  font-size: 10px;
  color: white;
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  line-height: 12px;
`

const HoverInfo = styled.div`
  background: #393a3f;
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  padding: 20px;
  gap: 10px;
`

const HoverInfoTitle = styled.div`
  font-size: 17px;
  font-family: Inter-Bold;
`

const HoverInfoSummary = styled.div`
  font-size: 12px;
  line-height: 15px;
  opacity: 0.5;
  font-family: Inter;
`

const DiversitySummary = styled.div`
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 15px;
  overflow-y: auto;
  padding-bottom: 100px;
`
const DiversityArticle = styled.div`
  border-radius: 8px;
  background: rgba(255,255,255,0.1);
  padding: 15px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  cursor: pointer;

  &&:hover {
    background: rgba(255,255,255,0.25);
  }
`

const ArticleLeft = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
`
const ArticleLeftHeadline = styled.div`
  font-family: Inter-Bold;
`

const ArticleLeftSubTitle = styled.div`
  opacity: 0.3;
  font-size: 10px;
`

const ArticleRight = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: Inter-Bold;
  font-size: 20px;
  flex-direction: column;
`

const ProgressBar = styled.div`
  height: 2px; 
  background: #7ADD7E;
  position: absolute;
  bottom: 0;
  left: 0;
  width: ${props => props.progress}%;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
`

const SpecificPage = styled.div`
  padding: 20px;
`

const BackButton = styled(BiArrowBack)`
  cursor: pointer;
  margin-bottom: 15px;
`

const ArticleRightMain = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`
const w = Math.random() * 2 * Math.PI;
const x = Math.random() * 2 * Math.PI;
const y = Math.random() * 2 * Math.PI;
const z = Math.random() * 2 * Math.PI;

const clusters = [
  {
    id: '1', type: 'main', data: {
      label: 'Perspectives'
    },
    position: { x: 358, y: 323 }
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
    position: { x: 358 + (Math.cos(x) * 300), y: 323 + (Math.sin(x) * 300) }

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
    position: { x: 358 + (Math.cos(y) * 300), y: 323 + (Math.sin(y) * 300) }
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
    position: { x: 358 + (Math.cos(z) * 300), y: 323 + (Math.sin(z) * 300) }
  },
  {
    id: 'ec1-2', source: '1', target: '2'
  },
  {
    id: 'ec1-3', source: '1', target: '3'
  },
  {
    id: 'ec1-4', source: '1', target: '4'
  }
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
    id: 'e1-2', type: 'custom', source: '1', target: '2', label: 0.5, data: {
      similarity: 0.5
    }
  },
  {
    id: 'e1-3', type: 'custom', source: '1', target: '3', label: 0.4, data: {
      similarity: 0.7
    }
  }
];

const App = () => {

  const [loadState, setLoadState] = useState("loading");
  const [selectedTab, setSelectedTab] = useState("first");
  const [pageType, setPageType] = useState({
    type: "normal",
    data: null
  })
  const [pageType2, setPageType2] = useState({
    type: "normal",
    data: null
  })
  const [currentArticleInfo, setCurrentArticleInfo] = useState(null)
  const [currentPerspectives, setCurrentArticlePerspectives] = useState(null)

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

      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.storage.sync.get(tabs[0].url + "_perspectives", data => {
          setCurrentArticlePerspectives(data[tabs[0].url + "_perspectives"])
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
        {selectedTab == "first" ?
          <>
            {pageType.type == "normal" ?
              <>
                <CurrentArticleHeader>
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
                    {currentArticleInfo.top_words.slice(0, 4).map((word) => {
                      return (
                        <Keyword>{word.word}</Keyword>
                      )
                    })}
                  </Keywords>

                </CurrentArticleHeader>

                {currentPerspectives ?
                  <DiversitySummary>
                    {currentPerspectives.clusters.map((cluster) => {

                      const article = currentPerspectives.articles.find(item => item.data.cluster_id == cluster.id);

                      if (article) {
                        return (
                          <DiversityArticle
                            onClick={() => {
                              setPageType({
                                type: 'specific', data: {
                                  headline: article.data.headline,
                                  summary: article.data.summary
                                }
                              })
                            }}
                          >
                            <ArticleLeft>
                              <ArticleLeftHeadline>
                                {article.data.headline}
                              </ArticleLeftHeadline>
                            </ArticleLeft>
                            <ArticleRight>
                              <ArticleRightMain>
                                50%
                              </ArticleRightMain>
                              <ArticleLeftSubTitle>
                                similar
                              </ArticleLeftSubTitle>
                            </ArticleRight>
                          </DiversityArticle>
                        )
                      } else {
                        return null
                      }

                    })}

                  </DiversitySummary>
                  : <Loader />}
              </>
              : pageType.type == "specific" ?
                <SpecificPage>
                  <BackButton color="white" size="20px" onClick={() => {
                    setPageType({
                      type: 'normal',
                      data: null
                    })
                  }} />
                  <ArticleLeftHeadline>{pageType.data.headline}</ArticleLeftHeadline>

                  <ul>
                    {pageType.data.summary.map(sentence => {
                      return (
                        <li>{sentence}</li>
                      )
                    })}
                  </ul>
                </SpecificPage>
                : null
            }
          </>
          : selectedTab == "second" ?
            <DiversitySummary>
              <Headline>Perspectives</Headline>

              {currentPerspectives ?
                <>
                  {currentPerspectives.clusters.map((cluster, i) => {
                    return (
                      <DiversityArticle>
                        <ArticleLeft>
                          <ArticleLeftHeadline>
                            Perspective {i + 1}
                          </ArticleLeftHeadline>

                        </ArticleLeft>
                        <ArticleRight>
                          <ArticleRightMain>
                            {cluster.data.numNodes}
                          </ArticleRightMain>
                          <ArticleLeftSubTitle>
                            articles
                        </ArticleLeftSubTitle>
                        </ArticleRight>
                      </DiversityArticle>
                    )
                  })}
                </>
                : null}

            </DiversitySummary>

            : null
        }


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
            <BiNetworkChart color={selectedTab == "third" ? "white" : "#535760"} size="30px" />
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
              {currentArticleInfo.top_words.slice(0, 15).map((word) => {
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
                {hoverInfo.summary.map((sentence => {
                  return (
                    <>
                      {sentence} <br />
                    </>
                  )
                }))}
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
            edgeTypes={{ custom: CustomEdge }}
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
