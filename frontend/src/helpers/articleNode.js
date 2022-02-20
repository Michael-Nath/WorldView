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
`

const Headline = styled.div`

`


const ArticleNode = ({ data }) => {
  return (
    <Container>
      <Handle
        type="target"
        position="left"
      />
      <Headline>
        {data.headline}
      </Headline>
      <Handle
        type="source"
        position="right"
      />
    </Container>
  )
}

export default ArticleNode