import react from 'react';
import styled from 'styled-components'
import { Handle } from 'react-flow-renderer';

const Container = styled.div`
  background: #4e5056;
  border-radius: 8px;
  padding: 50px;
  color: white;
  font-family: Inter-Bold;
  font-size: 25px;
  box-shadow: 5px 5px 38px -14px rgba(0,0,0,0.5);
`


const MainNode = ({ data }) => {
  return (
    <Container>
      <Handle
        type="target"
        position="left"
      />
      {data.label}
      <Handle
        type="source"
        position="right"
      />
    </Container>
  )
}

export default MainNode