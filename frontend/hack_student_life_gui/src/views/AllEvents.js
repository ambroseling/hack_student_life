import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState, Fragment, useEffect } from "react";
import { Row, Card, CardBody, CardTitle, CardText, Container, CardHeader, Button, Col } from "reactstrap";
import { faRightToBracket } from "@fortawesome/free-solid-svg-icons";
import RedirectButton from "../components/RedirectButton";
import Search from "../components/Search";
import Tags from "../components/Tags";
import FilterButton from "../components/FilterButton";
import { useEvents } from "../context/EventsContext";

function AllEvents() {
    const available_tags = ['music', 'general', 'sports', 'arts', 'academic', 'career', 'social', 'business', 'engineering', 'games', 'health', 'fitness', 'coding', 'other'];

    const dummyEvents = [
        { id: 1, title: "Career Fair", description: "Annual Spring Career Fair featuring top tech companies and startups", time: "10:00 AM", location: "Student Union Ballroom", tags: ["career", "business"]},
        { id: 2, title: "Research Symposium", description: "Undergraduate research presentations across all disciplines", time: "2:00 PM", location: "Science Center Auditorium", tags: ["academic", "engineering"]},
        { id: 3, title: "Club Fair", description: "Explore and join student organizations on campus", time: "11:00 AM", location: "Campus Quad", tags: ["social", "general"]},
        { id: 4, title: "Guest Speaker: Tech Innovation", description: "Industry leader discusses future of AI and robotics", time: "4:00 PM", location: "Engineering Building Room 101", tags: ["engineering", "coding"]},
        { id: 5, title: "Cultural Festival", description: "Celebrate diversity with food, performances and activities", time: "12:00 PM", location: "Student Center Plaza", tags: ["arts", "music"]},
        { id: 6, title: "Wellness Workshop", description: "Learn stress management and mindfulness techniques", time: "3:00 PM", location: "Health Center Conference Room", tags: ["health", "fitness"]},
        { id: 7, title: "Hackathon Kickoff", description: "24-hour coding competition with amazing prizes", time: "6:00 PM", location: "Computer Science Building", tags: ["coding", "games"]},
        { id: 8, title: "Art Exhibition Opening", description: "Student artwork showcase and gallery reception", time: "5:00 PM", location: "Fine Arts Gallery", tags: ["arts", "general"]},
        { id: 9, title: "Sports Tournament", description: "Intramural basketball championship games", time: "1:00 PM", location: "Recreation Center Courts", tags: ["sports", "fitness"]},
        { id: 10, title: "Study Abroad Fair", description: "Learn about international exchange programs", time: "11:30 AM", location: "International Center", tags: ["academic", "general"]},
    ];

    const { events, loading, error } = useEvents();
    const [search, setSearch] = useState("");
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [tags, setTags] = useState([]);
    const [modalOpen, setModalOpen] = useState(false);

    // creating booleans filter buttons so its toggleable
    const [eventTags, setEventTags] = useState(available_tags);
    const [toggledTags, setToggledTags] = useState({});
    const [filteredEvents, setFilteredEvents] = useState(dummyEvents);

    useEffect(() => {
        // Initialize state for each tag
        const initialToggledState = {};
        available_tags.forEach(tag => {
            initialToggledState[tag] = false;
        });
        setToggledTags(initialToggledState);
    }, []);

    useEffect(() => {
        const areAnyTagsToggled = Object.values(toggledTags).some(isToggled => isToggled);
        if (areAnyTagsToggled) {
            const filtered = dummyEvents.filter(event => event.tags.some(tag => toggledTags[tag]));
            setFilteredEvents(filtered);
        } else {
            setFilteredEvents(dummyEvents);
        }
    }, [toggledTags]);

    const addTag = (newTag) => {
        setEventTags([...eventTags, newTag]);
        setToggledTags({ ...toggledTags, [newTag]: false });
    };

    const handleToggle = (tag) => {
        setToggledTags(prevState => ({
            ...prevState,
            [tag]: !prevState[tag]
        }));
    };

    return (
        <Fragment>
            <div>
                <div id="box">
                    
                    {/* <img src="hack_student_life/frontend/hack_student_life_gui/uoftlogo.jpg" alt="uoft" /> */}



                    {/* title */}
                    <Row className="ml-1" style={{ display: "flex" }}>
                        <h1 className="font-weight-bold" style={{ align: "left", display: "flex" }}>MeetingPlace</h1>
                        <h6 style={{ align: "right", display: "flex" }}>everything, everywhere, all at uoft</h6>
                    </Row>

                    {/* This is the search bar and the filter buttons underneath */}
                    <Row className="row-cols-lg-auto mt-4 align-items-center">
                        <Search />
                        <Row>
                            {available_tags.map((tag, index) => (
                                <Col key={index}>
                                    <FilterButton tag={tag} isToggled={toggledTags[tag]} onToggle={handleToggle} />
                                </Col>
                            ))}
                        </Row>
                    </Row>
                </div>

                <div id="bottombox"/>
                
                <Container fluid="md" className="bulletin-board">
                    <Row>
                        {filteredEvents.map((event, index) => (
                            <Col lg="4" md="6" sm="12" className="mb-4" key={index}>
                                <Card className="card"> {/* apply the card class */}
                                    <CardBody className="card-body"> {/* apply the card-body class */}
                                        <CardHeader tag="h3" style={{ backgroundColor: "white" }}>{event.title}</CardHeader>
                                        <CardText>{event.description}</CardText>
                                        <CardText>{event.time}</CardText>
                                        <CardText>{event.location}</CardText>
                                        <RedirectButton icon={faRightToBracket} link={`/event/${event.id}`} />
                                        <div className="tags-container">
                                            {event.tags.map((tag, index) => (
                                                <Tags tag={tag} key={index} />
                                            ))}
                                        </div>
                                    </CardBody>
                                </Card>
                            </Col>
                        ))}
                    </Row>
                </Container>
            </div>
        </Fragment>
    );
}

export default AllEvents;
