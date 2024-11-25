import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState, Fragment } from "react";
import { Row, Card, CardBody, CardTitle, CardText, Container } from "reactstrap";
import { faRightToBracket } from "@fortawesome/free-solid-svg-icons";
import RedirectButton from "../components/RedirectButton";
import Search from "../components/Search";
import Tags from "../components/Tags";
import { useEvents } from "../context/EventsContext";

function AllEvents() {
    const dummyEvents = [
        { id: 1, name: "Career Fair", description: "Annual Spring Career Fair featuring top tech companies and startups", time: "10:00 AM", location: "Student Union Ballroom", tags: ["tag1", "tag2"]},
        { id: 2, name: "Research Symposium", description: "Undergraduate research presentations across all disciplines", time: "2:00 PM", location: "Science Center Auditorium", tags: ["tag3", "tag4"]},
        { id: 3, name: "Club Fair", description: "Explore and join student organizations on campus", time: "11:00 AM", location: "Campus Quad", tags: ["tag1", "tag3"]},
        { id: 4, name: "Guest Speaker: Tech Innovation", description: "Industry leader discusses future of AI and robotics", time: "4:00 PM", location: "Engineering Building Room 101", tags: ["tag2", "tag4"]},
        { id: 5, name: "Cultural Festival", description: "Celebrate diversity with food, performances and activities", time: "12:00 PM", location: "Student Center Plaza", tags: ["tag1", "tag4"]},
        { id: 6, name: "Wellness Workshop", description: "Learn stress management and mindfulness techniques", time: "3:00 PM", location: "Health Center Conference Room", tags: ["tag2", "tag3"]},
        { id: 7, name: "Hackathon Kickoff", description: "24-hour coding competition with amazing prizes", time: "6:00 PM", location: "Computer Science Building", tags: ["tag1", "tag2"]},
        { id: 8, name: "Art Exhibition Opening", description: "Student artwork showcase and gallery reception", time: "5:00 PM", location: "Fine Arts Gallery", tags: ["tag3", "tag4"]},
        { id: 9, name: "Sports Tournament", description: "Intramural basketball championship games", time: "1:00 PM", location: "Recreation Center Courts", tags: ["tag2", "tag4"]},
        { id: 10, name: "Study Abroad Fair", description: "Learn about international exchange programs", time: "11:30 AM", location: "International Center", tags: ["tag1", "tag3"]},
    ];
    const {events, loading, error } = useEvents();
    const [search, setSearch] = useState("");
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [tags, setTags] = useState([]);
    const [modalOpen, setModalOpen] = useState(false);
    const filteredEvents = events.filter((event) => {
        return (
            (event.title.toLowerCase().includes(search.toLowerCase())) &&
            tags.every((tag) => event.tags.includes(tag))
        );
    });
    return <Fragment>
        <div>
            <Row className="mt-3 mb-3 align-items-center text-center">
                <h1 className="font-weight-bold">everything, everywhere, all uoft</h1>
            </Row>

            <Container fluid="md">
                <Search/>

                {
                    filteredEvents.map((event) => (
                <Row className="mb-2">
                    <Card>
                        <CardBody>
                            <CardTitle tag="h3">{event.title}</CardTitle>
                            <CardText>{event.description}</CardText>
                            <CardText>{event.time}</CardText>
                            <CardText>{event.location}</CardText>
                            <RedirectButton icon={faRightToBracket} link={`/event/${event.id}`} />
                            {console.log(event.tags)}
                            {event.tags.map((tag) => (
                                <Tags tag={tag} />
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