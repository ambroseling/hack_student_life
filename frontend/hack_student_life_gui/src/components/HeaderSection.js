import React from 'react';
import { Container, Row, Col , Card, CardBody, CardTitle} from 'reactstrap';

const HeaderSection = () => {
  return (
    <Container className="header-section my-5 mx-auto" style={{ maxWidth: '80%' }}>
      <Row>
        <Col xs={4}>
        <h1 style={{
                    textDecoration: 'none',
                    color: '#333',
                    fontWeight: 'bold',
                    fontSize: '70px'
                }}>Everything  Everywhere  All at UofT</h1>
        </Col>
        <Col >
        <Card>
            <CardBody>
                <CardTitle tag="h3">LIVE NOW</CardTitle>
            </CardBody>
        </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default HeaderSection;