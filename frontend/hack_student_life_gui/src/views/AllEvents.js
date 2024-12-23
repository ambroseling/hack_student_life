import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState, Fragment, useEffect } from "react";
import { Row, Card, CardBody, CardTitle, CardText, Container, CardHeader, Button, Col } from "reactstrap";
import { faRightToBracket } from "@fortawesome/free-solid-svg-icons";
import RedirectButton from "../components/RedirectButton";
import Search from "../components/Search";
import Tags from "../components/Tags";
import FilterButton from "../components/FilterButton";
import SortDropDown from "../components/SortDropDown";
import Retrieve from "../components/Retrieve";
import NavBar from "../components/NavBar";
import { useEvents } from "../context/EventsContext";

function AllEvents() {
    const available_tags = ['music', 'general', 'sports', 'arts', 'academic', 'career', 'social', 'business', 'engineering', 'games', 'health', 'fitness', 'coding', 'other'];

    const dummyEvents = [
        { id: 1, title: "Career Fair", description: "Annual Spring Career Fair featuring top tech companies and startups", date: new Date('2024-03-20T10:00:00'), location: "Student Union Ballroom", tags: ["career", "business"] },
        { id: 2, title: "Research Symposium", description: "Undergraduate research presentations across all disciplines", date: new Date('2024-04-15T14:00:00'), location: "Science Center Auditorium", tags: ["academic", "engineering"] },
        { id: 3, title: "Club Fair", description: "Explore and join student organizations on campus", date: new Date('2024-02-10T11:00:00'), location: "Campus Quad", tags: ["social", "general"] },
        { id: 4, title: "Guest Speaker: Tech Innovation", description: "Industry leader discusses future of AI and robotics", date: new Date('2024-05-05T16:00:00'), location: "Engineering Building Room 101", tags: ["engineering", "coding"] },
        { id: 5, title: "Cultural Festival", description: "Celebrate diversity with food, performances and activities", date: new Date('2024-03-25T12:00:00'), location: "Student Center Plaza", tags: ["arts", "music"] },
        { id: 6, title: "Wellness Workshop", description: "Learn stress management and mindfulness techniques", date: new Date('2024-03-15T15:00:00'), location: "Health Center Conference Room", tags: ["health", "fitness"] },
        { id: 7, title: "Hackathon Kickoff", description: "24-hour coding competition with amazing prizes", date: new Date('2024-06-01T18:00:00'), location: "Computer Science Building", tags: ["coding", "games"] },
        { id: 8, title: "Art Exhibition Opening", description: "Student artwork showcase and gallery reception", date: new Date('2024-04-20T17:00:00'), location: "Fine Arts Gallery", tags: ["arts", "general"] },
        { id: 9, title: "Sports Tournament", description: "Intramural basketball championship games", date: new Date('2024-03-30T13:00:00'), location: "Recreation Center Courts", tags: ["sports", "fitness"] },
        { id: 10, title: "Study Abroad Fair", description: "Learn about international exchange programs", date: new Date('2024-04-10T11:30:00'), location: "International Center", tags: ["academic", "general"] },
    ];

    const {recommendedEvents, setRecommendedEvents} = useState("");
    // const { events, loading, error, fetchEvents } = useEvents();
    const [search, setSearch] = useState("");
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [tags, setTags] = useState([]);
    const [modalOpen, setModalOpen] = useState(false);
    const [sortOption, setSortOption] = useState("asc");

    const [eventTags, setEventTags] = useState(available_tags);
    const [toggledTags, setToggledTags] = useState({});
    const [filteredEvents, setFilteredEvents] = useState(dummyEvents);

    useEffect(() => {
        const initialToggledState = {};
        available_tags.forEach(tag => {
            initialToggledState[tag] = false;
        });
        setToggledTags(initialToggledState);
    }, []);

    useEffect(() => {
        const areAnyTagsToggled = Object.values(toggledTags).some(isToggled => isToggled);
        if (areAnyTagsToggled) {
            const filtered = filteredEvents.filter(event => event.tags.some(tag => toggledTags[tag]));
            setFilteredEvents(filtered);
        } else {
            setFilteredEvents(filteredEvents);
        }
    }, [toggledTags, dummyEvents]);

    const handleToggle = (tag) => {
        setToggledTags(prevState => ({
            ...prevState,
            [tag]: !prevState[tag]
        }));
    };

    const handleSearch = (searchValue) => {
        // fetchEvents(searchValue);
    };

    const sortedEvents = filteredEvents.sort((a, b) => {
        if (sortOption === 'asc') {
            return a.date - b.date;
        } else {
            return b.date - a.date;
        }
    });

    return (
        <Fragment>
        <div>
        <br/>
        <NavBar />
    <br/>
    <Container  className="text-center">
    <h1 style={{
                    textDecoration: 'none',
                    color: '#333',
                    fontWeight: 'bold'
                }}>Everything, Everywhere, All at UofT</h1>
    </Container>
    <div>
    <br/>
    <Search onSearchChange={handleSearch}/>
    <br/>
    <h2>Events for You</h2>
    {filteredEvents.length === 0 ? (
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
       {filteredEvents.map((event) => (
           <Col style={{marginRight:'20px'}}>
                <Card>
                    <CardBody>
                        <CardTitle tag="h3">{event.title}</CardTitle>
                        <CardText>{event.description}</CardText>
                        {/* <CardText>{event.time}</CardText> */}
                        {event.date && <CardText>Date: {event.date.toLocaleString()}</CardText>}
                        <CardText>{event.location}</CardText>
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

    <h2>Career</h2>
</div>

</div>
        </Fragment>
    );
}

export default AllEvents;
