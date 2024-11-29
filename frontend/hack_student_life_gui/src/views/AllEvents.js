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

    const { events, loading, error } = useEvents();
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
            const filtered = dummyEvents.filter(event => event.tags.some(tag => toggledTags[tag]));
            setFilteredEvents(filtered);
        } else {
            setFilteredEvents(dummyEvents);
        }
    }, [toggledTags]);

    const handleToggle = (tag) => {
        setToggledTags(prevState => ({
            ...prevState,
            [tag]: !prevState[tag]
        }));
    };

    const handleSearch = (searchValue) => {
        const filtered = dummyEvents.filter(event =>
            event.title.toLowerCase().includes(searchValue.toLowerCase()) ||
            event.description.toLowerCase().includes(searchValue.toLowerCase())
        );
        setFilteredEvents(filtered);
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
                <div id="box">
                    <Row className="ml-1" style={{ display: "flex" }}>
                        <h1 className="font-weight-bold" style={{ align: "left", display: "flex" }}>MeetingPlace</h1>
                        <h6 style={{ align: "right", display: "flex" }}>everything, everywhere, all from uoft</h6>
                    </Row>

                    <Row className="row-cols-lg-auto mt-4 align-items-center">
                        <Search onSearch={handleSearch} />
                        <Row>
                            {available_tags.map((tag, index) => (
                                <Col key={index}>
                                    <FilterButton tag={tag} isToggled={toggledTags[tag]} onToggle={handleToggle} />
                                </Col>
                            ))}
                            <Col>
                                <SortDropDown sortOption={sortOption} setSortOption={setSortOption} />
                            </Col>
                        </Row>
                    </Row>
                </div>

                <div id="bottombox"/>

                <Container fluid="md" className="bulletin-board">
                    <Row>
                        {sortedEvents.map((event, index) => (
                            <Col lg="4" md="6" sm="12" className="mb-4" key={index}>
                                <Card className="card">
                                    <CardBody className="card-body">
                                        <CardHeader tag="h3" style={{ backgroundColor: "white" }}>{event.title}</CardHeader>
                                        <CardText>{event.description}</CardText>
                                        <CardText>{event.date.toLocaleString()}</CardText>
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
