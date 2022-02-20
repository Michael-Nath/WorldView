import react from 'react';
import styled from 'styled-components'
import { Handle } from 'react-flow-renderer';

const Container = styled.div`
  background: #393a3f;
  border-radius: 8px;
  padding: 40px;
  color: white;
  font-family: Inter-Bold;
  font-size: 15px;
  box-shadow: 5px 5px 38px -14px rgba(0,0,0,0.5);
`


const ClusterNode = ({ data }) => {
  return (
    <Container>
      <Handle
        type="target"
        position="left"
      />
      Positive: {data.sentiment.pos} <br />
      Negative: {data.sentiment.neg} <br />
      Neutral: {data.sentiment.neu} <br />
      Num Nodes: {data.numNodes} <br />
      Degree: {data.degree} <br />
      <Handle
        type="source"
        position="right"
      />
    </Container>

  )
}

export default ClusterNode