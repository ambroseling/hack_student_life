import React from 'react';
import { Container, Row, Col, Card, CardBody, CardTitle } from 'reactstrap';


const Groups = () => {
    const dummyGroups = [  
        { id: 1, name: "Group 1", description: "Group 1 description", members: ["Member 1", "Member 2", "Member 3"] },
        { id: 2, name: "Group 2", description: "Group 2 description", members: ["Member 1", "Member 2", "Member 3"] },
        { id: 3, name: "Group 3", description: "Group 3 description", members: ["Member 1", "Member 2", "Member 3"] },
    ];

    return (
        <Container>
            <h1>Groups</h1>
        </Container>
    );
};

export default Groups;