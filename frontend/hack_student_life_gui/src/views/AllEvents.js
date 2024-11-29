import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState, Fragment } from "react";
import { Row, Card, CardBody, CardTitle, CardText, Container, CardHeader, Button, Col } from "reactstrap";
import { faRightToBracket } from "@fortawesome/free-solid-svg-icons";
import RedirectButton from "../components/RedirectButton";
import Search from "../components/Search";
import Tags from "../components/Tags";
import Retrieve from "../components/Retrieve";
import { useEvents } from "../context/EventsContext";


function AllEvents() {
    const dummyEvents = [
        { id: 1, title: "Career Fair", description: "Annual Spring Career Fair featuring top tech companies and startups", time: "10:00 AM", location: "Student Union Ballroom", tags: ["tag1", "tag2"]},
        { id: 2, title: "Research Symposium", description: "Undergraduate research presentations across all disciplines", time: "2:00 PM", location: "Science Center Auditorium", tags: ["tag3", "tag4"]},
        { id: 3, title: "Club Fair", description: "Explore and join student organizations on campus", time: "11:00 AM", location: "Campus Quad", tags: ["tag1", "tag3"]},
        { id: 4, title: "Guest Speaker: Tech Innovation", description: "Industry leader discusses future of AI and robotics", time: "4:00 PM", location: "Engineering Building Room 101", tags: ["tag2", "tag4"]},
        { id: 5, title: "Cultural Festival", description: "Celebrate diversity with food, performances and activities", time: "12:00 PM", location: "Student Center Plaza", tags: ["tag1", "tag4"]},
        { id: 6, title: "Wellness Workshop", description: "Learn stress management and mindfulness techniques", time: "3:00 PM", location: "Health Center Conference Room", tags: ["tag2", "tag3"]},
        { id: 7, title: "Hackathon Kickoff", description: "24-hour coding competition with amazing prizes", time: "6:00 PM", location: "Computer Science Building", tags: ["tag1", "tag2"]},
        { id: 8, title: "Art Exhibition Opening", description: "Student artwork showcase and gallery reception", time: "5:00 PM", location: "Fine Arts Gallery", tags: ["tag3", "tag4"]},
        { id: 9, title: "Sports Tournament", description: "Intramural basketball championship games", time: "1:00 PM", location: "Recreation Center Courts", tags: ["tag2", "tag4"]},
        { id: 10, title: "Study Abroad Fair", description: "Learn about international exchange programs", time: "11:30 AM", location: "International Center", tags: ["tag1", "tag3"]},
    ];
    const { events, loading, error, fetchEvents } = useEvents();
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
    const handleSearch = (searchTerm) => {
        setSearch(searchTerm);
        fetchEvents(searchTerm);
    };
    return <Fragment>
        <div>

            <Container fluid="md">
                <Search onSearchChange={handleSearch}/>
                <Retrieve />
                {filteredEvents.length === 0 ? (
                    <Row className="mb-2">
                        <Card>
                            <CardBody>
                                <CardTitle tag="h3">No events found</CardTitle>
                            </CardBody>
                        </Card>
                    </Row>
                ) : (
                    filteredEvents.map((event) => (
                        <Row className="mb-2">
                            <Card>
                                <CardBody>
                                    <CardTitle tag="h3">{event.title}</CardTitle>
                                    <CardText>{event.description}</CardText>
                                    {/* <CardText>{event.time}</CardText> */}
                                    {event.date && <CardText>Date: {event.date}</CardText>}
                                    <CardText>{event.location}</CardText>
                                    <RedirectButton icon={faRightToBracket} link={event.source_url} />
                                    {console.log(event.tags)}
                                    {event.tags.map((tag) => (
                                        <Tags tag={tag} />
                                    ))}
                                </CardBody>
                            </Card>
                        </Row>
                    ))
                )}
            </Container>

        </div>
    </Fragment>;
}

export default AllEvents;
