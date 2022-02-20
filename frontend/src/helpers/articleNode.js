import react from 'react';
import styled from 'styled-components'
import { Handle } from 'react-flow-renderer';

const Container = styled.div`
  background: #4e5056;
  border-radius: 8px;
  padding: 15px;
  color: white;
  font-family: Inter-Bold;
  font-size: 15px;
  box-shadow: 5px 5px 38px -14px rgba(0,0,0,0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  width: 150px;
`

const Summary = styled.div`
  font-size: 13px;
  font-family: Inter;
  opacity: 0.7;
`

const Headline = styled.div`

`

const SentimentBar = styled.div`
  width: 100%;
  display: flex;
  height: 15px;
  border-radius: 3px;
`

const PositiveSentiment = styled.div`
  flex: ${props => props.value};
  background: #7ADD7E;
  border-top-left-radius: 3px;
  border-bottom-left-radius: 3px;
`

const NegativeSentiment = styled.div`
  flex: ${props => props.value};
  background: #FF8F51;
`

const NeutralSentiment = styled.div`
  flex: ${props => props.value};
  background: #202124;
  border-bottom-right-radius: 3px;
  border-top-right-radius: 3px;
`

const Sentiment = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
`
const Keywords = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
`

const Keyword = styled.div`
  border-radius: 6px;
  background: #37383d;
  padding: 5px 10px;
  font-size: 10px;
  color: white; 
  font-family: Inter;
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  line-height: 14px;
`

const ArticleNode = ({ data }) => {
  return (
    <>
      <Handle
        type="target"
        position="left"
      />

      <Container>

        <Headline>
          {data.headline}
        </Headline>
        <Sentiment>
          <SentimentBar>
            <PositiveSentiment value={data.content_sentiment.pos} />
            <NegativeSentiment value={data.content_sentiment.neg} />
            <NeutralSentiment value={data.content_sentiment.neu} />
          </SentimentBar>
        </Sentiment>
        {/* <Keywords>
          {data.keywords.map(word => {
            return (
              <Keyword>{word}</Keyword>
            )
          })}
        </Keywords> */}

      </Container>

      <Handle
        type="source"
        position="right"
      />
    </>
  )
}

export default ArticleNode