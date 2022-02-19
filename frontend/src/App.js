/*global chrome*/
import React, { useEffect, useState } from 'react'
import './App.css';
import styled from 'styled-components'
import { AiFillAppstore, AiFillSetting } from "react-icons/ai";
import { BsFillPeopleFill } from "react-icons/bs";

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
  justify-content: center;
  align-items: center;  
  padding: 25px;
  background: #202124;
  border-bottom: 1px solid #292A2E; 
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

const App = () => {

  const [loadState, setLoadState] = useState("loading");
  const [selectedTab, setSelectedTab] = useState("first");

  useEffect(() => {
    let views = chrome.extension.getViews({ type: "popup" });

    if (views.length == 0) {
      setLoadState("dashboard")
    } else {
      setLoadState("popup")
    }

  }, [])

  if (loadState == "popup") {
    return (
      <PopupContainer>
        {/* <div
          onClick={() => {
            chrome.tabs.create({ active: true, url: '/popup.html' });
          }}
        >
          Hello
        </div> */}

        <CurrentArticleHeader>
          Sentiment Analysis
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
