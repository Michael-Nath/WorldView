import react from 'react';
import styled from 'styled-components'
import { Handle } from 'react-flow-renderer';
import { Button } from 'semantic-ui-react';

const Container = styled.div`
  background: #393a3f;
  border-radius: 8px;
  padding: 20px;
  width: 200px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  color: white;
  font-family: Inter-Bold;
  font-size: 15px;
  box-shadow: 5px 5px 38px -14px rgba(0,0,0,0.5);
`

const ClusterStats = styled.div`
  display: flex;
`

const NumNodes = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
`

const NumNodeNum = styled.div`
  font-size: 30px;
`

const NumNodeDescriptor = styled.div`
  font-size: 12px;
  font-family: Inter;
`

const NodeDegrees = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 5px;
`
const NodeDegreesNum = styled.div`
  font-size: 30px;
`

const NodeDegreesDescriptor = styled.div`
  font-size: 12px;
  font-family: Inter;
`

const SentimentBar = styled.div`
  width: 100%;
  display: flex;
  height: 20px;
  border-radius: 6px;
`

const Sentiment = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
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

const CustomButton = styled(Button)`
  background: rgba(255,255,255,0.1) !important;
  color: rgba(255,255,255,0.5) !important;
  font-family: Inter !important;
  font-size: 12px !important;
`

const ClusterNode = ({ data }) => {
  return (
    <>

      <Handle
        type="target"
        position="left"
      />
      <Container>

        <ClusterStats>
          <NumNodes>
            <NumNodeNum>
              {data.numNodes}
            </NumNodeNum>
            <NumNodeDescriptor>
              articles
          </NumNodeDescriptor>

          </NumNodes>
          <NodeDegrees>
            <NodeDegreesNum>
              {data.degree}
            </NodeDegreesNum>
            <NodeDegreesDescriptor>
              strength
          </NodeDegreesDescriptor>
          </NodeDegrees>
        </ClusterStats>
        <Sentiment>
          <SentimentBar>
            <PositiveSentiment value={data.sentiment.pos} />
            <NegativeSentiment value={data.sentiment.neg} />
            <NeutralSentiment value={data.sentiment.neu} />
          </SentimentBar>
        </Sentiment>
      </Container>

      <Handle
        type="source"
        position="right"
      />
    </>
  )
}

export default ClusterNode