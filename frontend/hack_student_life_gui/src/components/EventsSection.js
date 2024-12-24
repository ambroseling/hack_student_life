import React, { Fragment } from 'react';
import { Container,Row, Col, Card, CardBody, CardTitle, CardText } from 'reactstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCalendarDays, faLocationDot, faRightToBracket } from '@fortawesome/free-solid-svg-icons';
import RedirectButton from './RedirectButton';
import Tags from './Tags';

const EventsSection = ({events,title}) => {
  return (
  <Fragment>
<h2 style={{
                    textDecoration: 'none',
                    color: '#333',
                    fontWeight: 'bold'
                }}>{title}</h2>
    {events.length === 0 ? (
        <Row className="mb-2">
            <Card>
                <CardBody>
                    <CardTitle tag="h3">No events found</CardTitle>
                </CardBody>
            </Card>
        </Row>
    ) : (                                                                                                                                                                                                                                                                                                                                              
        <Container style={{ overflowX: 'auto', whiteSpace: 'nowrap', padding: '20px' }}>
        <div  style={{ display: 'flex' }}>
       {events.map((event) => (
           <Col style={{marginRight:'20px'}}>
                <Card style={{width: '500px'}}>
                    <CardBody>
                        <CardTitle tag="h3">{event.title}</CardTitle>
                        <CardText>{event.description}</CardText>
                        {event.date && <CardText>
                            <FontAwesomeIcon icon={faCalendarDays} style={{marginRight:'5px'}}/>
                            {event.date.toLocaleString()}
                            </CardText>}
                        <CardText>
                        <FontAwesomeIcon icon={faLocationDot} />                            {event.location}
                            </CardText>
                        <RedirectButton icon={faRightToBracket} link={event.source_url} />
                        {console.log(event.tags)}
                        {event.tags.map((tag) => (
                            <Tags tag={tag} />
                        ))}
                    </CardBody>
                </Card>
            </Col>
        ))}
        </div>
        </Container>
    )}
    </Fragment>);
  
};

export default EventsSection;
