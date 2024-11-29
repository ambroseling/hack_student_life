import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState, Fragment } from "react";
import { Row, Card, CardBody, CardTitle, CardText, Container, CardHeader, Button, Col } from "reactstrap";
import { faRightToBracket } from "@fortawesome/free-solid-svg-icons";
import RedirectButton from "../components/RedirectButton";
import Search from "../components/Search";
import Tags from "../components/Tags";
import FilterButton from "../components/FilterButton";
import { useEvents } from "../context/EventsContext";


function AllEvents() {
    const dummyEvents = [
        { id: 1, title: "Career Fair", description: "Annual Spring Career Fair featuring top tech companies and startups", time: "10:00 AM", location: "Student Union Ballroom", tags: ["tag1", "tag2"]},
        { id: 2, title: "Research Symposium", description: "Undergraduate research presentations across all disciplines", time: "2:00 PM", location: "Science Center Auditorium", tags: ["tag3", "tag4"]},
        { id: 3, title: "Club Fair", description: "Explore and join student organizations on campus", time: "11:00 AM", location: "Campus Quad", tags: ["social", "tag3"]},
        { id: 4, title: "Guest Speaker: Tech Innovation", description: "Industry leader discusses future of AI and robotics", time: "4:00 PM", location: "Engineering Building Room 101", tags: ["tag2", "tag4"]},
        { id: 5, title: "Cultural Festival", description: "Celebrate diversity with food, performances and activities", time: "12:00 PM", location: "Student Center Plaza", tags: ["tag1", "tag4"]},
        { id: 6, title: "Wellness Workshop", description: "Learn stress management and mindfulness techniques", time: "3:00 PM", location: "Health Center Conference Room", tags: ["tag2", "tag3"]},
        { id: 7, title: "Hackathon Kickoff", description: "24-hour coding competition with amazing prizes", time: "6:00 PM", location: "Computer Science Building", tags: ["tag1", "tag2"]},
        { id: 8, title: "Art Exhibition Opening", description: "Student artwork showcase and gallery reception", time: "5:00 PM", location: "Fine Arts Gallery", tags: ["tag3", "tag4"]},
        { id: 9, title: "Sports Tournament", description: "Intramural basketball championship games", time: "1:00 PM", location: "Recreation Center Courts", tags: ["tag2", "tag4"]},
        { id: 10, title: "Study Abroad Fair", description: "Learn about international exchange programs", time: "11:30 AM", location: "International Center", tags: ["tag1", "tag3"]},
    ];
    const available_tags = ['music', 'general', 'sports', 'arts', 'academic', 'career', 'social', 'business','engineering','games','health','fitness','coding','other']
    const {events, loading, error } = useEvents();
    const [search, setSearch] = useState("");
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [tags, setTags] = useState([]);
    const [modalOpen, setModalOpen] = useState(false);
    const filteredEvents = dummyEvents.filter((event) => {  //dummy events to use fake 
        return (
            (event.title.toLowerCase().includes(search.toLowerCase())) &&
            tags.every((tag) => event.tags.includes(tag))
        );
    });
    return <Fragment>
        <div>

            <div id="box">

                    {/* title */}
                    <Row className="ml-1" style = {{display: "flex"}}>
                        <h1 className="font-weight-bold" style = {{align: "left", display :"flex"}}>Project Name</h1> 
                        <h6 style = {{align: "right", display :"flex"}}>everything, everywhere, all at uoft</h6>
                    </Row>

                    {/* This is the search bar and the filter buttons underneath */}
                    <Row className="row-cols-lg-auto mt-4 align-items-center">
                        <Search/>
                        <Row>
                            {
                                available_tags.map((tag, index) => ( 
                                    <Col>
                                        <FilterButton key={index} tag={tag} />
                                    </Col>
                                ))
                            }
                        </Row>                       
                    </Row>
            </div>
        
            <div id="leftbox"></div>
            <div id="rightbox"></div>
            <div id="bottombox"></div>

            <Container fluid="md" className="bulletin-board">
                {
                    filteredEvents.map((event, index) => (
                        <Row className="mb-2">
                            <Card color = "primary">
                                <CardBody>
                                    <CardHeader tag="h3">{event.title}</CardHeader>
                                    <CardText>{event.description}</CardText>
                                    <CardText>{event.time}</CardText>
                                    <CardText>{event.location}</CardText>
                                    <RedirectButton icon={faRightToBracket} link={`/event/${event.id}`} />
                                    {event.tags.map((tag, index) => (
                                        <Tags tag={tag} key={index} />
                                    ))}
                                </CardBody>
                            </Card>
                        </Row>
                    ))
                }
            </Container>

        </div>
    </Fragment>;
}

export default AllEvents;
